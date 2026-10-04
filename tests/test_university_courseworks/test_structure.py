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

WEEK_RE = re.compile(r"^week\d+$")
SKIP_DIRS = {"__pycache__", ".ipynb_checkpoints"}

# Type folders, and the single extension each one is allowed to carry.
TYPE_SUFFIXES = {"java": ".java", "python": ".py", "pdf": ".pdf",
                 "sql": ".sql", "txt": ".txt", "data": None, "csv": ".csv"}

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
    Every CS1IP week splits into lecture/ and practical/, each carrying its
    material under java/, python/ and pdf/.
    """

    @pytest.fixture(scope="class")
    @classmethod
    def weeks(cls):
        return week_folders(CS1IP)

    def test_cs1ip_has_week_folders(self, weeks):
        assert weeks, "no week folders found under cs1ip/"

    def test_every_week_splits_lecture_and_practical(self, weeks):
        offenders = {
            week.name: subfolders(week) for week in weeks
            if not {"lecture", "practical"} <= set(subfolders(week))
        }
        assert offenders == {}, f"weeks missing lecture/practical: {offenders}"

    def test_every_week_offers_the_three_type_folders(self, weeks):
        """
        The type folders are created in all eleven weeks, which is what makes
        the split uniform even where a week has no material of that kind yet
        (an empty java/ in a lecture-only week is expected).
        """
        offenders = {}
        for week in weeks:
            for half in ("lecture", "practical"):
                expected = {"java", "python", "pdf"}
                missing = expected - set(subfolders(week / half))
                if missing:
                    offenders[f"{week.name}/{half}"] = sorted(missing)
        assert offenders == {}, f"type folders not created yet: {offenders}"

    def test_type_folders_carry_only_their_own_extension(self, weeks):
        offenders = {}
        for week in weeks:
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

    def test_loose_files_confined_to_weeks_mid_migration(self, weeks):
        """
        Files still sitting directly in lecture/ or practical/ belong only to
        the weeks named in WEEKS_MID_MIGRATION. Finishing a week means
        deleting its name from that set, which tightens this guard.
        """
        offenders = {}
        for week in weeks:
            for half in ("lecture", "practical"):
                names = loose_files(week / half)
                if names and week.name not in WEEKS_MID_MIGRATION:
                    offenders[f"{week.name}/{half}"] = names
        assert offenders == {}, (
            "files loose above the type folders outside the weeks named in "
            f"WEEKS_MID_MIGRATION: {offenders}"
        )

    def test_fixture_folders_are_not_mistaken_for_type_folders(self, weeks):
        """
        week_07_practical_files and week_08_practical_files hold the data a
        practical reads, so they legitimately mix .txt, .csv and .py. They
        are the reason the extension check above is scoped to known type
        folders rather than applied to every sub-folder.
        """
        fixture_dirs = sorted(
            f"{week.name}/{half}/{p.name}"
            for week in weeks
            for half in ("lecture", "practical")
            for p in (week / half).iterdir()
            if p.is_dir() and p.name not in TYPE_SUFFIXES
            and p.name not in SKIP_DIRS
        )
        assert fixture_dirs, "expected at least one practical fixture folder"


class TestSemesterTwoModules:
    """
    CS1DB and CS1OP follow the lecture/practical split like CS1IP, with the
    type folders their own modules imply: sql/ and data/ for the databases
    module, java/ and python/ for the OOP module.
    """

    @pytest.mark.parametrize("module", ["cs1db", "cs1op"])
    def test_module_has_week_folders(self, module):
        parent = CS1DB if module == "cs1db" else CS1OP
        assert len(week_folders(parent)) >= 10, f"{module} lost its week folders"

    @pytest.mark.parametrize("module", ["cs1db", "cs1op"])
    def test_every_week_splits_lecture_and_practical(self, module):
        parent = CS1DB if module == "cs1db" else CS1OP
        offenders = {
            week.name: subfolders(week) for week in week_folders(parent)
            if not {"lecture", "practical"} <= set(subfolders(week))
        }
        assert offenders == {}, f"{module} weeks missing a half: {offenders}"

    def test_cs1db_uses_sql_and_data(self):
        week = CS1DB / "week1"
        assert {"sql", "data"} <= set(subfolders(week / "lecture"))
        assert {"sql", "data"} <= set(subfolders(week / "practical"))

    def test_cs1op_uses_java_python_and_pdf(self):
        week = CS1OP / "week1"
        assert {"java", "python", "pdf"} <= set(subfolders(week / "lecture"))

    def test_cs1op_carries_a_coursework_folder(self):
        coursework = CS1OP / "coursework"
        assert coursework.is_dir()
        assert {"java", "python"} <= set(subfolders(coursework))


class TestYearTwoLayout:
    """
    Year 2 is early: CS2DA splits by language without a lecture/practical
    level, and semester 2 is present but empty.
    """

    def test_cs2da_weeks_split_by_language(self):
        weeks = week_folders(CS2DA)
        assert len(weeks) >= 10, "cs2da lost its week folders"
        offenders = {
            week.name: subfolders(week) for week in weeks
            if not {"java", "python"} <= set(subfolders(week))
        }
        assert offenders == {}, f"cs2da weeks missing java/python: {offenders}"

    def test_cs2pp_has_week_folders_for_the_current_semester(self):
        cs2pp = COURSEWORKS / "year2" / "semester1" / "cs2pp"
        assert week_folders(cs2pp), "cs2pp has no week folders"

    def test_year2_semester2_is_present_but_empty(self):
        """
        Semester 2 of year 2 is genuinely empty rather than absent, so the
        tree records the intent without inventing files in it.
        """
        semester2 = COURSEWORKS / "year2" / "semester2"
        assert semester2.is_dir()
        assert not any(semester2.iterdir())

