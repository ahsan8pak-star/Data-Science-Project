"""
Pytest suite for every script under python/functional_programming/fundamental_topics/.

Each script is executed for real via run_script() (see conftest.py), so these
tests exercise the actual coursework code rather than reimplementations of
it. None of these four files call input(), so every test asserts against
either the module's own top-level variables (accessible straight off the
executed module object) or the exact lines it printed.
"""

from tests.test_functional_programming.conftest import run_script

FOLDER = "functional_programming/fundamental_topics"


# ---------------------------------------------------------------------------
# filter.py
# ---------------------------------------------------------------------------

class TestFilter:
    FILE = f"{FOLDER}/filter.py"

    def test_even_odd_split(self):
        mod, _ = run_script(self.FILE)
        assert mod.evens == [2, 4, 6, 8, 10]
        assert mod.odds == [1, 3, 5, 7, 9]

    def test_adults_and_minors_threshold(self):
        mod, _ = run_script(self.FILE)
        assert mod.adults == [18, 21, 25]
        assert mod.minors == [15, 12, 17, 16]

    def test_non_empty_words_filtered(self):
        mod, _ = run_script(self.FILE)
        assert mod.non_empty_words == ["hello", "world", "python"]

    def test_filter_none_keeps_only_truthy_values(self):

        """
        filter(None, iterable) is a genuine, distinct code path from a
        lambda predicate - it drops every falsy value (0, "", None,
        False) while keeping 1, "text", 3.5, and True.
        """

        mod, _ = run_script(self.FILE)
        assert mod.truthy_only == [1, "text", 3.5, True]

    def test_printed_output_matches_computed_lists(self):
        mod, out = run_script(self.FILE)
        assert "Even numbers: [2, 4, 6, 8, 10]" in out
        assert "Odd numbers: [1, 3, 5, 7, 9]" in out
        assert "Adults (18+): [18, 21, 25]" in out
        assert "Minors (under 18): [15, 12, 17, 16]" in out
        assert "Non-empty words: ['hello', 'world', 'python']" in out
        assert "Truthy-only values: [1, 'text', 3.5, True]" in out

    def test_source_lists_are_unmodified(self):

        """
        filter() must not mutate its input iterable - confirms numbers,
        ages, and words still hold their original, unfiltered values.
        """

        mod, _ = run_script(self.FILE)
        assert mod.numbers == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        assert mod.ages == [15, 18, 12, 21, 17, 25, 16]
        assert mod.words == ["hello", "", "world", "", "python", ""]


# ---------------------------------------------------------------------------
# lambda.py
# ---------------------------------------------------------------------------

class TestLambda:
    FILE = f"{FOLDER}/lambda.py"

    def test_arithmetic_lambdas_directly(self):
        mod, _ = run_script(self.FILE)
        assert mod.double(2) == 4
        assert mod.halved(4) == 2.0
        assert mod.add(3, 4) == 7
        assert mod.subtract(5, 2) == 3
        assert mod.multiply(6, 7) == 42
        assert mod.divide(24, 8) == 3.0
        assert mod.base(7, 3) == 2
        assert mod.remainder(8, 5) == 3

    def test_comparison_lambdas_directly(self):
        mod, _ = run_script(self.FILE)
        assert mod.max_value(6, 7) == 7
        assert mod.min_value(9, 8) == 8

    def test_string_and_boolean_lambdas_directly(self):
        mod, _ = run_script(self.FILE)
        assert mod.full_name("Ahsan", "Iqbal") == "Ahsan Iqbal"
        assert mod.is_even(5) is False
        assert mod.is_odd(6) is False

    def test_age_check_ternary_lambda_boundary(self):

        """
        age_check uses `True if age >= 18 else False`, so 18 itself
        (the boundary) must return True, distinct from 21 comfortably
        above and 16 comfortably below.
        """

        mod, _ = run_script(self.FILE)
        assert mod.age_check(21) is True
        assert mod.age_check(18) is True
        assert mod.age_check(16) is False

    def test_printed_output_in_call_order(self):
        _, out = run_script(self.FILE)
        lines = out.strip().splitlines()
        assert lines == [
            "4", "2.0", "7", "3", "42", "3.0", "2", "3",
            "7", "8", "Ahsan Iqbal", "False", "False",
            "True", "True", "False",
        ]


# ---------------------------------------------------------------------------
# map.py
# ---------------------------------------------------------------------------

class TestMap:
    FILE = f"{FOLDER}/map.py"

    def test_single_iterable_map_squares_and_doubles(self):
        mod, _ = run_script(self.FILE)
        assert mod.squared == [1, 4, 9, 16, 25]
        assert mod.doubled == [2, 4, 6, 8, 10]

    def test_type_conversion_map_strings_to_floats(self):
        mod, _ = run_script(self.FILE)
        assert mod.prices_as_floats == [9.99, 14.50, 3.25, 20.00]
        assert all(isinstance(p, float) for p in mod.prices_as_floats)

    def test_multi_iterable_map_combines_by_position(self):

        """
        Distinct from zip.py: map() here actually combines matching
        positions arithmetically (sum/product), not just pairs them.
        """

        mod, _ = run_script(self.FILE)
        assert mod.sums == [11, 22, 33, 44]
        assert mod.products == [10, 40, 90, 160]

    def test_printed_output_matches_computed_lists(self):
        _, out = run_script(self.FILE)
        assert "Squared: [1, 4, 9, 16, 25]" in out
        assert "Doubled: [2, 4, 6, 8, 10]" in out
        assert "Prices as floats: [9.99, 14.5, 3.25, 20.0]" in out
        assert "Sums (A + B): [11, 22, 33, 44]" in out
        assert "Products (A * B): [10, 40, 90, 160]" in out

    def test_source_lists_are_unmodified(self):
        mod, _ = run_script(self.FILE)
        assert mod.numbers == [1, 2, 3, 4, 5]
        assert mod.list_a == [1, 2, 3, 4]
        assert mod.list_b == [10, 20, 30, 40]


# ---------------------------------------------------------------------------
# zip.py
# ---------------------------------------------------------------------------

class TestZip:
    FILE = f"{FOLDER}/zip.py"

    def test_all_three_people_printed(self):
        _, out = run_script(self.FILE)
        assert "Ahsan is a 21 year old Tutor" in out
        assert "Hamza is a 20 year old Manager" in out
        assert "Yahya is a 19 year old Baker" in out

    def test_printed_in_zipped_order(self):
        _, out = run_script(self.FILE)
        lines = out.strip().splitlines()
        assert lines == [
            "Ahsan is a 21 year old Tutor",
            "Hamza is a 20 year old Manager",
            "Yahya is a 19 year old Baker",
        ]

    def test_zip_pairs_by_position_not_value(self):

        """
        Confirms the pairing is purely positional (index 0 with index 0,
        etc.) rather than some sorted/matched-by-value behaviour.
        """

        mod, _ = run_script(self.FILE)
        zipped = list(zip(mod.names, mod.ages, mod.jobs))
        assert zipped == [
            ("Ahsan", 21, "Tutor"),
            ("Hamza", 20, "Manager"),
            ("Yahya", 19, "Baker"),
        ]

    def test_source_lists_defined_with_expected_lengths(self):
        mod, _ = run_script(self.FILE)
        assert len(mod.names) == len(mod.ages) == len(mod.jobs) == 3

