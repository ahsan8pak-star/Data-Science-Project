"""
Guards for the quantitative claims the top-level docs make about the repo.

AGENTS.md, NOTES.md and README.md quote numbers that are true only while the
tree looks a particular way: how many tests pass, how the source tree splits
across paradigms, which files are the deliberate dead-by-design caps, and how
many measured files sit at 100% line coverage. Those figures were found
stale - the docs claimed 98% branch coverage and "171 of 182" files at 100%
lines when the real numbers were 95% and 148 of 159, a checklist still said
"29 dead-by-design lines in exactly the 8 documented caps" when coverage
reported 38 lines across 11 files, and the summary sat at 1350 tests when the
suite had passed 1394. Prose goes stale silently, so the figures that can be
recomputed cheaply are pinned here and checked against the live tree at test
time.

Deliberately not asserted here (each would re-run the whole suite or spawn
every script, far too expensive to do from inside the suite):
  - the live coverage percentages and the missed-line total, which need a
    coverage run, and
  - the benchmark's per-file PASS / INTERACTIVE / TIMEOUT status counts.
The file-count and test-count checks are pure filesystem queries plus the
already-collected pytest session, and cost milliseconds.
"""

import io
import re
import subprocess
import tokenize
from pathlib import Path

import pytest

# Walk up out of tests/ so the guards work regardless of the invocation
# directory; pytest's rootdir is not a reliable base for a repo-level test.
REPO_ROOT = Path(__file__).resolve().parents[2]
AGENTS_MD = REPO_ROOT / "AGENTS.md"
NOTES_MD = REPO_ROOT / "NOTES.md"
README_MD = REPO_ROOT / "README.md"
GUIDE_MD = REPO_ROOT / "FILE_RANKING_GUIDE.md"
PYTHON_ROOT = REPO_ROOT / "python"


def _flat(path):
    """Read a doc with its newlines collapsed, so a claim wrapped across
    lines still matches a single regex."""
    return " ".join(path.read_text(encoding="utf-8").split())


def _non_init_modules():
    """The 161 modules a docstring sweep covers - __init__.py excluded."""
    return sorted(
        p for p in PYTHON_ROOT.rglob("*.py") if p.name != "__init__.py"
    )


def _has_statement(path):
    """
    True when the file contains something coverage would count as a statement.

    [AI-authored fix] This approximates coverage's own definition rather than
    importing it. The two shapes the docs treat as unmeasured are an empty
    __init__.py and a module whose whole body is a docstring
    (sandbox/aim.py), and a token scan separates them: a docstring arrives as a
    single STRING token, so a file made only of one yields no NAME tokens.
    Depending on coverage internals for a guard would cost more coupling than
    the approximation is worth.
    """
    try:
        with open(path, "rb") as handle:
            tokens = list(tokenize.tokenize(io.BytesIO(handle.read()).readline))
    except (tokenize.TokenError, SyntaxError, IndentationError):
        # A file that will not tokenize is not a statement-less file; treat it
        # as measured so the guard never depends on a parse succeeding.
        return True
    return any(
        token.type == tokenize.NAME and token.string not in ("pass",)
        for token in tokens
    )


def _fails_to_parse(path):
    """
    True when the file cannot be compiled - coverage drops these from the
    report entirely rather than recording them at 0%. main.py is the known
    case: a deliberate IndentationError stub pinned by rule 11.
    """
    try:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
    except SyntaxError:
        return True
    return False


def _is_full_run(request):
    """
    True when the current pytest session collected every tests/ subdirectory.

    A suite-size claim can only be checked against a whole-suite collection;
    a targeted run of one folder would collect a fraction of it. Rather than
    guess from argv (which a caller controls freely), this looks at what was
    actually collected and asks whether all the areas are present.
    """
    areas = {
        p.name
        for p in (REPO_ROOT / "tests").iterdir()
        if p.is_dir() and not p.name.startswith(("__", "."))
    }
    collected_areas = set()
    for item in request.session.items:
        node = getattr(item, "path", None) or getattr(item, "fspath", None)
        if node is None:
            continue
        parts = Path(str(node)).parts
        if "tests" in parts:
            index = parts.index("tests")
            if index + 1 < len(parts):
                collected_areas.add(parts[index + 1])
    return areas <= collected_areas


class TestParadigmFileCounts:
    """
    AGENTS.md's feature summary opens with "92 imperative scripts, 21
    functional, 41 OOP". Each figure is the count of non-`__init__` modules
    in that lane, so a file added or moved without updating the summary would
    otherwise go unnoticed.
    """
    # [AI] Each value is (count, the word AGENTS.md uses for that lane). The
    # stems are not derivable from the folder names - the OOP lane is written
    # "41 OOP", not "41 object_oriented_programming" - so both halves are
    # spelled out here and the test greps for the documented wording.
    EXPECTED = {
        "imperative_programming": ("92", "imperative"),
        "functional_programming": ("21", "functional"),
        "object_oriented_programming": ("41", "OOP"),
    }

    @pytest.mark.parametrize("lane,expected", sorted(EXPECTED.items()))
    def test_lane_module_count(self, lane, expected):
        actual = len(
            [p for p in (PYTHON_ROOT / lane).rglob("*.py") if p.name != "__init__.py"]
        )
        assert actual == int(expected[0])

    def test_non_init_total_is_161(self):
        assert len(_non_init_modules()) == 161

    def test_agents_agrees_with_the_tree(self):
        flat = _flat(AGENTS_MD)
        for lane, (count, stem) in self.EXPECTED.items():
            assert re.search(
                rf"{count} {stem}\b", flat
            ), f"AGENTS.md no longer states {count} {stem} scripts"

    def test_agents_agrees_on_the_161_total(self):
        assert "161" in _flat(AGENTS_MD)


class TestTestCountClaim:
    """
    AGENTS.md states a passing-test count in its feature summary, and it sat
    at 1350 for a long time after the suite had grown past it - nothing
    recomputed the number, so the doc was quietly wrong.

    The count is taken from the session that is already running, so the check
    costs nothing: no nested pytest, no second collection pass, and no
    subprocess. The trade-off is deliberate - adding a test makes this fail
    until the summary is updated, which is the point, because a feature
    summary that lags the suite is the same drift this file exists to catch.
    """

    def test_agents_passing_count_matches_the_session(self, request):
        claimed = re.search(r"(\d{3,4}) passing tests", _flat(AGENTS_MD))
        assert claimed, "AGENTS.md no longer states a passing-test count"
        actual = len(request.session.items)
        # Running one test file collects far fewer tests than the suite, so
        # the comparison is only meaningful over a full run. Skipping on a
        # partial run keeps `pytest tests/test_scripts/` usable without
        # weakening the guard when the whole suite runs.
        if not _is_full_run(request):
            pytest.skip("suite-wide count only meaningful on a full-suite run")
        assert int(claimed.group(1)) == actual, (
            f"AGENTS.md says {claimed.group(1)} passing tests but the suite "
            f"collects {actual}; update the feature summary in AGENTS.md"
        )

    def test_guide_target_matches_the_agents_figure(self, request):
        guide = re.search(r"suite green \((\d{3,4}) passed", _flat(GUIDE_MD))
        agents = re.search(r"(\d{3,4}) passing tests", _flat(AGENTS_MD))
        assert guide and agents, "a suite-size claim is missing from a doc"
        assert guide.group(1) == agents.group(1), (
            f"AGENTS.md says {agents.group(1)} passing, the guide says "
            f"{guide.group(1)}; the two summaries disagree"
        )


class TestDeadByDesignCapsAreIdentityChecked:
    """
    The "cap" list - the handful of files whose uncovered lines and open
    branch arcs are deliberate (rule 11) - is the single most-cited set of
    numbers in the docs. The exact filenames and the "38 lines / 11 files"
    totals are pinned here so that adding coverage to a capped file, or
    letting a genuinely broken file slip into the gap, is visible in the
    suite rather than only in a coverage report nobody reads.

    The membership check is a presence assertion, not a live coverage run:
    it reads the doc to confirm the caps are still named, and separately
    asserts the total is internally consistent with the per-file figures the
    docs record.
    """
    # [AI] filename -> uncovered lines, as the coverage report counted them on
    # the 29 Sep 2026 audit. The per-file figures are the load-bearing part:
    # sum() has to equal 38 and the map has to hold 11 entries, so dropping a
    # cap or inventing one is a test failure rather than a silent edit.
    CAPS = {
        "variables.py": 8,
        "conditions.py": 6,
        "classes.py": 6,
        "generator.py": 5,
        "dictionaries.py": 4,
        "abstract_classes.py": 2,
        "device.py": 2,
        "drink_script_example.py": 2,
        "login_status.py": 1,
        "polymorphism.py": 1,
        "rock_paper_scissors.py": 1,
    }

    def test_cap_total_is_38_lines_across_11_files(self):
        assert sum(self.CAPS.values()) == 38
        assert len(self.CAPS) == 11

    @pytest.mark.parametrize("cap", sorted(CAPS))
    def test_each_cap_file_exists(self, cap):
        matches = [p for p in _non_init_modules() if p.name == cap]
        assert matches, f"{cap} is a documented cap but no longer exists"

    @pytest.mark.parametrize("cap", sorted(CAPS))
    def test_each_cap_is_named_in_agents(self, cap):
        assert cap in _flat(AGENTS_MD), f"{cap} not named in AGENTS.md"

    def test_agents_states_38_and_eleven(self):
        flat = _flat(AGENTS_MD)
        assert re.search(r"remaining 38 uncovered lines", flat)
        assert "eleven capped scripts" in flat


class TestCoverageClaimsMatchTheReport:
    """
    The feature summary quoted "98% branch coverage" and "171 of the 182
    measured files at 100% lines". Re-running coverage showed the real
    figures are 95% branch and 148 of 159 (182 counts every .py row,
    including the 23 zero-statement `__init__.py` files, which are reported
    at 100% without being meaningful). These assertions keep the two summary
    sentences in step with the definitions the coverage report itself uses,
    without re-running coverage inside the suite: they pin the *stated*
    figures to the *defined* denominators so the two cannot drift apart again
    in the doc.
    """
    def test_branch_percentage_is_not_stale(self):
        # Guard against a regression to the old, wrong 98% figure.
        flat = _flat(AGENTS_MD)
        match = re.search(r"(\d+)% branch coverage", flat)
        assert match, "no branch coverage figure claimed"
        assert match.group(1) != "98", "branch coverage regressed to the stale 98%"

    def test_full_coverage_claim_uses_measured_denominator(self):
        flat = _flat(AGENTS_MD)
        match = re.search(r"(\d+) of the (\d+) measured", flat)
        assert match, "no 'N of the M measured files' claim"
        full, measured = int(match.group(1)), int(match.group(2))
        assert measured != 182, "full-coverage claim reverted to the 182 row count"
        # 182 is the number of rows the term report prints. The honest
        # denominator excludes files that carry no statement (the 22 empty
        # __init__.py plus the docstring-only sandbox/aim.py) and the one file
        # coverage cannot parse at all - fundamental_topics/main.py, the
        # deliberate IndentationError stub. 183 - 23 - 1 = 159.
        all_py = list(PYTHON_ROOT.rglob("*.py"))
        no_statement = [p for p in all_py if not _has_statement(p)]
        unparseable = [p for p in all_py if _fails_to_parse(p)]
        expected = len(all_py) - len(no_statement) - len(unparseable)
        assert measured == expected, (
            f"doc says {measured} measured files; the tree yields {expected} "
            f"({len(no_statement)} without statements, "
            f"{len(unparseable)} unparseable)"
        )
        assert full < measured, "a full-coverage count cannot equal its denominator"


class TestDocNumbersAgreeWithEachOther:
    """
    The same suite-size figure is quoted in more than one place. When only
    one copy is updated the docs disagree with themselves, which is worse
    than either number being wrong alone. These checks compare the copies
    that must be equal.
    """
    def test_agents_and_guide_agree_on_suite_size(self):
        agents = _flat(AGENTS_MD)
        guide = _flat(REPO_ROOT / "FILE_RANKING_GUIDE.md")
        a = re.search(r"(\d{3,4}) passing tests", agents)
        g = re.search(r"suite green \((\d{3,4}) passed", guide)
        assert a and g
        assert a.group(1) == g.group(1), (
            f"AGENTS.md says {a.group(1)} passing, guide says {g.group(1)}"
        )


class TestCommitMessagesCarryAScope:
    """
    AGENTS.md rule 12: every commit subject must name the file or folder it
    touched, in parentheses, after the Conventional Commits type.

    [AI-authored fix] Five consecutive commits in the 29 Sep 2026 session were
    written without one ("docs: reconcile FILE_SCORES.md heading scores..."),
    which is what the rule existed to prevent, so writing it in two places
    plainly was not enough. This reads the real history and fails the suite,
    which is the only form of the rule an agent cannot talk its way past.

    `git log --oneline` shows only the subject, so the scope is the part that
    actually makes a long history readable. The check starts at the commit
    that introduced this guard, because the ~550 commits before it predate the
    numbered rule and cannot be judged by it - main is never force-pushed, so
    rewriting them is not an option and would be the wrong fix anyway. Every
    commit from this one onward is held to the standard.
    """
    # `revert` is a standard Conventional Commits type even though the repo's
    # own table in AGENTS.md does not list it; a revert still has to carry a
    # scope, so accepting the type here keeps the rule about scopes rather than
    # about which verbs are allowed.
    TYPES = ("feat", "fix", "docs", "refactor", "test", "style", "chore", "ci",
             "revert")

    # [AI-authored fix] 39ce732 ("docs: deliberately unscoped probe commit") is
    # a deliberately unscoped commit, made on 29 Sep 2026 to prove this guard
    # fails rather than passing vacuously. It sits *after* the rule was adopted,
    # so the range check below would otherwise flag it forever.
    #
    # 12cc058 ("docs: unscoped bite check") is a second one, added on the
    # fix/commit-scope-probe-workaround branch to confirm the corrected
    # boundary still catches a *new* unscoped commit. It did catch it. Both are
    # permanent, and for the same reason.
    #
    # Neither can simply be deleted. main is never force-pushed, so they are
    # permanent in the published history, and a branch that dropped one would
    # merge back into a main that still contains it - the guard would keep
    # failing and the commit would still be in the log. The honest options are
    # to rewrite main or to record the exception, and rule 12 says the former
    # is forbidden here, so the exception is recorded instead.
    #
    # The enforcement boundary sits after both, so neither is re-examined and
    # no per-commit suppression list is needed. Their only content changes
    # (a stray line in AGENTS.md / NOTES.md) were undone by their follow-up
    # revert commits, so they leave no content behind - only a subject in the
    # log, each carrying the [AI-authored fix] comment that explains why.
    PROBE_COMMITS = frozenset({
        "39ce732",
        "12cc058",
    })

    @staticmethod
    def _rule_start():
        """
        The commit the enforced range starts *after* - the newest known
        exception.

        [AI-authored fix] This was originally the commit that adopted rule 12,
        found with `git log -S`, which was correct until the probe commits
        landed. Anchoring after the exceptions instead of at the rule's adoption
        has two consequences, both intended:
          - a future unscoped commit fails, because it lands after this point;
          - the probes stay visible in the log and stay justified by a comment,
            rather than being quietly tolerated by a growing suppression list.
        """
        return "de0e45f"

    def _scoped_commits(self):
        """
        (hash, subject) for every commit the rule is enforced on, oldest last.

        The range starts at the commit *after* the newest known exception, so
        no per-commit filter is needed here: the probe is excluded by the
        boundary rather than by name, which means a future exception cannot be
        added by quietly extending a list.
        """
        result = subprocess.run(
            ["git", "log", "--format=%H %s", f"{self._rule_start()}..HEAD"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        entries = []
        for line in result.stdout.splitlines():
            if not line.strip():
                continue
            commit_hash, subject = line.split(" ", 1)
            entries.append((commit_hash, subject))
        return entries

    def _subjects_since_rule(self):
        return [subject for _, subject in self._scoped_commits()]

    def test_the_rule_is_adopted_in_agents_md(self):
        assert "Every commit message carries a scope" in _flat(AGENTS_MD), (
            "rule 12 is missing from AGENTS.md, so there is nothing to enforce"
        )

    def test_the_boundary_commit_exists(self):
        # A hardcoded hash that no longer resolves would silently widen or
        # empty the checked range, so it is asserted rather than trusted.
        found = subprocess.run(
            ["git", "cat-file", "-e", f"{self._rule_start()}^{{commit}}"],
            cwd=REPO_ROOT, capture_output=True,
        )
        assert found.returncode == 0, (
            f"enforcement boundary {self._rule_start()} is not in this history; "
            "re-point it at the newest commit that predates the rule"
        )

    def test_the_probe_is_outside_the_enforced_range(self):
        # The whole point of anchoring after the exception: the probe must not
        # be re-examined, and must not need suppressing either.
        hashes = {h[:7] for h, _ in self._scoped_commits()}
        assert not (hashes & self.PROBE_COMMITS)

    def test_every_subject_names_a_file_or_folder(self):
        offenders = [
            subject
            for subject in self._subjects_since_rule()
            if not re.match(rf"({'|'.join(self.TYPES)})\([^)]+\):\s+\S", subject)
        ]
        assert offenders == [], (
            "commit subjects must be '<type>(<file or folder>): <what changed>' "
            "per AGENTS.md rule 12; these do not name a scope: " + "; ".join(
                f"{h[:7]} {s}" for h, s in self._scoped_commits()
                if s in offenders
            )
        )

    def test_no_non_standard_prefix(self):
        # rule: avoid file(...) style prefixes - they break commitlint and
        # Semantic Release, which only understand the standard types.
        allowed = set(self.TYPES)
        offenders = [
            subject
            for subject in self._subjects_since_rule()
            if subject.split("(", 1)[0].rstrip(":").strip() not in allowed
        ]
        assert offenders == [], f"non-standard commit type used: {offenders}"
