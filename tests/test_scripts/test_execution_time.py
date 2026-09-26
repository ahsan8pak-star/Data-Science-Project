"""
Pytest suite for scripts/execution_time.py - the dev harness that renders a
`tree /f`-style directory map of the project and benchmarks every .py file
under a user-selected folder (PASS / INTERACTIVE / TIMEOUT / FAIL / ERROR +
timings). INTERACTIVE is separate from FAIL because 62 of the 183 files stop
at an input() prompt, and folding those into FAIL hid the 2 real errors.

subprocess.run is mocked in the benchmark tests so no real scripts spawn.
"""

import subprocess
from pathlib import Path

import pytest

from scripts.execution_time import (
    PROJECT_ROOT,
    TREE_SKIP,
    execute_project_scripts,
    print_directory_tree,
    resolve_folder,
)

# [AI] Those five names are the tool's whole public surface, imported directly so
# each helper can be driven without entering the interactive main() loop.

# Absolute path so runpy's re-execution is attributed by coverage (a relative
# co_filename is not mapped back to the measured source file).
SCRIPT_PATH = Path(__file__).resolve().parents[2] / "scripts" / "execution_time.py"


def _make_sample_tree(root):
    (root / "beta").mkdir(parents=True, exist_ok=True)
    (root / "beta" / "nested.py").write_text("x = 1\n", encoding="utf-8")
    (root / "beta" / "nested.txt").write_text("hi\n", encoding="utf-8")
    (root / "alpha.txt").write_text("a\n", encoding="utf-8")
    for skipped in (".git", "__pycache__", "htmlcov"):
        (root / skipped).mkdir(exist_ok=True)
        (root / skipped / "entry").write_text("x\n", encoding="utf-8")


class TestDirectoryTree:
    """
    The tree /f-style renderer in execution_time.py - directories before
    files, trailing backslashes, connector glyphs, TREE_SKIP exclusions and
    silent handling of an uniterable path.
    """
    def test_lists_files_and_nested_directories(self, tmp_path, capsys):
        _make_sample_tree(tmp_path)
        print_directory_tree(tmp_path)
        out = capsys.readouterr().out
        assert "beta\\" in out
        assert "alpha.txt" in out
        assert "nested.py" in out
        assert "nested.txt" in out

    def test_directories_are_shown_with_trailing_backslash(self, tmp_path, capsys):
        _make_sample_tree(tmp_path)
        print_directory_tree(tmp_path)
        out = capsys.readouterr().out
        assert "beta\\" in out
        assert "nested" not in out.replace("beta", "").replace("nested.py", "").replace("nested.txt", "")

    def test_omits_generated_and_vendored_folders(self, tmp_path, capsys):
        for name in TREE_SKIP:
            (tmp_path / name).mkdir(exist_ok=True)
        (tmp_path / "keep.py").write_text("x = 1\n", encoding="utf-8")
        print_directory_tree(tmp_path)
        out = capsys.readouterr().out
        for name in TREE_SKIP:
            assert name not in out
        assert "keep.py" in out

    def test_directories_listed_before_files(self, tmp_path, capsys):
        _make_sample_tree(tmp_path)
        print_directory_tree(tmp_path)
        out = capsys.readouterr().out
        assert out.index("beta") < out.index("alpha.txt")

    def test_uses_tree_connector_glyphs(self, tmp_path, capsys):
        _make_sample_tree(tmp_path)
        print_directory_tree(tmp_path)
        out = capsys.readouterr().out
        assert "├── beta\\" in out
        assert "│" in out
        assert "└── alpha.txt" in out

    def test_path_that_cannot_be_iterated_returns_silently(self, tmp_path, capsys):

        # iterdir() on a plain file raises NotADirectoryError (an OSError),
        # which print_directory_tree swallows with a bare `return`.
        target = tmp_path / "not_a_directory.py"
        target.write_text("x = 1\n", encoding="utf-8")
        print_directory_tree(target)
        assert capsys.readouterr().out == ""


class TestResolveFolder:
    """
    Folder-name resolution in execution_time.py - bare names, relative and
    absolute paths, trailing backslashes, ambiguity and non-folders.
    """
    @pytest.fixture()
    def _project(self, tmp_path, monkeypatch):
        monkeypatch.setattr("scripts.execution_time.PROJECT_ROOT", tmp_path)
        return tmp_path

    def test_unique_folder_found_by_bare_name(self, _project):
        target = _project / "python" / "syntax_exercises"
        target.mkdir(parents=True)
        assert resolve_folder("syntax_exercises") == target

    def test_relative_path_resolves(self, _project):
        target = _project / "python" / "syntax_exercises"
        target.mkdir(parents=True)
        assert resolve_folder("python/syntax_exercises") == target

    def test_absolute_path_returns_unchanged(self, _project):
        target = _project / "python" / "syntax_exercises"
        target.mkdir(parents=True)
        assert resolve_folder(str(target)) == target

    def test_bare_name_with_trailing_backslash(self, _project):
        target = _project / "python" / "syntax_exercises"
        target.mkdir(parents=True)
        assert resolve_folder("syntax_exercises\\") == target

    def test_ambiguous_name_returns_none(self, _project):
        (_project / "a" / "same").mkdir(parents=True)
        (_project / "b" / "same").mkdir(parents=True)
        assert resolve_folder("same") is None

    def test_unknown_name_returns_none(self, _project):
        assert resolve_folder("does_not_exist") is None

    def test_file_is_not_a_folder(self, _project):
        (_project / "python").mkdir()
        (_project / "x.py").write_text("x = 1\n", encoding="utf-8")
        assert resolve_folder("x.py") is None


class TestExecuteProjectScripts:
    """
    Per-folder benchmarking in execution_time.py - every status in the
    report, a missing directory and the bare-name fallback.
    """
    def _install_fake_subprocess(self, monkeypatch):
        order = ["pass", "fail", "timeout", "error"]

        def fake_run(cmd, **kwargs):
            kind = order.pop(0)
            if kind == "pass":
                return subprocess.CompletedProcess(args=cmd, returncode=0, stdout="", stderr="")
            if kind == "fail":
                return subprocess.CompletedProcess(args=cmd, returncode=1, stdout="", stderr="")
            if kind == "timeout":
                raise subprocess.TimeoutExpired(cmd="python", timeout=2)
            raise RuntimeError("boom")

        monkeypatch.setattr("scripts.execution_time.subprocess.run", fake_run)

    def test_report_covers_all_statuses(self, tmp_path, capsys, monkeypatch):
        for name in ("a.py", "b.py", "c.py", "d.py"):
            (tmp_path / name).write_text("print(1)\n", encoding="utf-8")
        self._install_fake_subprocess(monkeypatch)

        execute_project_scripts(tmp_path)
        out = capsys.readouterr().out

        assert "execution report" in out
        assert "PASS" in out
        assert "FAIL" in out
        assert "TIMEOUT" in out
        assert "ERROR" in out
        assert "TOTAL FILES: 4" in out
        assert "TOTAL TIME:" in out

    def test_missing_directory_reports_zero_files(self, tmp_path, capsys, monkeypatch):
        self._install_fake_subprocess(monkeypatch)
        execute_project_scripts(tmp_path / "does_not_exist")
        out = capsys.readouterr().out
        assert "TOTAL FILES: 0" in out

    def test_file_outside_parent_falls_back_to_bare_name(self, tmp_path, capsys, monkeypatch):

        # A .py file that cannot be expressed relative to base_path.parent
        # raises ValueError inside the try, so the except stores just the
        # file name and the row still renders as PASS.
        from pathlib import Path

        monkeypatch.setattr(Path, "rglob", lambda self, pattern: iter([Path("C:/outside/base.py")]))
        monkeypatch.setattr(
            "scripts.execution_time.subprocess.run",
            lambda cmd, **kwargs: subprocess.CompletedProcess(
                args=cmd, returncode=0, stdout="", stderr=""
            ),
        )

        execute_project_scripts(tmp_path)
        out = capsys.readouterr().out

        assert "base.py" in out
        assert "TOTAL FILES: 1" in out


class TestStatusClassification:
    """
    How a child's outcome maps to a status. 62 of the 183 files stop at an
    input() prompt, and calling those FAIL buried the two real errors; the
    separate INTERACTIVE status is what makes FAIL mean something.
    """
    def _row_for_solo(self, tmp_path, capsys, monkeypatch, returncode, stderr=""):
        """
        Returns the status word on solo.py's own report row. The report also
        prints a legend naming every status, so assertions have to target the
        row rather than the whole output.
        """
        (tmp_path / "solo.py").write_text("print(1)\n", encoding="utf-8")
        monkeypatch.setattr(
            "scripts.execution_time.subprocess.run",
            lambda cmd, **kw: subprocess.CompletedProcess(
                args=cmd, returncode=returncode, stdout="", stderr=stderr
            ),
        )
        execute_project_scripts(tmp_path)
        out = capsys.readouterr().out
        for line in out.splitlines():
            if "solo.py" in line:
                for word in ("PASS", "INTERACTIVE", "TIMEOUT", "FAIL", "ERROR"):
                    if word in line:
                        return word
        raise AssertionError(f"no status on solo.py's row:\n{out}")

    def test_clean_exit_is_pass(self, tmp_path, capsys, monkeypatch):
        assert self._row_for_solo(tmp_path, capsys, monkeypatch, 0) == "PASS"

    def test_stopping_at_input_is_interactive_not_fail(self, tmp_path, capsys, monkeypatch):
        status = self._row_for_solo(
            tmp_path, capsys, monkeypatch, 1,
            stderr="Traceback (most recent call last):\nEOFError: EOF when reading a line\n",
        )
        assert status == "INTERACTIVE"

    def test_any_other_error_is_still_fail(self, tmp_path, capsys, monkeypatch):
        status = self._row_for_solo(
            tmp_path, capsys, monkeypatch, 1,
            stderr="Traceback (most recent call last):\nImportError: cannot import name 'x'\n",
        )
        assert status == "FAIL"

    def test_empty_stderr_failure_is_fail(self, tmp_path, capsys, monkeypatch):
        # The harness must not infer interactivity from a bare non-zero exit
        assert self._row_for_solo(tmp_path, capsys, monkeypatch, 1) == "FAIL"


class TestChildEnvironment:
    """
    The interpreter the benchmark spawns, and the encoding its children get.
    Both were wrong and both silently mis-scored files.
    """
    def test_benchmark_uses_the_running_interpreter_not_bare_python(self):
        import sys as _sys
        from scripts.execution_time import BENCHMARK_PYTHON
        assert BENCHMARK_PYTHON == _sys.executable
        assert Path(BENCHMARK_PYTHON).name.lower().startswith("python")

    def test_child_env_forces_utf8_stdout(self):
        from scripts.execution_time import CHILD_ENV
        assert CHILD_ENV.get("PYTHONIOENCODING") == "utf-8"

    def test_children_receive_the_env_and_utf8_decoding(self, tmp_path, capsys, monkeypatch):
        (tmp_path / "solo.py").write_text("print(1)\n", encoding="utf-8")
        seen = {}

        def fake_run(cmd, **kwargs):
            seen["cmd"] = cmd
            seen["kwargs"] = kwargs
            return subprocess.CompletedProcess(args=cmd, returncode=0, stdout="", stderr="")

        monkeypatch.setattr("scripts.execution_time.subprocess.run", fake_run)
        execute_project_scripts(tmp_path)
        capsys.readouterr()

        from scripts.execution_time import BENCHMARK_PYTHON
        assert seen["cmd"][0] == BENCHMARK_PYTHON
        assert seen["kwargs"]["env"]["PYTHONIOENCODING"] == "utf-8"
        assert seen["kwargs"]["encoding"] == "utf-8"
        assert seen["kwargs"]["errors"] == "replace"

    def test_project_root_is_the_scripts_parent_not_a_baked_path(self):
        # A literal machine path would break the harness on any other machine;
        # deriving it from __file__ means the assertion is structural, not textual.
        assert (PROJECT_ROOT / "scripts" / "execution_time.py").is_file()
        source = SCRIPT_PATH.read_text(encoding="utf-8")
        assert 'Path(r"C:' not in source
        assert "Path(__file__).resolve().parent.parent" in source


class TestMain:
    """
    The interactive main() of execution_time.py - a typed folder, the whole
    python/ tree, the --all flag and re-prompting on an unknown name.
    """
    def _instal_main(self, tmp_path, monkeypatch, inputs):
        folder = tmp_path / "python" / "syntax_exercises"
        folder.mkdir(parents=True)
        monkeypatch.setattr("scripts.execution_time.PROJECT_ROOT", tmp_path)
        results = []
        monkeypatch.setattr(
            "scripts.execution_time.execute_project_scripts",
            lambda target: results.append(target),
        )
        iterator = iter(inputs)
        monkeypatch.setattr("builtins.input", lambda prompt="": next(iterator))
        return folder, results

    def test_typed_folder_is_executed_then_quits(self, tmp_path, monkeypatch, capsys):
        folder, results = self._instal_main(tmp_path, monkeypatch, ["syntax_exercises", "quit"])
        from scripts.execution_time import main

        main()

        assert results == [folder]
        assert "is currently running" in capsys.readouterr().out

    def test_enter_runs_whole_python_folder(self, tmp_path, monkeypatch):
        (tmp_path / "python").mkdir()
        _, results = self._instal_main(tmp_path, monkeypatch, ["", "quit"])
        from scripts.execution_time import main, PROJECT_ROOT

        main()

        assert results == [PROJECT_ROOT / "python"]

    def test_all_flag_runs_without_prompting(self, tmp_path, monkeypatch):
        (tmp_path / "python").mkdir()
        monkeypatch.setattr("scripts.execution_time.PROJECT_ROOT", tmp_path)
        results = []
        monkeypatch.setattr(
            "scripts.execution_time.execute_project_scripts",
            lambda target: results.append(target),
        )
        monkeypatch.setattr("builtins.input", lambda prompt="": pytest.fail("input must not be called"))
        monkeypatch.setattr("sys.argv", ["scripts/execution_time.py", "--all"])
        from scripts.execution_time import main, PROJECT_ROOT

        main()

        assert results == [PROJECT_ROOT / "python"]

    def test_unknown_folder_skips_and_prompts_again(self, tmp_path, monkeypatch, capsys):

        # resolve_folder returns None for an unrecognised name, so main()
        # hits the `if target is None: continue` guard and loops back to
        # the prompt instead of benchmarking anything.
        _, results = self._instal_main(tmp_path, monkeypatch, ["does_not_exist", "quit"])
        from scripts.execution_time import main

        main()

        assert results == []
        assert "Exiting." in capsys.readouterr().out


class TestModuleLevelReconfigure:
    """
    The module-level stdout reconfigure, whose failure must stay silent.
    """
    def test_stdout_reconfigure_failure_is_swallowed(self, monkeypatch):

        # Lines 10-11 only execute if reconfigure() itself raises. Swapping
        # in a stdout whose reconfigure() throws proves the bare except keeps
        # the module importing cleanly instead of crashing.
        import io
        import runpy
        import sys

        buffer = io.StringIO()
        fake_stdout = type(
            "FakeStdout",
            (),
            {
                "write": buffer.write,
                "reconfigure": lambda *args, **kwargs: (_ for _ in ()).throw(
                    OSError("console cannot be reconfigured")
                ),
            },
        )()

        monkeypatch.setattr(sys, "stdout", fake_stdout)
        runpy.run_path(str(SCRIPT_PATH), run_name="execution_time_reconfigure_probe")

        assert buffer.getvalue() == ""


class TestMainGuard:
    """
    The if __name__ guard that fires the tool when run as a script.
    """
    def test_running_as_main_fires_the_guard(self, monkeypatch, capsys):

        # run_name="__main__" triggers the module-level guard (line 160).
        # "--all" skips the tree dump and subprocess.run is stubbed, so this
        # only exercises main()'s --all branch through to the break.
        import runpy
        import sys

        monkeypatch.setattr(
            subprocess,
            "run",
            lambda cmd, **kwargs: subprocess.CompletedProcess(
                args=cmd, returncode=0, stdout="", stderr=""
            ),
        )
        monkeypatch.setattr(sys, "argv", ["scripts/execution_time.py", "--all"])

        runpy.run_path(str(SCRIPT_PATH), run_name="__main__")

        assert "is currently running" in capsys.readouterr().out


