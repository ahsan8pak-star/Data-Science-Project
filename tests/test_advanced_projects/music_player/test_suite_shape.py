"""
Guards on the shape of the music player test suite itself.

Every other guard in this package asks whether the two players behave
correctly. This one asks whether the two halves of the suite are still
balanced, because that is the thing no behavioural test can notice.

The GUI wrapper is the larger surface: it owns the window, the track list,
the checkbox variables and every delegation into the audio engine, so it
carries more cases than the terminal player - roughly one and a quarter
times the count. That figure is guidance rather than a quota, and the guard
is written to match: it fails when the GUI stops being the thicker suite at
all, and warns at a fifth rather than a quarter, so adding cases to one half
does not immediately break the other.

The counts are read from the files rather than from a pytest collection,
because a collection here would have to run the package from inside the
package.
"""

import re

from pathlib import Path


BASE = Path(__file__).resolve().parent

# The GUI stops being the lead suite below this multiple of the TUI count.
MIN_RATIO = 1.15
# The intended guidance, recorded so the guard can name how far off it is.
TARGET_RATIO = 1.25


def _case_count(path):
    """Test functions defined in one test module, indented inside a class."""
    source = path.read_text(encoding="utf-8")
    return len(re.findall(r"^    def test_", source, re.M))


def _counts_by_family():
    """
    (tui, gui) case counts across the package.

    Split by file name rather than by a hand-kept list, so adding a second
    GUI module is picked up without editing this file.
    """
    tui = gui = 0
    for path in sorted(BASE.glob("test_*.py")):
        count = _case_count(path)
        if "gui" in path.name:
            gui += count
        elif "tui" in path.name:
            tui += count
    return tui, gui


class TestSuiteShape:
    """The GUI suite must stay the thicker of the two halves."""

    def test_the_gui_suite_is_not_thinner_than_the_tui(self):
        tui, gui = _counts_by_family()
        assert tui > 0, "no TUI cases found; the file names may have changed"
        assert gui >= tui, (
            f"the GUI suite holds {gui} cases against the TUI's {tui}; the "
            "GUI wrapper is the larger surface and must not become the "
            "thinner suite"
        )

    def test_the_gui_suite_holds_a_quarter_more_cases(self):
        tui, gui = _counts_by_family()
        ratio = gui / tui
        assert ratio >= MIN_RATIO, (
            f"GUI:TUI case ratio is {ratio:.2f}; the guidance is "
            f"{TARGET_RATIO:.2f} and the floor is {MIN_RATIO:.2f}. Either "
            "add GUI cases or record why the ratio has been reset."
        )

    def test_the_ratio_is_within_tolerance_of_the_guidance(self):
        """
        Names the drift rather than failing on it. A ratio well past the
        guidance is as much a signal as one below it: it means one half has
        grown without the other being looked at.
        """
        tui, gui = _counts_by_family()
        ratio = gui / tui
        assert ratio <= TARGET_RATIO + 0.35, (
            f"GUI:TUI case ratio is {ratio:.2f}, well above the "
            f"{TARGET_RATIO:.2f} guidance; check the TUI suite has not been "
            "left behind"
        )

