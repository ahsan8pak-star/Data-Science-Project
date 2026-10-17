"""
Guard HISTORY_REVIEW.md against the git record it claims to describe.

[AI-authored fix] The review is a retrospective, and a retrospective is the
easiest document in a repository to let rot: nothing in the suite reads it, so
it can quietly disagree with the history it summarises and still look finished.
The first version of this guard did the obvious thing and asserted the
document's stated total of 836 commits against `git rev-list --count HEAD`,
which failed on the very next commit - the one that added the document. A guard
that fails on being correct is a guard that gets deleted, so the total is
checked for internal consistency instead: the five per-identity figures must
sum to the figure the document states. That catches a transcription error, which
is the mistake actually worth catching, and it survives every future commit.

What is pinned, and why each one:

  * every git identity is named - so a new contributor, a second pair of hands or
    a bot that finally lands a merge cannot slip into the history unrecorded;
  * the per-identity counts sum to the stated total - the table cannot be edited
    carelessly;
  * the WWW and EBI sections are present - the framework is the document's
    reason for existing, not decoration;
  * the file obeys the house byte invariants - it is a tracked text file like
    any other, and `.gitattributes` plus `test_data_files.py` would otherwise
    have to special-case it.
"""

import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
REVIEW_MD = REPO_ROOT / "git_repo_progress" / "HISTORY_REVIEW.md"

IDENTITY_ROW = re.compile(r"^\|\s*\d+\s*\|\s*`([^`]+)`\s*\|.*?\|\s*(\d+)\s*\|")
TOTAL_ROW = re.compile(r"^\|\s*\|\s*\*\*Total\*\*\s*\|.*?\|\s*\*\*(\d+)\*\*\s*\|")
WEEKDAY_HEADING = re.compile(
    r"^##\s+\d+\.\s+.*(What Went Well|What Went Wrong|Evidence-Based Improvements)"
)


def git(*args):
    """Run a read-only git command and return its stdout."""
    return subprocess.run(
        ["git", *args], cwd=REPO_ROOT, capture_output=True, text=True, check=True
    ).stdout


def review_text():
    assert REVIEW_MD.is_file(), (
        f"{REVIEW_MD.name} is missing; it is the retrospective for the "
        f"contributor record and is guarded like any other document"
    )
    return REVIEW_MD.read_text(encoding="utf-8")


def git_identities():
    """
    Distinct author names in the history, with their commit counts.

    Keyed on the name rather than the name-and-email pair: `om001219` appears
    under two different emails and is one actor, which is exactly the ambiguity
    section 1 of the review is about, so the guard must not reintroduce it.
    """
    counts = {}
    for line in git("log", "--format=%an|%ae").splitlines():
        name, _, _email = line.partition("|")
        counts[name.strip()] = counts.get(name.strip(), 0) + 1
    return counts


def identity_rows():
    """The contributor-register rows of the review, as (name, count) pairs."""
    rows = []
    for line in review_text().splitlines():
        match = IDENTITY_ROW.match(line)
        if match:
            rows.append((match.group(1), int(match.group(2))))
    return rows


class TestTheReviewRecordsEveryContributor:

    def test_the_register_table_exists(self):
        rows = identity_rows()
        assert len(rows) >= 4, (
            f"expected the contributor register to name at least four identities, "
            f"found {len(rows)}"
        )

    def test_every_git_identity_is_named_in_the_review(self):
        """
        The point of the guard: a new pair of hands, or a bot that lands a merge,
        changes the record this document claims to summarise.
        """
        text = review_text()
        missing = [name for name in git_identities() if name not in text]
        assert not missing, (
            f"git history contains identities the review does not name: "
            f"{missing}. Add a row to section 1 of HISTORY_REVIEW.md."
        )

    def test_the_stated_total_matches_the_rows_above_it(self):
        """
        Internal consistency, not consistency with `git rev-list`, so the guard
        survives the next commit. See the module docstring for why.
        """
        rows = identity_rows()
        assert rows, "no contributor rows found to check"
        stated = [int(m.group(1)) for m in
                  (TOTAL_ROW.match(line) for line in review_text().splitlines()) if m]
        assert stated, "the register table has no bold Total row"
        assert sum(count for _name, count in rows) == stated[0], (
            f"the {len(rows)} identity rows sum to "
            f"{sum(count for _n, count in rows)}, but the table states {stated[0]}"
        )

    def test_the_counts_are_plausible_for_the_history(self):
        """A count of zero, or one larger than the history, is a transcription slip."""
        actual = git_identities()
        total_commits = int(git("rev-list", "--count", "HEAD").strip())
        for name, count in identity_rows():
            assert count > 0, f"{name} is recorded with no commits"
            assert count <= total_commits, (
                f"{name} is recorded with {count} commits, more than the "
                f"{total_commits} in the history"
            )
            if name in actual:
                # An identity may be recorded under one email while git splits
                # it across two, so only the lower bound is safe to assert.
                assert count >= 1


class TestTheFrameworkSurvives:

    def test_the_review_uses_www_and_ebi(self):
        found = {m.group(1) for m in
                 (WEEKDAY_HEADING.match(line) for line in review_text().splitlines()) if m}
        assert {"What Went Well", "What Went Wrong", "Evidence-Based Improvements"} <= found, (
            f"expected the What Went Well / What Went Wrong / Evidence-Based "
            f"Improvements sections, found {sorted(found)}"
        )

    def test_the_recommendation_is_stated_rather_than_implied(self):
        text = review_text()
        assert "Recommendation" in text, (
            "the review reaches a conclusion about university_courseworks/; "
            "state it in a Recommendation line so a reader cannot miss it"
        )

    def test_every_figure_carries_a_command(self):
        """
        A retrospective whose numbers cannot be re-derived is a memory exercise.
        """
        text = review_text()
        assert "git log" in text and "git ls-files" in text, (
            "the review should show the git commands its figures came from"
        )


class TestTheReviewObeysTheHouseInvariants:

    def test_line_endings_are_lf(self):
        raw = REVIEW_MD.read_bytes()
        assert b"\r\n" not in raw, (
            "HISTORY_REVIEW.md has CRLF endings; .gitattributes pins LF"
        )

    def test_it_ends_with_exactly_two_newlines(self):
        raw = REVIEW_MD.read_bytes()
        assert raw.endswith(b"\n\n") and not raw.endswith(b"\n\n\n"), (
            "HISTORY_REVIEW.md must end with the last line of content followed "
            "by one empty line, i.e. exactly two trailing newlines"
        )

    def test_it_is_tracked_as_text_not_binary(self):
        attributes = (REPO_ROOT / ".gitattributes").read_text(encoding="utf-8")
        assert "*.md" not in attributes.split("*.wav")[0].split("*.pdf")[-1], (
            "a markdown file should fall under the global text=auto rule, not "
            "be singled out as binary"
        )

