"""
Pytest suite for requirements_sync.py - the venv-sync/dev-tool script at the
repo root that regenerates requirements.txt / requirements-win_dev.txt from
the live installation and audits them.

Only the pure logic is exercised here. The write step (compile_from_installed)
is pointed at tmp_path outputs and its `pip check` subprocess call is mocked,
so no real requirements files are ever touched and nothing talks to the
network. main() is not invoked directly; subprocess-based branches (--outdated)
are stubbed via patching module-level `run`.
"""

import importlib.metadata as md
import runpy
import sys
from types import SimpleNamespace

import pytest

import requirements_sync as rs
# [AI] Requirement is the single name taken from packaging; it parses the pinned
# specifier strings so the audit can compare them against the live installation.
from packaging.requirements import Requirement


def _fake_dist(name, version, requires=None):
    return SimpleNamespace(
        metadata={"Name": name, "Version": version},
        version=version,
        requires=requires or [],
    )


class TestNorm:
    """
    Name canonicalisation - case folded and separators unified.
    """
    def test_canonicalizes_case_and_separators(self):
        assert rs.norm("requests") == "requests"
        assert rs.norm("PyQt5") == "pyqt5"
        assert rs.norm("scikit-learn") == "scikit-learn"
        assert rs.norm("Scikit_Learn") == "scikit-learn"


class TestReadDirect:
    """
    Parsing requirements.txt directly - comments, blank lines, extra
    specifiers and the repository's real file.
    """
    def test_skips_comments_and_blank_lines(self, tmp_path):
        f = tmp_path / "reqs.in"
        f.write_text("# comment\n\npip\n   \n# another\npytest-pretty\n", encoding="utf-8")
        reqs = rs.read_direct(f)
        names = [r.name for r in reqs]
        assert names == ["pip", "pytest-pretty"]

    def test_parses_extra_specifiers(self, tmp_path):
        f = tmp_path / "reqs.in"
        f.write_text("coverage[toml]\n", encoding="utf-8")
        reqs = rs.read_direct(f)
        assert reqs[0].name == "coverage"
        assert reqs[0].extras == {"toml"}

    def test_real_requirements_in_files_parse(self):
        a = rs.read_direct(rs.TIER_A_IN)
        b = rs.read_direct(rs.TIER_B_IN)
        assert {r.name for r in a} >= {"pytest", "numpy", "pandas", "requests"}
        assert {r.name for r in b} >= {"jupyter", "mypy", "colorama"}


class TestInstalledIndex:
    """
    The installed-distribution index, with canonical keys and values
    preserved.
    """
    def test_keys_are_canonical_and_values_are_preserved(self, monkeypatch):
        fake_left = SimpleNamespace(metadata={"Name": "requests"})
        fake_center = SimpleNamespace(metadata={"Name": "Scikit_Learn"})
        fake_right = SimpleNamespace(metadata={"Name": "PyQt5"})
        monkeypatch.setattr(
            md, "distributions", lambda: [fake_left, fake_center, fake_right]
        )
        index = rs.installed_index()
        assert index == {
            "requests": fake_left,
            "scikit-learn": fake_center,
            "pyqt5": fake_right,
        }


class TestDepsFor:
    """
    Base dependencies always included, with the extra-gated package
    appearing only when the extra is wanted.
    """
    def test_base_dependencies_always_included(self):
        dist = _fake_dist("requests", "1.0", requires=["certifi>=2"])
        deps = rs.deps_for(dist, frozenset())
        assert [r.name for r in deps] == ["certifi"]

    def test_extra_gated_dependency_included_when_extra_wanted(self):
        dist = _fake_dist(
            "coverage", "1.0",
            requires=["tomli; extra == 'toml'", "pytest; python_version >= '3.8'"],
        )
        with_extra = [r.name for r in rs.deps_for(dist, frozenset(["toml"]))]
        assert "tomli" in with_extra

    def test_extra_gated_dependency_omitted_when_extra_unwanted(self):
        dist = _fake_dist("coverage", "1.0", requires=["tomli; extra == 'toml'"])
        plain = [r.name for r in rs.deps_for(dist, frozenset())]
        assert "tomli" not in plain

    def test_dist_with_no_requires_returns_empty_list(self):
        dist = _fake_dist("jupyter", "1.0", requires=None)
        assert rs.deps_for(dist, frozenset()) == []


class TestTierClosure:
    """
    Walking the installed dependency graph - extras unlocking packages,
    uninstalled packages reported as missing and duplicates skipped.
    """
    def _index(self):
        certifi = _fake_dist("certifi", "2026.1", requires=[])
        requests = _fake_dist("requests", "2.32", requires=["certifi>=2", "PyYAML; extra == 'yaml'"])
        pyyaml = _fake_dist("PyYAML", "6.0", requires=[])
        return {
            "certifi": certifi,
            "requests": requests,
            "pyyaml": pyyaml,
        }

    def test_walks_the_installed_dependency_graph(self):
        direct = [Requirement("requests")]
        state, missing = rs.tier_closure(direct, self._index(), "requirements.in")
        assert set(state) == {"requests", "certifi"}
        assert missing == set()

    def test_extra_requirement_unlocks_extra_dependencies(self):
        direct = [Requirement("requests[yaml]")]
        state, _ = rs.tier_closure(direct, self._index(), "requirements.in")
        assert set(state) == {"requests", "certifi", "pyyaml"}

    def test_uninstalled_package_is_reported_as_missing(self):
        direct = [Requirement("not-installed-pkg")]
        state, missing = rs.tier_closure(direct, self._index(), "requirements.in")
        assert "not-installed-pkg" in missing
        assert state == {}

    def test_via_label_and_extras_are_recorded_in_state(self):
        direct = [Requirement("requests[yaml]")]
        state, _ = rs.tier_closure(direct, self._index(), "requirements.in")
        assert state["requests"][0] == frozenset({"yaml"})
        assert state["requests"][1] == "requirements.in"
        assert state["certifi"][1] == "requests"

    def test_duplicate_dependency_of_missing_package_is_skipped(self):
        # Two top-level packages both point at one missing dependency; the
        # missing package is reported once and never inserted into state,
        # so a later duplicate resolution can't KeyError on it.
        index = {
            "a": _fake_dist("a", "1.0", requires=["ghost-pkg"]),
            "b": _fake_dist("b", "1.0", requires=["ghost-pkg"]),
        }
        state, missing = rs.tier_closure(
            [Requirement("a"), Requirement("b")], index, "requirements.in"
        )
        assert missing == {"ghost-pkg"}
        assert "ghost-pkg" not in state

    def test_extra_union_updates_state_and_repeat_dependency_is_skipped(self):
        # 'requests[yaml]' must merge into (not overwrite) the extras already
        # recorded for plain 'requests', and the already-visited 'certifi'
        # appearing again in the direct list is skipped silently.
        index = {
            "requests": _fake_dist(
                "requests", "2.32",
                requires=["certifi>=2", "PyYAML; extra == 'yaml'"],
            ),
            "certifi": _fake_dist("certifi", "2026.1", requires=[]),
            "pyyaml": _fake_dist("PyYAML", "6.0", requires=[]),
        }
        direct = [Requirement("requests"), Requirement("requests[yaml]"), Requirement("certifi")]
        state, missing = rs.tier_closure(direct, index, "requirements.in")
        assert state["requests"][0] == frozenset({"yaml"})
        assert "pyyaml" in state
        assert missing == set()


class TestRun:
    """
    The subprocess wrapper, exercised with a mocked run().
    """
    def test_mocked_subprocess_invocation(self, monkeypatch, capsys):
        calls = []

        def fake_run(cmd, cwd=None, check=True):
            calls.append((cmd, cwd))
            return None

        monkeypatch.setattr(rs.subprocess, "run", fake_run)
        rs.run(["pip", "--version"])
        captured = capsys.readouterr()
        assert "$ pip --version" in captured.out
        assert calls[0][0] == ["pip", "--version"]


class TestCompileFromInstalled:
    """
    Writing the pinned closure to the output files, warning on any
    missing package.
    """
    def test_writes_pinned_closure_to_output_files(self, tmp_path, monkeypatch, capsys):
        out_a = tmp_path / "requirements.txt"
        out_b = tmp_path / "requirements-win_dev.txt"
        monkeypatch.setattr(rs, "TIER_A_OUT", out_a)
        monkeypatch.setattr(rs, "TIER_B_OUT", out_b)
        monkeypatch.setattr(rs, "run", lambda cmd: print(f"\n$ {' '.join(cmd)}"))

        index = {
            "certifi": _fake_dist("certifi", "2026.1", requires=[]),
            "requests": _fake_dist("requests", "2.32", requires=["certifi>=2"]),
            "click": _fake_dist("click", "8.1", requires=[]),
        }
        monkeypatch.setattr(rs, "installed_index", lambda: index)
        a_path = tmp_path / "a.in"
        b_path = tmp_path / "b.in"
        a_path.write_text("requests\n", encoding="utf-8")
        b_path.write_text("click\n", encoding="utf-8")
        monkeypatch.setattr(rs, "TIER_A_IN", a_path)
        monkeypatch.setattr(rs, "TIER_B_IN", b_path)

        rs.compile_from_installed()

        text_a = out_a.read_text(encoding="utf-8")
        text_b = out_b.read_text(encoding="utf-8")
        assert "requests==2.32    # via requirements.in" in text_a
        assert "certifi==2026.1    # via requests" in text_a
        assert "click==8.1    # via requirements-win_dev.in" in text_b
        assert "certifi" not in text_b
        assert "pip check" in capsys.readouterr().out

    def test_missing_packages_trigger_warning(self, tmp_path, monkeypatch, capsys):
        out_a = tmp_path / "requirements.txt"
        out_b = tmp_path / "requirements-win_dev.txt"
        monkeypatch.setattr(rs, "TIER_A_OUT", out_a)
        monkeypatch.setattr(rs, "TIER_B_OUT", out_b)
        monkeypatch.setattr(rs, "run", lambda cmd: None)

        a_path = tmp_path / "a.in"
        b_path = tmp_path / "b.in"
        a_path.write_text("ghost-pkg\n", encoding="utf-8")
        b_path.write_text("", encoding="utf-8")
        monkeypatch.setattr(rs, "TIER_A_IN", a_path)
        monkeypatch.setattr(rs, "TIER_B_IN", b_path)
        monkeypatch.setattr(rs, "installed_index", lambda: {})

        rs.compile_from_installed()
        assert "WARNING: not installed" in capsys.readouterr().out


class TestParseCompiled:
    """
    Reading pinned names back out of a frozen requirements file.
    """
    def test_extracts_pinned_names_from_frozen_file(self, tmp_path):
        f = tmp_path / "requirements.txt"
        f.write_text(
            "# header\n"
            "requests==2.32    # via requirements.in\n"
            "coverage[toml]==7.16.0    # via requirements.in\n"
            "psycopg2==2.9.9    # via requirements.in\n",
            encoding="utf-8",
        )
        assert rs.parse_compiled(f) == ["requests", "coverage", "psycopg2"]

    def test_empty_file_yields_empty_list(self, tmp_path):
        f = tmp_path / "empty.txt"
        f.write_text("", encoding="utf-8")
        assert rs.parse_compiled(f) == []


class TestTable:
    """
    The markdown version table, showing missing installed packages.
    """
    def test_prints_markdown_rows_with_versions(self, capsys):
        rs.table("Tier A", ["requests", "numpy"], {"requests": "2.32", "numpy": "1.26"}, "A")
        out = capsys.readouterr().out
        assert "## Tier A" in out
        assert "| `requests` | 2.32 | A |" in out
        assert "| `numpy` | 1.26 | A |" in out

    def test_missing_installed_package_shows_missing(self, capsys):
        rs.table("Tier B", ["mypy"], {}, "B")
        assert "| `mypy` | MISSING | B |" in capsys.readouterr().out


class TestAudit:
    """
    The audit step - exit code and printed dependency caps when in sync.
    """
    def test_in_sync_returns_zero_and_prints_caps(self, capsys):
        code = rs.audit()
        out = capsys.readouterr().out
        assert code in (0, 1)
        assert "=== ENVIRONMENT AUDIT ===" in out
        assert "Installed packages" in out
        assert "Audit:" in out


class TestMain:
    """
    The CLI of requirements_sync.py - default sync, --check skipping the
    compile, the outdated upgrade check and the main guard.
    """
    def test_default_sync_compiles_and_audits(self, monkeypatch, capsys):
        # No flags -> compile_from_installed() runs, then audit() runs; the
        # argv is stubbed so argparse consumes it instead of the test runner's.
        monkeypatch.setattr(rs, "compile_from_installed", lambda: print("compiled"))
        monkeypatch.setattr(rs, "audit", lambda: 0)
        monkeypatch.setattr(sys, "argv", ["requirements_sync.py"])

        assert rs.main() == 0
        assert "compiled" in capsys.readouterr().out

    def test_check_mode_skips_compile(self, monkeypatch, capsys):
        # --check short-circuits before compile, so even a 7 exit code from
        # audit proves no compilation side-effect took place.
        monkeypatch.setattr(rs, "compile_from_installed", lambda: print("compiled"))
        monkeypatch.setattr(rs, "audit", lambda: 7)
        monkeypatch.setattr(sys, "argv", ["requirements_sync.py", "--check"])

        assert rs.main() == 7
        assert "compiled" not in capsys.readouterr().out

    def test_outdated_flag_runs_upgrade_check(self, monkeypatch, capsys):
        # --outdated without subprocess factually reaching pip is made
        # observable by stubbing run(); the pip list --outdated cmd proves
        # the upgrade-check branch was taken.
        monkeypatch.setattr(rs, "audit", lambda: 0)
        monkeypatch.setattr(rs, "run", lambda cmd: print(f"RUN {' '.join(cmd)}"))
        monkeypatch.setattr(sys, "argv", ["requirements_sync.py", "--check", "--outdated"])

        assert rs.main() == 0
        assert "pip list --outdated" in capsys.readouterr().out

    def test_main_guard_runs_check_mode(self, monkeypatch, capsys):
        # Running the real file as __main__ proves the bottom guard forwards
        # sys.argv; audit() is real here so capture shows the banner, and
        # SystemExit is expected because audit() calls sys.exit().
        monkeypatch.setattr(sys, "argv", ["requirements_sync.py", "--check"])
        with pytest.raises(SystemExit):
            runpy.run_path(str(rs.ROOT / "requirements_sync.py"), run_name="__main__")
        assert "=== ENVIRONMENT AUDIT ===" in capsys.readouterr().out


