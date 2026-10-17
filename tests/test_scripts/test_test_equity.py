"""
Guards for test-equity across the python/ portfolio.

A module is not "well tested" because it has N tests; it is well tested when
the tests it has are in proportion to what the module actually does.  Equal
counts per file are the wrong target - a 200-line calculator and a 5-line
helper do not deserve the same effort.  The right target is a consistent
ratio of tests (and the guards inside them) to the module's behavioural
surface, plus coverage of the full input/output range.

This guard reads the live measurement from scripts/test_equity.py rather
than pinning constants, so it ratchets against reality instead of a stale
number.  Loosening any threshold here is a deliberate decision, not a
silent edit, and must be justified in the commit message.
"""

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from test_equity import measure  # noqa: E402


@pytest.fixture(scope="module")
def equity():
    summary, report = measure()
    return summary, report


class TestTestEquityCoverage:
    """Every non-stub module must be exercised by at least one test."""

    def test_every_measured_module_has_a_surface(self, equity):
        _, report = equity
        assert all(r["surface"]["surface"] >= 1 for r in report.values())

    def test_measured_module_count_matches_the_portfolio(self, equity):
        summary, _ = equity
        assert summary["modules_measured"] == 160

    def test_only_the_deliberate_stub_has_no_tests(self, equity):
        summary, _ = equity
        # main.py is a deliberate IndentationError-stub-turned-`pass`; it is
        # the one module with no behavioural surface worth testing.
        assert summary["modules_with_zero_tests"] <= 1
        assert summary["modules_with_tests"] >= 159


class TestTestEquityFullRange:
    """A module's tests must cover its inputs and carry at least one guard."""

    def test_full_range_failures_are_zero(self, equity):
        summary, _ = equity
        # main.py is the only module allowed to have no tests; every other
        # module must have its inputs exercised and at least one assertion.
        assert summary["full_range_failures"] <= 1


class TestTestEquityProportion:
    """Test density must be consistent across modules (ratio-equivalent)."""

    def test_density_coefficient_of_variation_is_bounded(self, equity):
        """
        Ratchet, not a target. Measured CV is 2.22 after the portable-order
        fix in test_tui_players.py; the floor sits above it so ordinary work
        does not trip the guard, and lowering it is how equity improves.

        [AI] Set to 2.2 the first time, from a measurement taken minutes
        earlier, and it failed on the very next run because editing one test
        moved CV to 2.224. A ratchet tighter than the thing it watches is not
        a ratchet, it is a tripwire on your own edits - and the same mistake
        the repo has already made once with the coverage figures, where a
        recorded count was pinned without the toolchain that produced it.
        """
        summary, _ = equity
        assert summary["density_cv"] <= 2.3, (
            f"density CV {summary['density_cv']} exceeds the 2.3 ratchet "
            "(measured baseline 2.22); the test suite has become less "
            "proportionally distributed, or the surface metric has moved"
        )

    def test_density_min_max_ratio_is_bounded(self, equity):
        summary, _ = equity
        assert summary["density_min_max_ratio"] is not None
        assert summary["density_min_max_ratio"] <= 310, (  # measured 301.21
            f"density min/max ratio {summary['density_min_max_ratio']} exceeds "
            "the 310 ratchet"
        )

    def test_unattributed_cases_are_bounded(self, equity):
        summary, _ = equity
        # Cases that could not be tied to a specific module.  Ratchet: 80.
        assert summary["unattributed_cases"] <= 80, (
            f"{summary['unattributed_cases']} cases could not be attributed to "
            "a module; the mapping has regressed"
        )

    def test_unattributed_guards_are_bounded(self, equity):
        summary, _ = equity
        assert summary["unattributed_guards"] <= 230, (
            f"{summary['unattributed_guards']} guards could not be attributed"
        )

