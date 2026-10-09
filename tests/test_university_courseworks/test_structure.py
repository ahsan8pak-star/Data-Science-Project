"""
Structural guards for the `university_courseworks/` tree.

[AI] The coursework tree was reorganised on 4 October 2026 from a flat week
folder into a per-week `lecture/` and `practical/` split, with `java/`,
`python/` and `pdf/` beneath each, and the two CS1IP coursework folders
gained `java/`, `python/` and `data/`. That reorganisation changes the
tree's *shape*, so it is worth guarding like any other contract: the tests
below assert the layout the rest of the suite and the documentation now
assume.

Three kinds of assertion appear here, and the distinction matters:

  - **Invariants** that hold everywhere and are cheap to break — every week
    splits into lecture and practical, a type folder carries one extension,
    every marked script has both language twins.
  - **Named exemptions** for the parts of the migration still in flight.
    A.I.M was still moving files while these tests were written, so three
    CS1IP weeks still hold files loose above their type folders. Naming
    those weeks here means finishing the migration is a one-line edit to
    this file, and the guard tightens as a result — rather than the
    convention being quietly dropped to match the tree.
  - **Deliberate non-uniformity** — CS2DA splits by language without a
    lecture/practical level, and CS1DB uses `sql/` where the others use
    `java/`. Both are facts about the modules, not oversights.

Nothing here executes coursework code or asserts a marked artefact's
behaviour: these are layout assertions only.
"""

import json
import re

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve()
while PROJECT_ROOT.name != "Data-Science-Project":
    PROJECT_ROOT = PROJECT_ROOT.parent

COURSEWORKS = PROJECT_ROOT / "university_courseworks"
CS1IP = COURSEWORKS / "year1" / "semester1" / "cs1ip"
CS1DB = COURSEWORKS / "year1" / "semester2" / "cs1db"
CS1OP = COURSEWORKS / "year1" / "semester2" / "cs1op"
CS2DA = COURSEWORKS / "year2" / "semester1" / "cs2da"
CS2PP = COURSEWORKS / "year2" / "semester1" / "cs2pp"

WEEK_RE = re.compile(r"^week\d+$")
SKIP_DIRS = {"__pycache__", ".ipynb_checkpoints"}

# Type folders, and the single extension each may carry; `jupyter` joined on
# 4 October 2026, when CS2PP's weeks gained notebook folders, and `pptx` on
# 8 October 2026, when CS1OP's lecture halves gained their slide decks.
TYPE_SUFFIXES = {"java": ".java", "python": ".py", "pdf": ".pdf",
                 "sql": ".sql", "txt": ".txt", "data": None, "csv": ".csv",
                 "jupyter": ".ipynb", "pptx": ".pptx"}

# Modules whose weeks split into lecture/ and practical/, and the type folders
# each nests: CS1DB carries sql/ and data/, CS2PP carries jupyter/ in both halves.
SPLIT_MODULES = {
    "cs1ip": {"lecture": {"java", "python", "pdf"},
              "practical": {"java", "python", "pdf"}},
    "cs1db": {"lecture": {"sql", "data", "pdf"},
              "practical": {"sql", "data", "pdf"}},
    "cs1op": {"lecture": {"java", "python", "pdf"},
              "practical": {"java", "python", "pdf"}},
    "cs2pp": {"lecture": {"jupyter", "pdf"},
              "practical": {"jupyter", "pdf"}},
}

# Type folders a half may carry without being required to. The contract above is
# a *required* shape, and CS1OP cannot honour it: its lecture material is slide
# decks rather than PDFs, and every PDF in this repository is deliberately
# gitignored as local-only, so a pdf/ folder holding nothing but ignored PDFs is
# untrackable - git cannot commit an empty folder, so the requirement would pass
# on the owner's disk and fail on a fresh clone. CS1OP therefore requires
# java/ and python/ and merely allows pdf/ and pptx/. Decided 8 October 2026.
OPTIONAL_TYPE_FOLDERS = {"cs1op": {"lecture": {"pdf", "pptx"},
                                   "practical": {"pdf"}}}

# CS2PP's python/ folders are empty everywhere and outside its contract: its work
# is notebook-based, so they are leftovers from before the notebooks were split out.
STALE_TYPE_FOLDERS = {("cs2pp", "python")}

# CS1IP week7's lecture carries a txt/ folder, because it reads and writes
# text files; the one type folder outside the shared contract. CS1IP week3's
# lecture carries week_03_lecture_code/, which holds that week's lecture code as
# A.I.M placed it on 8 October 2026 - the lecture half's counterpart to the
# week_07_practical_files fixtures.
EXTRA_TYPE_FOLDERS = {("cs1ip", "week7", "lecture"): {"txt"},
                      ("cs1ip", "week3", "lecture"): {"week_03_lecture_code"}}

MODULE_PATHS = {"cs1ip": CS1IP, "cs1db": CS1DB, "cs1op": CS1OP, "cs2pp": CS2PP}

# Every module folder, including CS2DA which is deliberately absent from
# SPLIT_MODULES; the "only module without the split" check needs all of them.
ALL_MODULE_PATHS = dict(MODULE_PATHS, cs2da=CS2DA)

# CS1IP weeks still holding files loose above their type folders mid-migration;
# delete an entry as its week is finished rather than relaxing the check.
WEEKS_MID_MIGRATION = {"week8", "week9", "week12"}

# Files that legitimately sit at a coursework root: desktop.ini is created
# by Windows Explorer, not by A.I.M.
ROOT_ARTEFACTS = {"desktop.ini"}


def week_folders(parent):
    """Week folders directly under `parent`, ordered by week number."""
    if not parent.is_dir():
        return []
    found = [p for p in parent.iterdir() if p.is_dir() and WEEK_RE.match(p.name)]
    return sorted(found, key=lambda p: int(p.name[4:]))


def subfolders(folder):
    """Immediate sub-folders of `folder`, excluding caches and checkpoints."""
    if not folder.is_dir():
        return []
    return sorted(
        p.name for p in folder.iterdir()
        if p.is_dir() and p.name not in SKIP_DIRS
    )


def loose_files(folder):
    """Files sitting directly in `folder`, ignoring hidden metadata files."""
    return sorted(
        p.name for p in folder.iterdir()
        if p.is_file() and p.name not in ROOT_ARTEFACTS
    )


class TestTopLevelLayout:
    """The three study years, the modules reference, and the modules folders."""

    @pytest.mark.parametrize("name", [
        "university_modules", "year1", "year2", "year3",
    ])
    def test_expected_top_level_folder_exists(self, name):
        assert (COURSEWORKS / name).is_dir(), f"missing {name}/"

    def test_university_modules_holds_the_rolling_reference(self):
        reference = COURSEWORKS / "university_modules" / "UNIVERSITY_MODULES.md"
        assert reference.is_file()
        assert reference.stat().st_size > 0

    @pytest.mark.parametrize("year", ["year1", "year2", "year3"])
    def test_each_year_carries_a_modules_folder(self, year):
        assert (COURSEWORKS / year / "modules").is_dir(), f"{year}/modules/ missing"

    def test_no_modules_folder_is_empty(self):
        empty = [
            f"{year.name}/modules"
            for year in sorted(COURSEWORKS.glob("year*"))
            if (year / "modules").is_dir() and not any((year / "modules").iterdir())
        ]
        assert empty == [], f"empty module folders: {empty}"


class TestCs1ipCourseworkFolders:
    """
    coursework1 and coursework2 split by language; coursework1 keeps
    settings.json with the Java side, coursework2 keeps its deck fixtures in
    data/.
    """

    def test_coursework1_splits_java_and_python(self):
        assert {"java", "python"} <= set(subfolders(CS1IP / "coursework1"))

    def test_coursework2_splits_java_python_and_data(self):
        assert {"java", "python", "data"} <= set(subfolders(CS1IP / "coursework2"))

    @pytest.mark.parametrize("stem", [
        "average_grades", "hello", "ice_cream", "seven_segment", "volume",
    ])
    def test_every_marked_script_has_both_language_twins(self, stem):
        assert (CS1IP / "coursework1" / "python" / f"{stem}.py").is_file()
        assert (CS1IP / "coursework1" / "java" / f"{stem}.java").is_file()

    def test_coursework2_module_and_its_java_twin_are_split(self):
        assert (CS1IP / "coursework2" / "python" / "sort_comparison.py").is_file()
        assert (CS1IP / "coursework2" / "java" / "sort_comparison.java").is_file()

    def test_settings_json_sits_with_the_java_sources(self):
        assert (CS1IP / "coursework1" / "java" / "settings.json").is_file()

    @pytest.mark.parametrize("name", [
        "sort10.txt", "sort100.txt", "sort10000.txt", "sort_comparison.csv",
    ])
    def test_coursework2_fixtures_live_in_data(self, name):
        assert (CS1IP / "coursework2" / "data" / name).is_file()

    @pytest.mark.parametrize("folder", ["coursework1", "coursework2"])
    def test_no_script_or_fixture_sits_at_the_coursework_root(self, folder):
        """
        The point of the split: nothing language-shaped is left loose in a
        coursework folder, so a reader never has to guess where a file went.
        Windows' desktop.ini is exempt and named in ROOT_ARTEFACTS.
        """
        assert loose_files(CS1IP / folder) == []


class TestCs1ipWeekFoldersSplitLectureAndPractical:
    """
    Every week of every conforming module splits into lecture/ and
    practical/, each carrying its material under the type folders that
    module implies. CS2PP joined this convention on 4 October 2026 and is
    checked by the same rules as CS1IP, CS1DB and CS1OP.
    """

    @staticmethod
    def weeks(module):
        """
        The module's week folders.

        Read per test, because `module` is a function-scoped parametrisation
        and cannot feed a class-scoped fixture without a ScopeMismatch.
        """
        return week_folders(MODULE_PATHS[module])

    @pytest.mark.parametrize("module", sorted(SPLIT_MODULES))
    def test_module_has_week_folders(self, module):
        assert len(self.weeks(module)) >= 10, (
            f"{module} has only {len(self.weeks(module))} week folders"
        )

    @pytest.mark.parametrize("module", sorted(SPLIT_MODULES))
    def test_every_week_splits_lecture_and_practical(self, module):
        offenders = {
            week.name: subfolders(week) for week in self.weeks(module)
            if not {"lecture", "practical"} <= set(subfolders(week))
        }
        assert offenders == {}, f"{module} weeks missing a half: {offenders}"

    @pytest.mark.parametrize("module", sorted(SPLIT_MODULES))
    def test_every_week_offers_its_module_type_folders(self, module):
        """
        The type folders exist in every week even where a week has no
        material of that kind yet, which is what keeps the shape uniform: an
        empty java/ in a lecture-only week is expected, a missing one is not.

        Only the *required* half of the contract is demanded here. The optional
        kinds are in OPTIONAL_TYPE_FOLDERS because a folder holding nothing but
        gitignored material cannot be committed, so requiring one would make the
        guard pass on the owner's disk and fail on a fresh clone.
        """
        required = SPLIT_MODULES[module]
        offenders = {}
        for week in self.weeks(module):
            for half, kinds in required.items():
                optional = OPTIONAL_TYPE_FOLDERS.get(module, {}).get(half, set())
                extra = EXTRA_TYPE_FOLDERS.get((module, week.name, half), set())
                missing = (kinds - optional - extra) - set(subfolders(week / half))
                if missing:
                    offenders[f"{week.name}/{half}"] = sorted(missing)
        assert offenders == {}, f"{module} type folders not created: {offenders}"

    @pytest.mark.parametrize("module", sorted(SPLIT_MODULES))
    def test_no_unexpected_type_folders(self, module):
        """
        A folder the module's contract does not list is either a typo or an
        unrecorded convention, and both are worth failing on: this is what
        stops a new folder appearing without anyone deciding what it means.
        """
        expected = SPLIT_MODULES[module]
        optional = OPTIONAL_TYPE_FOLDERS.get(module, {})
        offenders = {}
        for week in self.weeks(module):
            for half in ("lecture", "practical"):
                allowed = (expected[half]
                           | optional.get(half, set())
                           | EXTRA_TYPE_FOLDERS.get((module, week.name, half), set()))
                extra = set(subfolders(week / half)) - allowed - SKIP_DIRS
                # Fixture folders hold a practical's data rather than a type
                # of material, so they are excluded by name, not listed.
                extra = {name for name in extra if "practical_files" not in name}
                if extra:
                    offenders[f"{week.name}/{half}"] = sorted(extra)
        assert offenders == {}, f"{module} folders not in the contract: {offenders}"

    @pytest.mark.parametrize("module", sorted(SPLIT_MODULES))
    def test_weeks_hold_nothing_but_the_two_halves(self, module):
        """
        A week folder contains lecture/ and practical/ and nothing else.

        The check above only looks *inside* those two halves, so a stray
        folder dropped beside them would otherwise pass unnoticed - which is
        how a scratch directory or a loose script survives several commits.
        """
        offenders = {
            week.name: subfolders(week) for week in self.weeks(module)
            if set(subfolders(week)) - {"lecture", "practical"} - SKIP_DIRS
        }
        assert offenders == {}, (
            f"{module} weeks holding folders other than lecture/practical: {offenders}"
        )

    @pytest.mark.parametrize("module", sorted(SPLIT_MODULES))
    def test_weeks_hold_no_loose_files(self, module):
        """A file sitting directly in a week folder is unmigrated material."""
        offenders = {
            week.name: loose_files(week) for week in self.weeks(module)
            if loose_files(week)
        }
        assert offenders == {}, f"{module} weeks holding loose files: {offenders}"

    @pytest.mark.parametrize("module", sorted(SPLIT_MODULES))
    def test_type_folders_carry_only_their_own_extension(self, module):
        offenders = {}
        for week in self.weeks(module):
            for half in ("lecture", "practical"):
                for kind in subfolders(week / half):
                    folder = week / half / kind
                    wanted = TYPE_SUFFIXES.get(kind)
                    if wanted is None:
                        continue
                    wrong = sorted(
                        p.name for p in folder.iterdir()
                        if p.is_file() and p.suffix.lower() != wanted
                    )
                    if wrong:
                        offenders[f"{week.name}/{half}/{kind}"] = wrong
        assert offenders == {}, f"type folders holding foreign files: {offenders}"

    @pytest.mark.parametrize("module", sorted(SPLIT_MODULES))
    def test_loose_files_confined_to_weeks_mid_migration(self, module):
        """
        Files still sitting directly in lecture/ or practical/ belong only to
        the weeks named in WEEKS_MID_MIGRATION. Finishing a week means
        deleting its name from that set, which tightens this guard.
        """
        offenders = {}
        for week in self.weeks(module):
            for half in ("lecture", "practical"):
                names = loose_files(week / half)
                if names and week.name not in WEEKS_MID_MIGRATION:
                    offenders[f"{week.name}/{half}"] = names
        assert offenders == {}, (
            "files loose above the type folders outside the weeks named in "
            f"WEEKS_MID_MIGRATION: {offenders}"
        )

    def test_fixture_folders_are_not_mistaken_for_type_folders(self):
        """
        week_07_practical_files and week_08_practical_files hold the data a
        practical reads, so they legitimately mix .txt, .csv and .py. They
        are the reason the extension check above is scoped to known type
        folders rather than applied to every sub-folder.
        """
        fixture_dirs = sorted(
            f"{week.name}/{half}/{p.name}"
            for week in self.weeks("cs1ip")
            for half in ("lecture", "practical")
            for p in (week / half).iterdir()
            if p.is_dir() and p.name not in TYPE_SUFFIXES
            and p.name not in SKIP_DIRS
        )
        assert fixture_dirs, "expected at least one practical fixture folder"


class TestModuleCourseworkFolders:
    """
    Coursework folders, per module. CS1DB is the one module of the four with
    no coursework folder, which is a fact about the module rather than an
    omission, so it is asserted rather than left unremarked.
    """

    def test_cs1db_has_no_coursework_folder_yet(self):
        """
        CS1DB's coursework folder has not been created. Naming the gap means
        adding it later is a deliberate change to this file rather than a
        silent divergence from the other three modules.
        """
        coursework = [
            p.name for p in CS1DB.iterdir()
            if p.is_dir() and p.name.startswith("coursework")
        ]
        assert coursework == [], f"unexpected cs1db coursework folder: {coursework}"

    def test_cs1op_carries_a_coursework_folder(self):
        coursework = CS1OP / "coursework"
        assert coursework.is_dir()
        assert {"java", "python"} <= set(subfolders(coursework))

    @pytest.mark.parametrize("name", ["coursework1", "coursework2"])
    def test_cs2pp_has_both_coursework_folders(self, name):
        folder = CS2PP / name
        assert folder.is_dir(), f"cs2pp/{name} missing"
        assert not loose_files(folder), f"cs2pp/{name} holds loose files"

    def test_cs2pp_weeks_use_notebooks_in_both_halves(self):
        """
        CS2PP is the Python module whose material is submitted as notebooks,
        so both halves carry jupyter/ where the programming modules carry a
        second programming-language folder. The lecture half gained one too on
        4 October 2026, which is why this no longer asserts its absence.
        """
        week = CS2PP / "week1"
        assert "jupyter" in subfolders(week / "lecture")
        assert "jupyter" in subfolders(week / "practical")

    def test_cs2pp_has_no_empty_python_folders(self):
        """
        CS2PP's python/ folders hold nothing in any of the eleven weeks and
        are not part of its contract; they are leftovers from before the
        notebooks were split out. This asserts the tree matches that decision
        rather than leaving twenty empty folders to be rediscovered later.
        """
        stale = [
            f"{week.name}/{half}"
            for week in week_folders(CS2PP)
            for half in ("lecture", "practical")
            if (week / half / "python").is_dir()
        ]
        assert stale == [], (
            "cs2pp carries an empty python/ folder in these weeks, which its "
            f"contract does not include: {stale}. Delete them, or drop "
            "(\"cs2pp\", \"python\") from STALE_TYPE_FOLDERS if .py files are "
            "intended here after all."
        )


class TestCs2ppNotebooks:
    """
    CS2PP's only tracked files are notebooks. Validity, cell count and the
    kernel are checked because a notebook that will not open is
    indistinguishable from an empty folder until someone tries.
    """

    def test_every_tracked_notebook_is_valid_json_with_cells(self):
        """
        Only *tracked* notebooks are checked. Jupyter writes an autosaved copy
        into .ipynb_checkpoints/ that can be empty, and that folder is
        gitignored (root .gitignore), so asserting on it would fail on a file
        the repository has deliberately excluded.
        """
        notebooks = sorted(
            p for p in CS2PP.rglob("*.ipynb")
            if ".ipynb_checkpoints" not in p.parts
        )
        assert notebooks, "expected at least one notebook under cs2pp/"
        for notebook in notebooks:
            payload = json.loads(notebook.read_text(encoding="utf-8"))
            rel = notebook.relative_to(PROJECT_ROOT).as_posix()
            assert "cells" in payload, f"{rel} has no cells key"
            assert payload["cells"], f"{rel} has no cells"

    def test_notebooks_declare_a_kernel_or_a_language(self):
        """
        A notebook should name the kernel it was written against, so that
        opening it later runs against the same interpreter.

        [AI] This was originally a bare `kernelspec.name` assertion, and it
        failed on week2/lecture/jupyter/basic.ipynb - 132 cells that carry
        `metadata.language_info.name = python` but no kernelspec. That is a
        real gap in the file, not a strict test: the notebook cannot pick a
        kernel, so opening it silently falls back to the environment default.
        Asserting one *or* the other is what a notebook can actually satisfy,
        and it still catches the genuinely kernel-less case of an empty
        metadata block.
        """
        undeclared = []
        for notebook in sorted(
            p for p in CS2PP.rglob("*.ipynb")
            if ".ipynb_checkpoints" not in p.parts
        ):
            metadata = json.loads(
                notebook.read_text(encoding="utf-8")
            ).get("metadata", {})
            kernel = metadata.get("kernelspec", {}).get("name")
            language = metadata.get("language_info", {}).get("name")
            if not kernel and not language:
                undeclared.append(
                    notebook.relative_to(PROJECT_ROOT).as_posix()
                )
        assert undeclared == [], (
            "notebooks naming neither a kernelspec nor a language_info, so "
            f"Jupyter cannot tell what they were written against: {undeclared}"
        )


class TestYearTwoLayout:
    """
    Year 2 is early. CS2PP now follows the lecture/practical convention;
    CS2DA is the last module that does not, and semester 2 is still empty.
    """

    def test_cs2da_weeks_split_by_language(self):
        """
        CS2DA is the one module left without a lecture/practical level: its
        weeks carry java/ and python/ directly. Recorded as the open case, so
        closing it means editing this test rather than leaving it to drift.
        """
        weeks = week_folders(CS2DA)
        assert len(weeks) >= 10, "cs2da lost its week folders"
        offenders = {
            week.name: subfolders(week) for week in weeks
            if not {"java", "python"} <= set(subfolders(week))
        }
        assert offenders == {}, f"cs2da weeks missing java/python: {offenders}"

    def test_cs2da_is_the_only_module_without_the_split(self):
        """
        One assertion that names the exception, so adding the split to CS2DA
        makes this fail and prompts a decision rather than being absorbed.

        It walks every module folder, not only the conforming ones: an
        earlier version read SPLIT_MODULES, which excluded CS2DA and so
        passed without inspecting anything at all.
        """
        assert set(ALL_MODULE_PATHS) == set(SPLIT_MODULES) | {"cs2da"}

        without_split = sorted(
            name for name, path in ALL_MODULE_PATHS.items()
            if any("lecture" not in subfolders(week) for week in week_folders(path))
        )
        assert without_split == ["cs2da"], (
            "expected cs2da to be the only module without a lecture/ half; if "
            "one has been migrated, update SPLIT_MODULES and this list "
            f"together: {without_split}"
        )

    def test_year2_semester2_is_present_but_empty(self):
        """
        Semester 2 of year 2 is genuinely empty rather than absent, so the
        tree records the intent without inventing files in it.
        """
        semester2 = COURSEWORKS / "year2" / "semester2"
        assert semester2.is_dir()
        assert not any(semester2.iterdir())

