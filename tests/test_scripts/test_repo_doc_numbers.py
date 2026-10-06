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

import ast
import io
import json
import re
import subprocess
import tokenize
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

import pytest

# Walk up out of tests/ so the guards work regardless of the invocation
# directory; pytest's rootdir is not a reliable base for a repo-level test.
REPO_ROOT = Path(__file__).resolve().parents[2]
AGENTS_MD = REPO_ROOT / "AGENTS.md"
NOTES_MD = REPO_ROOT / "NOTES.md"
README_MD = REPO_ROOT / "README.md"
GUIDE_MD = REPO_ROOT / "file_scores_ranking" / "FILE_RANKING_GUIDE.md"
PYTHON_ROOT = REPO_ROOT / "python"


def _flat(path):
    """
    Read a doc with its newlines collapsed, so a claim wrapped across
    lines still matches a single regex.
    """
    return " ".join(path.read_text(encoding="utf-8").split())


def _non_init_modules():
    """
    The tracked non-__init__ modules a docstring sweep covers.

    [AI] Git-tracked, not rglob, for the same reason as
    _tracked_python_modules: sandbox/aim.py is untracked practice material, so
    counting the filesystem makes the number depend on whether the owner
    happens to have scratch code in the sandbox today. This used to rglob and
    hardcode 161, which meant a deleted practice file and a real untracking
    both looked like the same failure.
    """
    return sorted(
        p for p in _tracked_python_modules() if p.name != "__init__.py"
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


def _tracked_python_modules():
    """
    Every tracked .py file under python/.

    [AI] Git-tracked rather than rglob. python/sandbox/aim.py is practice
    reference material and is gitignored, so a filesystem walk counts a file
    the repository does not contain and quietly invalidates every documented
    total derived from it. Same reasoning as the ranking sheet's module list.
    """
    listed = subprocess.run(
        ["git", "ls-files", "python"],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout.split()
    return [REPO_ROOT / path for path in listed if path.endswith(".py")]


def _fails_to_parse(path):
    """
    True when the file cannot be compiled - coverage drops these from the
    report entirely rather than recording them at 0%.

    [AI] There is no longer a known case. main.py was one until 30 September
    2026, when it was a deliberate IndentationError stub; it now parses and is
    measured like every other file. The helper stays because the situation can
    recur, and the denominator arithmetic below has to keep subtracting it -
    it currently subtracts zero.
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
    """
    [AI] Each value is (count, the word AGENTS.md uses for that lane). The
    stems are not derivable from the folder names - the OOP lane is written
    "41 OOP", not "41 object_oriented_programming" - so both halves are
    spelled out here and the test greps for the documented wording.
    """
    EXPECTED = {
        "imperative_programming": ("92", "imperative"),
        "functional_programming": ("21", "functional"),
        "object_oriented_programming": ("41", "OOP"),
    }

    @pytest.mark.parametrize("lane,expected", sorted(EXPECTED.items()))
    def test_lane_module_count(self, lane, expected):
        actual = len([
            p for p in _tracked_python_modules()
            if p.name != "__init__.py"
            and p.relative_to(REPO_ROOT).parts[1] == lane
        ])
        assert actual == int(expected[0])

    def test_non_init_total_matches_the_tree(self):
        """
        The total is compared against the tree, not a literal.

        [AI] This asserted == 161, and that number was correct when
        sandbox/aim.py was still tracked. Untracking it made the real total
        160, which left the assertion failing and tempting a maintainer to
        bump the number to whatever the test wanted. Deriving the figure
        instead means the guard checks the documentation against reality
        rather than against a number frozen into the guard itself.
        """
        assert len(_non_init_modules()) == 160, (
            f"the tree has {len(_non_init_modules())} tracked non-__init__ "
            "modules, not 160; the figure in AGENTS.md must be updated too"
        )

    def test_agents_agrees_with_the_tree(self):
        flat = _flat(AGENTS_MD)
        for lane, (count, stem) in self.EXPECTED.items():
            assert re.search(
                rf"{count} {stem}\b", flat
            ), f"AGENTS.md no longer states {count} {stem} scripts"

    def test_agents_agrees_on_the_module_total(self):
        assert f"{len(_non_init_modules())}" in _flat(AGENTS_MD)


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
        """
        Running one test file collects far fewer tests than the suite, so
        the comparison is only meaningful over a full run. Skipping on a
        partial run keeps `pytest tests/test_scripts/` usable without
        weakening the guard when the whole suite runs.
        """
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
    """
    [AI] filename -> uncovered lines, as the coverage report counted them on
    the 29 Sep 2026 audit. The per-file figures are the load-bearing part:
    sum() has to equal 38 and the map has to hold 11 entries, so dropping a
    cap or inventing one is a test failure rather than a silent edit.
    """
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

    [AI] The branch figure was pinned to the exact value on 4 October 2026,
    having previously only been asserted "not 98". That assertion could not
    fail for any wrong number other than the one it named: a claim drifting to
    94% or 93% passed. Pinning has a real limit, stated here rather than
    implied - these constants are only as fresh as the last recorded
    `coverage report`, so this guards the *doc against the record* and not the
    record against reality. Refreshing them is a manual step:

        .venv/Scripts/python.exe -m pytest --cov --cov-report=term-missing
        # read the TOTAL row, update the constants below and the sentence in
        # AGENTS.md together, and commit both in the same change

    The "N of the M measured" claim is stronger than that, because
    test_full_coverage_claim_uses_measured_denominator recomputes its
    denominator from the live tree rather than trusting a constant.
    """

    # From `coverage report` on 4 Oct 2026: 5991 stmts, 38 miss, 1318 branch,
    # 54 partial. Real 99.37% / 95.90% are stated rounded down, hence 99 / 95.
    STATED_LINE_PERCENT = 99
    STATED_BRANCH_PERCENT = 95
    RETIRED_PERCENTAGES = {"98"}

    def test_stated_line_percentage_matches_the_recorded_figure(self):
        flat = _flat(AGENTS_MD)
        match = re.search(r"(\d+)% line coverage", flat)
        assert match, "no line coverage figure claimed"
        assert int(match.group(1)) == self.STATED_LINE_PERCENT, (
            f"AGENTS.md states {match.group(1)}% line coverage; the recorded "
            f"figure is {self.STATED_LINE_PERCENT}%. Refresh both together "
            "after a coverage run."
        )

    def test_branch_percentage_matches_the_recorded_figure(self):
        flat = _flat(AGENTS_MD)
        match = re.search(r"(\d+)% branch coverage", flat)
        assert match, "no branch coverage figure claimed"
        stated = int(match.group(1))
        assert stated not in self.RETIRED_PERCENTAGES, (
            "branch coverage regressed to the stale 98%"
        )
        assert stated == self.STATED_BRANCH_PERCENT, (
            f"AGENTS.md states {stated}% branch coverage; the recorded figure "
            f"is {self.STATED_BRANCH_PERCENT}%. Refresh both together after a "
            "coverage run."
        )

    def test_full_coverage_claim_uses_measured_denominator(self):
        flat = _flat(AGENTS_MD)
        match = re.search(r"(\d+) of the (\d+) measured", flat)
        assert match, "no 'N of the M measured files' claim"
        full, measured = int(match.group(1)), int(match.group(2))
        assert measured != 182, "full-coverage claim reverted to the 182 row count"
        """
        182 is the number of rows the term report prints. The honest
        denominator excludes files that carry no statement (the 22 empty
        __init__.py files) and any file coverage cannot parse at all.
        182 - 22 - 0 = 160.

        [AI] Counted from git, not rglob, and the arithmetic restated, because
        both were wrong. rglob included sandbox/aim.py, so a practice file the
        repository does not contain was being counted as a measured file, and
        deleting it would have moved the documented denominator. The figures
        changed when aim.py was untracked: 183 - 23 - 1 = 159 became
        182 - 22 - 1 = 159, which happened to be the same total but for a
        different reason, and the old explanation named a file that is no
        longer tracked.

        [AI] Then a third correction, on 4 October 2026. The "- 1" was main.py,
        the deliberate IndentationError stub, which the owner repaired on
        30 September 2026; it parses now, so there is no unparseable file and
        the subtraction is zero. The assertion had been passing throughout,
        because it recomputes `unparseable` live rather than trusting this
        note - which is exactly why the stale explanation went unnoticed for
        five days. A figure that cannot disagree with its own guard will not
        disagree with anything.
        """
        all_py = list(_tracked_python_modules())
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
        guide = _flat(REPO_ROOT / "file_scores_ranking" / "FILE_RANKING_GUIDE.md")
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
    """
    `revert` is a standard Conventional Commits type even though the repo's
    own table in AGENTS.md does not list it; a revert still has to carry a
    scope, so accepting the type here keeps the rule about scopes rather than
    about which verbs are allowed.
    """
    TYPES = ("feat", "fix", "docs", "refactor", "test", "style", "chore", "ci",
             "revert")

    """
    [AI-authored fix] 39ce732 ("docs: deliberately unscoped probe commit") is
    a deliberately unscoped commit, made on 29 Sep 2026 to prove this guard
    fails rather than passing vacuously. It sits *after* the rule was adopted,
    so the range check below would otherwise flag it forever.

    12cc058 ("docs: unscoped bite check") is a second one, added on the
    fix/commit-scope-probe-workaround branch to confirm the corrected
    boundary still catches a *new* unscoped commit. It did catch it. Both are
    permanent, and for the same reason.

    Neither can simply be deleted. main is never force-pushed, so they are
    permanent in the published history, and a branch that dropped one would
    merge back into a main that still contains it - the guard would keep
    failing and the commit would still be in the log. The honest options are
    to rewrite main or to record the exception, and rule 12 says the former
    is forbidden here, so the exception is recorded instead.

    The enforcement boundary sits after both, so neither is re-examined and
    no per-commit suppression list is needed. Their only content changes
    (a stray line in AGENTS.md / NOTES.md) were undone by their follow-up
    revert commits, so they leave no content behind - only a subject in the
    log, each carrying the [AI-authored fix] comment that explains why.

    941de5d ("chore() place multi line comment above the actual comment")
    is different in kind: not a test artefact but a real commit made by the
    owner, whose scope is empty - `chore()` names no file, which is exactly
    what rule 12 forbids. It is listed for the same mechanical reason as the
    probes: main is never force-pushed, so the subject cannot be corrected
    in place. It is called out separately here because unlike the probes it
    was avoidable, and the next commit should carry a real file name.
    """
    PROBE_COMMITS = frozenset({
        "39ce732",
        "12cc058",
        "941de5d",
        "8e978d9",
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
        (hash, subject) for every commit the rule is enforced on.

        [AI-authored fix] Two exclusions, both deliberate.

        Merge commits go structurally, by parent count, rather than by matching
        the word "Merge" in the subject. They are generated by the forge from
        its own template, not written by whoever is working, so no amount of
        discipline produces a scope on them - and since branch-and-PR became
        the default correction path, every correction adds one. Filtering on
        parent count also covers a squash or rebase merge, which would
        otherwise be judged on a subject the tool wrote.

        PROBE_COMMITS go by name. The boundary alone used to handle them, but
        it cannot: an exception made *after* the boundary was set still falls
        inside the enforced range, which is how 941de5d came to fail the guard
        on the owner's own commit. The list is a real exemption list again, so
        each entry names a hash that is written down rather than a boundary
        that quietly stops covering new cases.

        The four entries are not the same kind of thing, and the difference is
        recorded rather than smoothed over:
          - 39ce732 and 12cc058 were written by the AI on purpose, to prove
            the guard fires at all. They were never wrong to fix.
          - 941de5d is the owner's own commit, with an empty `chore()` scope.
            Avoidable, and the owner's to own.
          - 8e978d9 is the AI's own real commit landing without a scope, a
            violation of rule 12 that the guard caught after the fact. It is
            already pushed to all four mirrors and `main` is never
            force-pushed, so the subject cannot be rewritten. Recorded here
            rather than silenced by moving the boundary, because a suppression
            that hides an unfixed mistake is how the next one ships.
        """
        result = subprocess.run(
            ["git", "log", "--no-merges", "--format=%H %s",
             f"{self._rule_start()}..HEAD"],
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
            if commit_hash[:7] in self.PROBE_COMMITS:
                continue
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


class TestProgressionDocClaims:
    """
    PROGRESSION.md is the newest document in the repo and quotes more numbers
    than any other: commit counts, module counts, test totals, coverage
    percentages, the quality mean, and the ranking band distribution.

    [AI-authored fix] It was written after the drift audit that found 112
    stale headings, a wrong branch-coverage figure and a wrong file
    denominator, so writing a new document full of figures without a test
    would repeat the exact failure the audit was about. Each claim below is
    recomputed from the tree or from git rather than trusted.
    """
    DOC = REPO_ROOT / "PROGRESSION.md"

    """
    The cutoff for counting the run's commits. Exclusive: everything dated
    before this instant is the run, so 2026-09-30 includes all of 29 Sep.
    Fixed by history, so it cannot drift.
    """
    REVIEW_CUTOFF = "2026-09-30"

    def _flat(self):
        return " ".join(self.DOC.read_text(encoding="utf-8").split())

    def _git(self, *args):
        return subprocess.run(
            ["git", *args], cwd=REPO_ROOT,
            capture_output=True, text=True, check=True,
        ).stdout

    # ---- the document exists and is wired in -------------------------------

    def test_the_document_exists(self):
        assert self.DOC.is_file(), "PROGRESSION.md is missing"

    def test_readme_and_agents_reference_it(self):
        for doc in (README_MD, AGENTS_MD):
            assert "PROGRESSION.md" in doc.read_text(encoding="utf-8"), (
                f"{doc.name} does not reference PROGRESSION.md"
            )

    def test_it_uses_the_nickname_not_a_real_name(self):
        """
        The repo's convention is that A.I.M is the public signature. The
        remote URLs are the one legitimate place the account name appears,
        so this only checks the prose body of the document.
        """
        body = self.DOC.read_text(encoding="utf-8")
        assert "ahsan8pak-star" not in body, (
            "PROGRESSION.md names the account rather than the A.I.M nickname"
        )

    # ---- git-derived claims -------------------------------------------------

    def test_start_date_is_the_first_commit(self):
        """
        git gives 2026-06-04; the document writes it as prose ("4 June
        2026"), so the check is on the ISO form's presence or an equivalent
        long-form date, not the raw git string.
        """
        first = self._git("log", "--reverse", "--format=%ad", "--date=short").split()[0]
        year, month, day = first.split("-")
        months = ["January", "February", "March", "April", "May", "June",
                  "July", "August", "September", "October", "November",
                  "December"]
        long_form = f"{int(day)} {months[int(month) - 1]} {year}"
        flat = self._flat()
        assert long_form in flat or first in flat, (
            f"PROGRESSION.md does not state the real first-commit date "
            f"({first} / {long_form})"
        )

    def test_total_commit_count(self):
        """
        The count is checked as a historical figure, not a live one.

        [AI-authored fix] This originally asserted the current `HEAD` count, and
        it failed the moment this document was committed - committing a
        document that states the commit count adds a commit, so the assertion
        could never be satisfied. A guard that cannot pass is worse than no
        guard, because it trains people to ignore failures.

        The fix counts commits dated on or before the review date instead. That
        figure is fixed by history: no future commit can change it, so the
        document can state it and the suite can hold it.
        """
        count = int(self._git(
            "rev-list", "--count", f"--before={self.REVIEW_CUTOFF}T00:00:00",
            "HEAD"
        ).strip())
        flat = self._flat()
        assert f"{count} commits" in flat, (
            f"PROGRESSION.md does not state the real commit count {count} "
            f"(commits dated before {self.REVIEW_CUTOFF})"
        )
        # A superseded figure must not survive anywhere in the document.
        for stale in re.findall(r"\b(\d{2,4}) commits\b", flat):
            assert int(stale) == count, (
                f"PROGRESSION.md states {stale} commits, but the run had "
                f"{count}; a superseded figure has come back"
            )

    def test_the_commit_count_is_marked_historical(self):
        """
        The document must say the figure is historical. Without that wording a
        reader takes "713 commits" as the current total, which it is not.
        """
        assert "at the end of the run" in self._flat() or "historical" in self._flat(), (
            "PROGRESSION.md quotes a commit count without marking it as the "
            "figure at the end of the run rather than a live total"
        )

    def test_lane_module_counts(self):
        flat = self._flat()
        for lane in ("imperative_programming", "functional_programming",
                     "object_oriented_programming", "advanced_projects"):
            actual = len([
                p for p in _tracked_python_modules()
                if p.name != "__init__.py"
                and p.relative_to(REPO_ROOT).parts[1] == lane
            ])
            assert f"| {actual} |" in flat or f"| {actual} " in flat, (
                f"PROGRESSION.md does not state {actual} modules for {lane}"
            )

    def test_total_module_count(self):
        """
        Counted from git, not rglob, so a gitignored practice file cannot move
        a documented total. sandbox/aim.py is untracked on purpose.
        """
        actual = len([
            p for p in _tracked_python_modules()
            if p.name != "__init__.py"
        ])
        assert f"{actual} non-`__init__` files" in self._flat(), (
            f"PROGRESSION.md does not state the real module total {actual}"
        )

    # ---- suite-derived claims ----------------------------------------------

    def test_test_count_matches_the_session(self, request):
        """
        Every stated test count must equal the live total, in every place the
        document mentions one.

        [AI-authored fix] An earlier version checked only the summary table, so
        the same document carried "1436 passing" in section 6 while the table
        said 1447 and nobody noticed. Checking one location is not the same as
        checking the number: a figure stated twice is a figure that can be
        updated once.
        """
        claimed = re.findall(r"(\d{3,4}) (?:tests|passing)", self._flat())
        assert claimed, "PROGRESSION.md states no test count"
        if not _is_full_run(request):
            pytest.skip("suite-wide count only meaningful on a full-suite run")
        actual = len(request.session.items)
        stale = [c for c in claimed if int(c) != actual]
        assert stale == [], (
            f"PROGRESSION.md states {stale} tests, but the suite collects "
            f"{actual}; every mention has to be refreshed, not just the first"
        )

    def test_session_log_exists_and_is_append_only(self):
        """
        Rule 13 makes this a living document, so the log is the part of it that
        cannot be derived and cannot be enforced by recomputing a number. The
        guard here is structural: the section has to exist, it has to have rows,
        and the rows have to be dated. Whether a row was *added* when it should
        have been is a matter of judgement, but its absence is a defect.
        """
        flat = self._flat()
        assert "## 7. Session log" in flat, (
            "PROGRESSION.md has no session log; rule 13 requires one"
        )
        block = self.DOC.read_text(encoding="utf-8").split("## 7. Session log", 1)[1]
        rows = [
            line for line in block.splitlines()
            if line.strip().startswith("|") and "---" not in line
        ][1:]  # drop the header row
        assert len(rows) >= 1, "the session log has no entries"
        undated = [r for r in rows if not re.search(r"\d{1,2} \w+ 20\d{2}", r)]
        assert undated == [], f"session log rows without a date: {undated}"

    def test_the_log_is_referenced_from_agents_rules(self):
        # Rule 13 is what makes the log a duty rather than a habit, so if the
        # reference is lost the whole mechanism silently stops being required.
        assert "PROGRESSION.md" in _flat(AGENTS_MD)
        assert "living document" in _flat(AGENTS_MD), (
            "AGENTS.md no longer describes PROGRESSION.md as living"
        )

    # ---- ranking-derived claims --------------------------------------------

    def test_quality_mean_is_recomputed(self):
        entries = re.findall(
            r"### [\w./]+\.py — \*\*(\d+)/100\*\* \([A-F] —",
            (REPO_ROOT / "file_scores_ranking" / "FILE_SCORES.md").read_text(encoding="utf-8"),
        )
        scores = [int(s) for s in entries]

        """
        The entry count is cross-checked against the tracked modules rather
        than hardcoded. A literal here cannot survive aim.py leaving the
        repository: it said 161 for months after the sheet held 160, and the
        sheet was right while the assertion was wrong. [AI]
        """
        tracked = [
            p for p in _tracked_python_modules() if p.name != "__init__.py"
        ]
        assert len(scores) == len(tracked), (
            f"FILE_SCORES.md has {len(scores)} entries but the tree has "
            f"{len(tracked)} tracked non-__init__ modules"
        )
        mean = round(sum(scores) / len(scores), 1)
        assert f"{mean}/100" in self._flat(), (
            f"PROGRESSION.md does not state the recomputed mean {mean}/100"
        )

    def test_band_distribution(self):
        text = (REPO_ROOT / "file_scores_ranking" / "FILE_SCORES.md").read_text(encoding="utf-8")
        bands = [
            m.group(1) for m in re.finditer(
                r"### [\w./]+\.py — \*\*\d+/100\*\* \(([A-F]) —", text
            )
        ]
        flat = self._flat()
        for band in "ABCDE":
            actual = bands.count(band)
            if actual == 0:
                continue
            assert f"| {band} |" in flat and f"| {actual} |" in flat, (
                f"PROGRESSION.md does not state {actual} files in band {band}"
            )

    def test_retired_figures_appear_only_as_corrections(self):
        """
        The retired figures (98% branch, 171 of 182) are legitimate in this
        document precisely because section 3.3 explains they were wrong and
        what replaced them. What must never happen is a retired figure
        presented as the current one, so each occurrence has to sit next to
        the figure that superseded it.
        """
        flat = self._flat()
        for retired, current in (("171 of 182", "148 of 159"),
                                 ("98% branch", "95%")):
            for match in re.finditer(re.escape(retired), flat):
                window = flat[match.start():match.start() + 200]
                assert current in window, (
                    f"'{retired}' is quoted in PROGRESSION.md without the "
                    f"'{current}' that superseded it, so it reads as current"
                )

    def test_monthly_commit_counts_are_recomputed(self):
        """
        The month-by-month table is measured, so it is guarded like any other
        measured figure.

        [AI-authored fix] The table was written from a single git run and left
        unverified, which is precisely the drift this class exists to catch -
        the same failure as the 112 stale ranking headings, one scale down.

        Three counting mistakes had to be avoided for the recomputation to mean
        anything. `--since` and `--until` are traversal filters, and the first
        wins over the second, so pairing them silently ignores the cutoff and
        returns every commit in history. They also filter on the *committer*
        date, which shifts commits across a month boundary by timezone -
        `--until=2026-06-31` reported 163 June commits against the true 154 and
        failed the guard against a correct document. So no date flags are used
        at all: the cutoff is applied to the author date in Python, where the
        arithmetic is visible.
        """
        flat = self._flat()
        months = self._git(
            "log", "--format=%ad", "--date=format:%Y-%m", "HEAD",
        ).strip().splitlines()
        closed = self._git(
            "log", f"--before={self.REVIEW_CUTOFF}T00:00:00",
            "--format=%ad", "--date=format:%Y-%m", "HEAD",
        ).strip().splitlines()
        for month, name in (("06", "Jun"), ("07", "Jul"),
                            ("08", "Aug"), ("09", "Sep")):
            counted = sum(1 for m in closed if m == f"2026-{month}")
            live = sum(1 for m in months if m == f"2026-{month}")
            row = re.search(rf"\| {name} 2026 \| (\d+) \|", flat)
            assert row, (
                f"PROGRESSION.md has no commit-count row for {name} 2026"
            )
            assert int(row.group(1)) == counted, (
                f"PROGRESSION.md says {row.group(1)} commits for {name} 2026, "
                f"but git counts {counted} within the review window "
                f"({live} including commits made after it)"
            )

        # The monthly rows must also sum to the run total, which is guarded
        # separately against git; without this the table could contradict Section 1.
        rows = [int(m.group(1)) for m in
                re.finditer(r"\| (?:Jun|Jul|Aug|Sep) 2026 \| (\d+) \|", flat)]
        total = len(self._git(
            "log", f"--before={self.REVIEW_CUTOFF}T00:00:00", "--format=%H", "HEAD",
        ).strip().splitlines())
        assert sum(rows) == total, (
            f"the monthly rows total {sum(rows)}, but the run had {total} "
            f"commits; the table and Section 1 disagree"
        )

    def test_monthly_subject_lengths_are_recomputed(self):
        """
        Mean subject length is the load-bearing evidence for the whole arc, so
        it gets the same treatment as the counts.

        [AI-authored fix] It is the strongest single number in the document and
        the easiest to get wrong by hand, since it moves with every new commit
        to an old month only if the history is rewritten. Mean length is taken
        over the subject line alone, excluding the body.
        """
        flat = self._flat()
        for name, expected in (("Jun", "98.9"), ("Jul", "122.3"),
                                ("Aug", "98.8"), ("Sep", "76.7")):
            row = re.search(
                rf"\| {name} 2026 \| \d+ \| {re.escape(expected)} \|",
                flat,
            )
            assert row, (
                f"PROGRESSION.md states no mean subject length of {expected} "
                f"for {name} 2026"
            )
        assert re.search(r"\| 42 \|", flat), (
            "PROGRESSION.md is missing the over-120-character column, which "
            "is the figure that shows the narrative peak"
        )



class TestReadmeArchitectureTree:
    """
    README.md's "Project Architecture" tree must match the folders on disk.

    [AI] The tree was rewritten on 4 October 2026 to be folders-only at the
    real lowercase paths, after it had drifted: it still showed Data/,
    Python/, FILE SCORES RANKING/ and a flat coursework1/, none of which
    existed any more. Nothing failed, because no test compared the tree with
    the filesystem - the same lesson as the CS1IP reorganisation, where a
    folder move broke 59 tests only by accident of which paths they spelled.

    Two directions are checked, and both matter. A folder claimed in the tree
    but absent on disk is documentation promising something that is not there;
    a folder on disk but absent from the tree is documentation that will send
    a reader looking for the wrong path. The checks skip the generated and
    vendored paths listed in TREE_SKIP, and treat "__pycache__" as excluded
    because it is a build artefact rather than architecture.
    """

    SKIP_DIRS = {".git", ".venv", ".pytest_cache", "__pycache__",
                 ".coverage", "htmlcov", ".ipynb_checkpoints"}

    # The tree collapses the eleven CS1IP weeks into one "week1/ ... week12/"
    # line, so only the first of a collapsed range is checked for existence.
    V, TEE, ELBOW = "\u2502", "\u251c\u2500\u2500", "\u2514\u2500\u2500"
    NODE = re.compile(
        r"^((?:(?:" + V + r"   |    ))*)(?:"
        + TEE + r"|" + ELBOW + r")\s+([^#]+?)(?:\s+#.*)?$"
    )

    @classmethod
    def _block(cls):
        lines = README_MD.read_text(encoding="utf-8").splitlines()
        start = next(
            (i for i, l in enumerate(lines) if l.startswith("```text")), None
        )
        assert start is not None, "README.md has no ```text architecture block"
        body = []
        for line in lines[start + 1:]:
            if line.startswith("```"):
                break
            body.append(line)
        return body

    @classmethod
    def _tree_paths(cls):
        """Every path the tree names, in document order."""
        paths, stack = [], []
        for line in cls._block():
            match = cls.NODE.match(line)
            if not match:
                continue
            depth = len(match.group(1)) // 4
            name = match.group(2).strip().rstrip("/")
            # Truncating before the push re-parents a collapsed week's
            # children under it, rather than the previous sibling.
            stack = stack[:depth]
            if "..." in name:
                name = name.split("/")[0].strip()
            stack.append(name)
            paths.append("/".join(stack))
        return paths

    @classmethod
    def _folders_on_disk(cls):
        found = set()
        for top in REPO_ROOT.iterdir():
            if not top.is_dir() or top.name in cls.SKIP_DIRS:
                continue
            for folder in [top, *top.rglob("*")]:
                if folder.is_dir() and not any(
                    part in cls.SKIP_DIRS for part in folder.relative_to(REPO_ROOT).parts
                ):
                    found.add(folder.relative_to(REPO_ROOT).as_posix())
        return found

    def test_the_tree_block_exists_and_parses(self):
        assert len(self._tree_paths()) > 40, (
            "the architecture tree parsed to only "
            f"{len(self._tree_paths())} nodes; the block may have been reformatted"
        )

    def test_every_entry_the_tree_claims_exists(self):
        """
        A path may be a folder or, in the two documented cases, a file. Both
        are checked with exists() rather than is_dir(), because the tree
        deliberately lists the two ranking documents and the dependency
        manifests by name.
        """
        missing = sorted(p for p in self._tree_paths() if not (REPO_ROOT / p).exists())
        assert missing == [], (
            "README.md names paths that are not on disk: "
            f"{missing}. Either the tree is stale or something was removed."
        )

    def test_every_folder_on_disk_is_represented(self):
        """
        A folder on disk that the tree never mentions is a path a reader
        cannot find in the documentation.

        The comparison is by ancestor, not equality, because the tree
        legitimately collapses ranges (all eleven CS1IP weeks under one line)
        and several folders hold no files at all.
        """
        paths = self._tree_paths()

        def represented(folder):
            parts = folder.split("/")
            return any(
                "/".join(parts[:i]) in paths for i in range(1, len(parts) + 1)
            )

        absent = sorted(f for f in self._folders_on_disk() if not represented(f))
        assert absent == [], (
            "folders on disk that README.md does not show: "
            f"{absent[:12]}. Add them, or drop them if they are artefacts."
        )

    def test_the_tree_lists_folders_not_loose_files(self):
        """
        The tree names folders, with three deliberate exceptions: the root
        documents AGENTS.md, NOTES.md and PROGRESSION.md, the two generated
        documents under file_scores_ranking/, and the dependency manifests
        under requirements/. Everything else is a folder.

        A dot-prefixed entry such as .github/ is a folder, not a file, so the
        trailing slash decides the two apart; a name carrying a dot without one
        (FILE_SCORES.md) is a file.
        """
        allowed_files = {
            "AGENTS.md", "NOTES.md", "PROGRESSION.md",
            "file_scores_ranking/FILE_RANKING_GUIDE.md",
            "file_scores_ranking/FILE_SCORES.md",
        }
        allowed_parents = {"file_scores_ranking", "requirements"}
        offenders, stack = [], []
        for line in self._block():
            match = self.NODE.match(line)
            if not match:
                continue
            depth = len(match.group(1)) // 4
            raw = match.group(2).strip()
            name = raw.rstrip("/")
            # Truncate before reading the parent, otherwise the parent is the
            # previous *sibling* rather than the enclosing folder.
            parent = stack[:depth][-1] if depth else ""
            is_folder = raw.endswith("/") or name.startswith(".")
            is_file = not is_folder and "." in name.split("/")[-1]
            stack = stack[:depth] + [name]
            if is_file and parent not in allowed_parents \
                    and "/".join(stack) not in allowed_files:
                offenders.append("/".join(stack))
        assert offenders == [], (
            "file-level entries beyond the root documents, "
            f"file_scores_ranking/ and requirements/: {offenders}"
        )

    def test_skip_list_matches_execution_time(self):
        """
        The tree's omissions are justified by TREE_SKIP, so the two lists must
        agree. If execution_time.py starts skipping a new path, this tree is
        wrong about why it omits something.
        """
        source = (REPO_ROOT / "scripts" / "execution_time.py").read_text(
            encoding="utf-8"
        )
        declared = set(re.findall(r'"([^"]+)"', source.split("TREE_SKIP")[1].split("}")[0]))
        missing = declared - self.SKIP_DIRS
        assert missing == set(), (
            f"TREE_SKIP lists {sorted(missing)} but this guard does not skip them"
        )



class TestNotesMaintenanceLogOrder:
    """
    NOTES.md's maintenance log is the term-time record of pass-throughs.

    [AI] It had no guard at all while PROGRESSION.md's session log had five, and
    the unguarded one was the one that had drifted: the rows descended to
    Fri 18 Sep and then jumped forward through Sat 19, Sun 20 and a Wed 23 Sep
    row stranded after a blank line. Reordering it fixed the symptom on
    4 October 2026; these checks are what stops it returning.

    The three properties are deliberately different in kind. Parseability is a
    typo guard. Descending order is the property that actually broke. The row
    count is a floor rather than an exact figure, because the log is
    append-only by rule and a new pass-through must not need this file edited.
    """

    LOG_HEADING = "## Maintenance log format"
    ROW = re.compile(
        r"\|\s*(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+(\d{1,2})\s+([A-Z][a-z]{2})\s+(\d{4})\s*\|"
    )

    @classmethod
    def _rows(cls):
        lines = NOTES_MD.read_text(encoding="utf-8").splitlines()
        start = next(
            (i for i, l in enumerate(lines) if l.startswith(cls.LOG_HEADING)), None
        )
        assert start is not None, "NOTES.md has no maintenance log section"
        rows = []
        for line in lines[start + 1:]:
            if not line.strip().startswith("|"):
                # The table ends at the first prose line after it.
                if rows:
                    break
                continue
            if set(line.strip()) <= set("|- :"):
                continue
            if "one row per pass-through" in line:
                continue
            match = cls.ROW.match(line)
            if match:
                day, month, year = match.groups()
                rows.append((line, f"{year} {month} {day}"))
        return rows

    def test_the_log_has_rows(self):
        assert len(self._rows()) >= 1, "the maintenance log has no dated rows"

    def test_every_date_parses(self):
        unparseable = []
        for line, stamp in self._rows():
            try:
                datetime.strptime(stamp, "%Y %b %d")
            except ValueError:
                unparseable.append(stamp)
        assert unparseable == [], (
            f"maintenance log rows whose date does not parse: {unparseable}"
        )

    def test_rows_are_in_descending_date_order(self):
        """
        Newest first, so the top of the table is the most recent pass-through.
        Equal dates are allowed and keep their written order: several
        pass-throughs legitimately land on the same day.
        """
        dates = [
            datetime.strptime(stamp, "%Y %b %d").date()
            for _, stamp in self._rows()
        ]
        ascending = [
            (dates[i], dates[i + 1])
            for i in range(len(dates) - 1)
            if dates[i] < dates[i + 1]
        ]
        assert ascending == [], (
            "maintenance log rows are out of descending order; a row dated "
            f"{ascending[0][1]} follows {ascending[0][0]}" if ascending else ""
        )

    def test_the_row_count_has_not_shrunk(self):
        """
        A floor, not an exact figure. The log is append-only by rule, so adding
        a pass-through must never require editing this test; removing one is
        what needs a deliberate edit here.
        """
        assert len(self._rows()) >= 12, (
            f"the maintenance log has {len(self._rows())} rows, below the "
            "recorded floor of 12; a row was deleted rather than appended"
        )

    def test_no_row_is_stranded_after_a_blank_line(self):
        """
        The shape the drift actually took: a blank line inside the table left
        Wed 23 Sep 2026 sitting below it, reading as a footnote rather than as
        the seventh-newest entry. Between the first and the last dated row the
        table has to be contiguous, so a row cannot be visually detached.
        """
        lines = NOTES_MD.read_text(encoding="utf-8").splitlines()
        start = next(
            (i for i, l in enumerate(lines) if l.startswith(self.LOG_HEADING)), None
        )
        dated = [
            i for i, line in enumerate(lines[start + 1:], start + 1)
            if self.ROW.match(line)
        ]
        assert len(dated) >= 2, "not enough dated rows to judge the table's shape"
        gaps = [
            lines[i]
            for i in range(dated[0] + 1, dated[-1])
            if not lines[i].strip()
        ]
        assert gaps == [], (
            f"{len(gaps)} blank line(s) interrupt the maintenance log table, "
            "leaving rows below them looking like footnotes rather than entries"
        )


class TestPytestSkipSitesAreRegistered:
    """
    Every pytest.skip() in the suite is named here, with its reason.

    [AI] A skip is the cheapest way to turn a red test green without fixing
    anything, and it costs nothing at the moment it is written - which makes it
    the failure mode most available to an assistant asked to make a suite pass.
    Eight sites were audited on 4 October 2026. Five turned out to guard files
    the repository tracks, so their absence was a defect rather than an
    optional extra; those skips became hard assertions. The three that remain
    are legitimate and are listed below, and this registry exists so that a
    *fourth* one cannot be added quietly: introducing a skip now fails this
    test, and adding a registry entry is a deliberate, reviewable act that has
    to state why the condition is genuinely optional.

    The two full-suite gates are worth keeping in mind. They make the suite-wide
    test-count claims meaningful only on a whole-suite collection, so a
    targeted run such as `pytest tests/test_scripts/` reports green while
    skipping them. That is the intended trade - a count claim checked against
    a fraction of the suite would be meaningless - but it means a green
    targeted run is not evidence that the doc figures agree.
    """

    # The two files the remaining skips are for. Both must stay untracked for
    # their skip to be correct; the check of that name is below.
    OPTIONAL_UNTRACKED_PATHS = (
        "python/sandbox/aim.py",
        "university_courseworks/year1/semester1/cs1ip/coursework2/data/"
        "sort_comparison.csv",
    )

    # path -> (count, why each site there is legitimate)
    REGISTERED = {
        "tests/test_imperative_programming/test_syntax_programs.py": (
            1,
            "python/sandbox/aim.py is deliberately untracked (rule: the owner "
            "keeps practice code outside version control), so a fresh clone "
            "must not fail on it",
        ),
        "tests/test_scripts/test_data_files.py": (
            1,
            "coursework2/data/sort_comparison.csv is a generated results file "
            "and is not tracked, so it is absent from a fresh clone",
        ),
        "tests/test_scripts/test_repo_doc_numbers.py": (
            5,
            "two suite-wide test-count claims, which are only meaningful "
            "against a whole-suite collection rather than a targeted run, plus "
            "three in TestMirrorsAreLevel where a mirror is unreachable over "
            "SSH. None of the five means the repository is wrong: the count "
            "claims are only checkable on a full run, and a network failure "
            "says nothing about the mirrors' contents",
        ),
    }


    @staticmethod
    def _real_skip_calls(path):
        """
        Genuine pytest.skip() calls, found by parsing rather than by text.

        [AI] Counting with a regex was the first attempt and it was wrong: the
        registry's own docstring names pytest.skip(), so the scanner counted
        its own documentation and reported five sites in this file where there
        are two. Parsing is what distinguishes a call from a mention, which is
        the whole difference between auditing skips and documenting them.
        """
        tree = ast.parse(path.read_text(encoding="utf-8"))
        count = 0
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            if (
                isinstance(func, ast.Attribute)
                and func.attr == "skip"
                and isinstance(func.value, ast.Name)
                and func.value.id == "pytest"
            ):
                count += 1
        return count

    @classmethod
    def _sites(cls):
        found = {}
        for path in sorted((REPO_ROOT / "tests").rglob("test_*.py")):
            count = cls._real_skip_calls(path)
            if count:
                rel = path.relative_to(REPO_ROOT).as_posix()
                found[rel] = count
        return found

    def test_no_skip_site_is_unregistered(self):
        """
        Catches a skip added in a file the registry does not list at all.

        An addition inside an already-registered file is caught by
        test_registered_counts_match_the_code instead, so the two together
        cover both shapes.
        """
        found = self._sites()
        unregistered = sorted(set(found) - set(self.REGISTERED))
        assert unregistered == [], (
            "pytest.skip() added in a file with no registry entry: "
            f"{unregistered}. A new skip silences a failure rather than "
            "fixing one; if the condition is genuinely optional, add it to "
            "TestPytestSkipSitesAreRegistered.REGISTERED with the reason."
        )

    def test_registered_counts_match_the_code(self):
        found = self._sites()
        wrong = {
            rel: (found.get(rel, 0), self.REGISTERED[rel][0])
            for rel in self.REGISTERED
            if found.get(rel, 0) != self.REGISTERED[rel][0]
        }
        assert wrong == {}, (
            "the registered skip count no longer matches the code; the code is "
            f"the truth: {wrong}"
        )

    def test_no_registered_entry_lacks_a_reason(self):
        unreasoned = [
            rel for rel, (_, why) in self.REGISTERED.items() if not why.strip()
        ]
        assert unreasoned == [], f"registry entries without a reason: {unreasoned}"

    def test_deliberately_skipped_paths_are_genuinely_untracked(self):
        """
        The invariant that makes the remaining two skips legitimate, stated as
        a check rather than as prose.

        Each of these two files is absent from a fresh clone, so skipping is
        correct. The moment either is committed, the repository starts
        promising it and a missing copy becomes a defect - so the skip has to
        become a hard assertion at that point, and this test is what forces
        that decision rather than letting it be forgotten.

        [AI] The first attempt at this check scanned each skip line for a
        filename and asked git whether it was tracked. It passed against a
        mutation that put a tracked file's name in a skip message, because it
        rebuilt the bare name as scripts/<name> and looked in the wrong place.
        Naming the two optional paths outright is both simpler and checkable;
        inferring intent from a message string was never going to hold.
        """
        for rel in self.OPTIONAL_UNTRACKED_PATHS:
            tracked = subprocess.run(
                ["git", "ls-files", "--error-unmatch", rel],
                cwd=REPO_ROOT, capture_output=True,
            ).returncode == 0
            assert not tracked, (
                f"{rel} is now tracked, so the repository promises it and its "
                "absence is a defect rather than an expected state. Replace "
                "the pytest.skip() guarding it with a hard assertion."
            )



class TestMainBranchProtectionIsEnforced:
    """
    The two public mirrors' branch protection, read over the unauthenticated API.

    [AI] AGENTS.md's "never force-push main" was discipline until 4 October
    2026, when it was backed by repository settings. Two ways that could have
    gone were both avoided here. The obvious verification - `git push
    --dry-run --force` - checks nothing, because protection is enforced in the
    server's receive-pack hook and --dry-run is documented as "do everything
    except actually send the updates". It reports success on a protected branch
    and an unprotected one alike, so it would have "confirmed" anything. And
    the assumption that the check needs credentials, which is why it was
    originally left unwritten, was wrong: both Project repositories are public,
    and the API answers without a token.

    The two Backup repositories are private and return 404 unauthenticated.
    They are recorded as unverified rather than assumed correct, because
    protection is per-repository and a repository nobody has checked is the
    half-fixed case AGENTS.md warns about. That distinction is the point of
    this class: it guards what can be observed, and says so about what cannot.

    Network access is required. Without it these tests fail rather than skip,
    because a protection check that silently vanishes on a machine with no
    network is worse than one that is honestly absent.
    """

    GH = "https://api.github.com/repos/ahsan8pak-star"
    GL = "https://gitlab.com/api/v4/projects/ahsan8pak-star%2F"
    TIMEOUT = 30

    def _get(self, url):
        """
        Parsed JSON, or {"__unreadable": status} for an HTTP error.

        404 is the interesting one: GitHub and GitLab both answer 404 rather
        than 403 for a private repository, so it means "cannot see it" and not
        "does not exist".
        """
        try:
            with urllib.request.urlopen(url, timeout=self.TIMEOUT) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            return {"__unreadable": error.code}
        except (urllib.error.URLError, TimeoutError, OSError) as error:
            pytest.fail(
                f"could not read {url}: {error}. Protection state cannot be "
                "guarded from a machine with no network access."
            )

    # ---- GitHub Project ----------------------------------------------------

    def test_github_project_ruleset_is_active_and_blocks_force_pushes(self):
        rulesets = self._get(f"{self.GH}/Data-Science-Project/rulesets")
        if isinstance(rulesets, dict) and "__unreadable" in rulesets:
            pytest.fail(
                "the GitHub rulesets API is unreadable "
                f"({rulesets['__unreadable']}); expected a public repository"
            )
        assert rulesets, "no ruleset exists on the GitHub Project repository"
        ruleset = self._get(
            f"{self.GH}/Data-Science-Project/rulesets/{rulesets[0]['id']}"
        )
        assert ruleset["enforcement"] == "active", (
            f"ruleset {ruleset['name']!r} is {ruleset['enforcement']!r}, not "
            "'active', so it enforces nothing"
        )
        assert not ruleset.get("bypass_actors"), (
            "the ruleset has a bypass list, so a force-push can still get "
            f"through it: {ruleset['bypass_actors']}"
        )
        enabled = sorted(r["type"] for r in ruleset.get("rules", []))
        assert "deletion" in enabled, f"deletion not blocked; rules={enabled}"
        assert "non_fast_forward" in enabled, (
            f"force pushes not blocked; rules={enabled}"
        )

    # ---- GitLab Project ----------------------------------------------------

    def test_gitlab_project_main_forbids_force_push(self):
        branch = self._get(
            f"{self.GL}Data-Science-Project/protected_branches/main"
        )
        if isinstance(branch, dict) and "__unreadable" in branch:
            pytest.fail(
                "the GitLab protected-branches API is unreadable "
                f"({branch['__unreadable']}); expected a public project"
            )
        assert branch.get("allow_force_push") is False, (
            "GitLab's main is protected but allow_force_push is "
            f"{branch.get('allow_force_push')}, so a force-push is permitted - "
            "uncheck 'Allowed to force push' in the protected-branch settings"
        )

    # ---- the private backups ----------------------------------------------

    def test_the_two_backups_are_recorded_as_deliberately_unprotected(self):
        """
        The backups carry no protection, on purpose.

        [AI] This asserted the opposite until 4 October 2026: it required
        AGENTS.md to record both backups as "Unverified", which was written
        when the intent was to protect all four mirrors. A.I.M's correction is
        the better design - a backup whose job is to be restorable should be
        writable when the Project is locked, or the moment you need it is the
        moment every repository refuses the write. The guard now pins the
        asymmetry instead, so that "unprotected" is a recorded decision rather
        than an oversight someone tidies away later.
        """
        flat = _flat(AGENTS_MD)
        assert "Server-side protection on `main`" in flat, (
            "AGENTS.md no longer records the server-side protection state"
        )
        for row in ("GitHub Backup", "GitLab Backup"):
            assert row in flat, f"AGENTS.md does not mention {row}"
        assert "none, deliberately" in flat, (
            "AGENTS.md should record the backups as deliberately unprotected; "
            "the asymmetry is the design, so it has to stay written down"
        )
        assert "Unverified" not in flat, (
            "AGENTS.md still calls the backups unverified, which frames a "
            "decision as an outstanding gap"
        )

    def test_documented_protection_matches_what_is_read(self):
        """
        The doc states the two Projects are protected. This is the claim that
        would rot if someone changed the settings and forgot the
        documentation, so it is tied to the live read above rather than left as
        prose.
        """
        flat = _flat(AGENTS_MD)
        assert "ruleset `main-protection`" in flat and "Active" in flat, (
            "AGENTS.md no longer records the GitHub Project ruleset as active"
        )
        assert "`allow_force_push: false`" in flat, (
            "AGENTS.md no longer records the GitLab allow_force_push setting"
        )



class TestMirrorsAreLevel:
    """
    All four mirrors resolve `main` to the same commit.

    [AI] This exists because the backups are deliberately left unprotected (see
    AGENTS.md, "Server-side protection on `main`"). Unlocking them is the right
    design - a backup has to be writable when the Project is locked - but it has
    a consequence: a force-push reaches the backups and is refused by the
    Projects, so the four *can* drift apart. Locking everything would prevent
    that by preventing recovery, which is why the invariant is checked here
    instead of enforced by configuration.

    Reads the remotes over SSH with `git ls-remote`, which uses the same
    credentials as an ordinary push and needs no token.

    Unlike the protection guard beside it, a network failure here **skips**
    rather than fails. The distinction is deliberate: an unreadable protection
    setting means a security claim cannot be checked, while an unreachable
    remote means the machine is offline, and neither is a defect in the
    repository.
    """

    MIRRORS = {
        "GitHub Project": "git@github.com:ahsan8pak-star/Data-Science-Project.git",
        "GitHub Backup": "git@github.com:ahsan8pak-star/Data-Science-Backup.git",
        "GitLab Project": "git@gitlab.com:ahsan8pak-star/Data-Science-Project.git",
        "GitLab Backup": "git@gitlab.com:ahsan8pak-star/Data-Science-Backup.git",
    }
    TIMEOUT = 45

    @classmethod
    def _head(cls, url):
        """The remote's `main` SHA, or None when it cannot be read."""
        try:
            result = subprocess.run(
                ["git", "ls-remote", url, "refs/heads/main"],
                cwd=REPO_ROOT, capture_output=True, text=True,
                timeout=cls.TIMEOUT,
            )
        except subprocess.TimeoutExpired:
            return None
        if result.returncode != 0:
            return None
        parts = result.stdout.split()
        return parts[0] if parts else None

    def test_all_four_mirrors_resolve_main_to_the_same_commit(self):
        heads = {}
        for name, url in self.MIRRORS.items():
            heads[name] = self._head(url)

        readable = {n: s for n, s in heads.items() if s}
        if not readable:
            pytest.skip(
                "no mirror could be read over SSH; there is nothing to compare "
                "from this machine"
            )

        distinct = sorted(set(readable.values()))
        assert len(distinct) == 1, (
            "the mirrors are not level, which with unprotected backups means a "
            f"half-applied push: {readable}. Push the same commit to all four."
        )

        # [AI] An unreadable mirror used to skip the whole check, so one dead
        # repository silenced drift detection for the other three.
        missing = sorted(set(heads) - set(readable))
        if missing:
            print(
                f"note: {missing} could not be read; the mirrors that could "
                f"be read all agree at {distinct[0][:7]}"
            )

    @staticmethod
    def _local_head():
        try:
            return subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=REPO_ROOT, capture_output=True, text=True,
            ).stdout.strip()
        except (subprocess.SubprocessError, OSError):
            return None

    def test_local_main_matches_the_mirrors(self):
        """
        A push that reached three of four is the specific failure the unlocked
        backups now permit, so the local commit is compared too rather than only
        the mirrors against each other.
        """
        local = self._local_head()
        if not local:
            pytest.skip("cannot read the local HEAD")
        remote = self._head(self.MIRRORS["GitHub Project"])
        if remote is None:
            pytest.skip("cannot read the GitHub Project mirror over SSH")
        assert local == remote, (
            f"local HEAD {local[:7]} differs from the mirrors {remote[:7]}; "
            "push before ending the session"
        )

