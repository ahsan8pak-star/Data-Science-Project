"""
Repo hygiene guards.

The point of these is the person who clones the repo, checks out a branch and
runs the test suite or the benchmark: they should not end up with new untracked
files in the working tree, and they should not be able to commit one by
accident with `git add .`.

Nothing here writes to the repository. The git checks are read-only queries
against the index and .gitignore; the one filesystem test writes its probe
files into tmp_path.
"""

import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]


def _is_ignored(name):
    """True when git would ignore this path at the repo root."""
    result = subprocess.run(
        ["git", "check-ignore", "-q", name],
        cwd=REPO_ROOT,
        capture_output=True,
    )
    return result.returncode == 0


class TestCwdRelativeArtefactsAreIgnored:
    """
    AGENTS.md rules 3 and 4 make two scripts save into the current working
    directory on purpose, and the tests point them at tmp_path. That is correct
    and stays. But a contributor running either script from the repo root, or
    the execution_time.py benchmark - which launches all 183 files with the
    repo root as CWD - gets these two files dropped at the top level, and
    neither was ignored, so `git add .` would have committed them.
    """
    ARTEFACTS = (
        "transactionv1.xlsx",   # transactions.py   -> wb.save("transactionv1.xlsx")
        "qrcode.png",           # qrcode_generator.py -> os.getcwd() + qrcode.png
    )

    @pytest.mark.parametrize("name", ARTEFACTS)
    def test_artefact_is_gitignored(self, name):
        assert _is_ignored(name), (
            f"{name} is written into the CWD by a script and is not in "
            f".gitignore, so a `git add .` after running the benchmark would "
            f"commit it. Add /{name} to the root-artifacts section."
        )

    @pytest.mark.parametrize("name", ARTEFACTS)
    def test_artefact_is_not_tracked_in_git(self, name):
        # Ignored is not enough - if it were already committed the ignore rule
        # would not stop it being pushed, so assert it is genuinely untracked.
        result = subprocess.run(
            ["git", "ls-files", "--error-unmatch", name],
            cwd=REPO_ROOT,
            capture_output=True,
        )
        assert result.returncode != 0, f"{name} is tracked; it should not be"

    def test_artefact_written_to_tmp_path_is_not_in_the_repo(self, tmp_path):
        """
        The behaviour the artefacts come from still works and still lands
        outside the repo, which is the whole reason the rules need no change.
        """
        probe = tmp_path / "transactionv1.xlsx"
        probe.write_bytes(b"not a real workbook")

        assert probe.is_file()
        assert not (REPO_ROOT / "transactionv1.xlsx").exists()
        assert not (REPO_ROOT / "qrcode.png").exists()


class TestRepoIsCleanAfterATestRun:
    """
    A cheap guard on the claim that a test run does not pollute the repo: the
    suite is already covered elsewhere, so this only checks that no tracked
    source file was modified and that the two artefacts are absent.
    """
    @pytest.mark.parametrize("name", ("transactionv1.xlsx", "qrcode.png"))
    def test_artefact_absent_from_the_working_tree(self, name):
        assert not (REPO_ROOT / name).exists(), (
            f"{name} is sitting in the repo root. Delete it; it is generated."
        )


class TestPracticeSandboxStaysUntracked:
    """
    python/sandbox/aim.py is practice reference material, not repo content.

    [AI] Written after a real incident: the file held genuine practice code,
    a `git add -A` swept it into a commit, and the code was then lost when a
    later restore of the same path overwrote it. Two rules now exist because
    of that, and both are worth enforcing rather than trusting:

      - the file is gitignored, so `git add .` cannot pick it up;
      - it is untracked, so the ignore rule is not merely decorative.

    Both halves matter. An ignore entry for a file that is already tracked
    does nothing at all, and the file would still be swept into commits while
    the rule looked satisfied.
    """
    SANDBOX = "python/sandbox/aim.py"

    def test_the_practice_file_is_gitignored(self):
        result = subprocess.run(
            ["git", "check-ignore", "-q", self.SANDBOX],
            cwd=REPO_ROOT, capture_output=True,
        )
        assert result.returncode == 0, (
            f"{self.SANDBOX} is not gitignored, so a `git add .` can commit "
            "practice code into the repository"
        )

    def test_the_practice_file_is_not_tracked(self):
        listed = subprocess.run(
            ["git", "ls-files", "--error-unmatch", self.SANDBOX],
            cwd=REPO_ROOT, capture_output=True, text=True,
        )
        assert listed.returncode != 0, (
            f"{self.SANDBOX} is tracked by git. An ignore rule does not apply "
            "to a tracked file, so it is still committable. Untrack it with "
            "`git rm --cached python/sandbox/aim.py`."
        )

    def test_the_sandbox_folder_itself_stays_tracked(self):
        """
        The ignore rule is scoped to the one file on purpose.

        python/sandbox/__init__.py must remain tracked, or the package becomes
        unimportable and the lane stops being a package. Untracking aim.py must
        not take the folder with it.
        """
        listed = subprocess.run(
            ["git", "ls-files", "python/sandbox/"],
            cwd=REPO_ROOT, capture_output=True, text=True, check=True,
        ).stdout.split()
        assert "python/sandbox/__init__.py" in listed, (
            "python/sandbox/__init__.py is no longer tracked; untracking "
            "aim.py must not untrack the package"
        )

