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


# ---------------------------------------------------------------------------
# reduce.py
# ---------------------------------------------------------------------------

class TestReduce:
    FILE = f"{FOLDER}/reduce.py"

    def test_accumulation_results(self):
        mod, _ = run_script(self.FILE)
        assert mod.total == 15
        assert mod.factorial == 120
        assert mod.largest == 5
        assert mod.sentence == "Python is functional"

    def test_source_iterables_unmodified(self):
        mod, _ = run_script(self.FILE)
        assert mod.numbers == [1, 2, 3, 4, 5]
        assert mod.words == ["Python", "is", "functional"]

    def test_printed_output_matches_computed_values(self):
        _, out = run_script(self.FILE)
        assert "Sum: 15" in out
        assert "Factorial of 5: 120" in out
        assert "Largest: 5" in out
        assert "Joined: Python is functional" in out


# ---------------------------------------------------------------------------
# sorted.py
# ---------------------------------------------------------------------------

class TestSorted:
    FILE = f"{FOLDER}/sorted.py"

    def test_sorts_return_new_lists(self):
        mod, _ = run_script(self.FILE)
        assert mod.sorted_names == ["Ahsan", "Alina", "Bilal", "Hamza", "Zara"]
        assert mod.reverse_names == ["Zara", "Hamza", "Bilal", "Alina", "Ahsan"]
        assert mod.by_age == [("Zara", 19), ("Hamza", 20), ("Ahsan", 21), ("Bilal", 22)]

    def test_source_list_is_not_mutated(self):
        mod, _ = run_script(self.FILE)
        assert mod.names == ["Alina", "Hamza", "Zara", "Bilal", "Ahsan"]

    def test_printed_output_matches_computed_lists(self):
        _, out = run_script(self.FILE)
        assert "Sorted: ['Ahsan', 'Alina', 'Bilal', 'Hamza', 'Zara']" in out
        assert "Reverse: ['Zara', 'Hamza', 'Bilal', 'Alina', 'Ahsan']" in out
        assert "By age: [('Zara', 19), ('Hamza', 20), ('Ahsan', 21), ('Bilal', 22)]" in out


# ---------------------------------------------------------------------------
# comprehensions.py
# ---------------------------------------------------------------------------

class TestComprehensions:
    FILE = f"{FOLDER}/comprehensions.py"

    def test_list_comprehensions(self):
        mod, _ = run_script(self.FILE)
        assert mod.squares == [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
        assert mod.evens == [2, 4, 6, 8, 10]

    def test_set_comprehension_removes_duplicates(self):
        mod, _ = run_script(self.FILE)
        assert mod.unique_votes == {"yes", "no", "abstain"}

    def test_dict_comprehension(self):
        mod, _ = run_script(self.FILE)
        assert mod.lengths == {"Ahsan": 5, "Hamza": 5, "Zara": 4}

    def test_printed_output_includes_list_lines(self):
        _, out = run_script(self.FILE)
        assert "Numbers: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]" in out
        assert "Squares: [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]" in out
        assert "Evens: [2, 4, 6, 8, 10]" in out


# ---------------------------------------------------------------------------
# first_class_functions.py
# ---------------------------------------------------------------------------

class TestFirstClassFunctions:
    FILE = f"{FOLDER}/first_class_functions.py"

    def test_handlers_capture_function_references(self):
        mod, _ = run_script(self.FILE)
        assert mod.operation(4) == 16
        assert mod.apply(mod.square, 5) == 25
        assert mod.apply(mod.cube, 5) == 125

    def test_manufactured_functions(self):
        mod, _ = run_script(self.FILE)
        assert mod.doubler(6) == 36
        assert mod.cubed(6) == 216

    def test_printed_output_in_call_order(self):
        _, out = run_script(self.FILE)
        lines = out.strip().splitlines()
        assert lines == [
            "square stored as operation: 16",
            "apply(square, 5): 25",
            "apply(cube, 5): 125",
            "doubler(6): 36",
            "cubed(6): 216",
        ]


# ---------------------------------------------------------------------------
# closures.py
# ---------------------------------------------------------------------------

class TestClosures:
    FILE = f"{FOLDER}/closures.py"

    def test_multipliers_remember_their_factor(self):
        mod, _ = run_script(self.FILE)
        assert mod.double(5) == 10
        assert mod.triple(5) == 15

    def test_counter_remembers_its_state(self):
        mod, _ = run_script(self.FILE)
        assert mod.tickets() == 4

    def test_printed_output_in_call_order(self):
        _, out = run_script(self.FILE)
        lines = out.strip().splitlines()
        assert lines == [
            "double(5): 10",
            "triple(5): 15",
            "ticket 1: 1",
            "ticket 2: 2",
            "ticket 3: 3",
        ]


# ---------------------------------------------------------------------------
# partial_application.py
# ---------------------------------------------------------------------------

class TestPartialApplication:
    FILE = f"{FOLDER}/partial_application.py"

    def test_partials_prefill_arguments(self):
        mod, _ = run_script(self.FILE)
        assert mod.square(4) == 16
        assert mod.cube(3) == 27
        assert mod.formatted(3.14159) == 3.14

    def test_printed_output_matches_partial_results(self):
        _, out = run_script(self.FILE)
        assert "square(4): 16" in out
        assert "cube(3): 27" in out
        assert "formatted(3.14159): 3.14" in out


# ---------------------------------------------------------------------------
# currying.py
# ---------------------------------------------------------------------------

class TestCurrying:
    FILE = f"{FOLDER}/currying.py"

    def test_curried_functions_take_one_argument_at_a_time(self):
        mod, _ = run_script(self.FILE)
        assert mod.curried_add(2)(3) == 5
        assert mod.greet("Hi")("Zara") == "Hi, Zara!"

    def test_printed_output_in_call_order(self):
        _, out = run_script(self.FILE)
        lines = out.strip().splitlines()
        assert lines == [
            "regular add(2, 3): 5",
            "curried add(2)(3): 5",
            "Hello, Ahsan!",
            "Hi, Hamza!",
        ]


# ---------------------------------------------------------------------------
# any_all.py
# ---------------------------------------------------------------------------

class TestAnyAll:
    FILE = f"{FOLDER}/any_all.py"

    def test_predicate_results(self):
        mod, _ = run_script(self.FILE)
        assert mod.any_passed is True
        assert mod.all_passed is True
        assert mod.has_python is True

    def test_empty_iterable_semantics(self):
        mod, _ = run_script(self.FILE)
        assert mod.any_passed is not None
        assert "any([]) is False" in _
        assert "all([]) is True" in _

    def test_printed_output_matches_flags(self):
        _, out = run_script(self.FILE)
        assert "Anyone scored 70+: True" in out
        assert "Everyone scored 40+: True" in out
        assert "Includes Python: True" in out


# ---------------------------------------------------------------------------
# itertools_module.py
# ---------------------------------------------------------------------------

class TestItertoolsModule:
    FILE = f"{FOLDER}/itertools_module.py"

    def test_building_blocks_produce_expected_lists(self):
        mod, _ = run_script(self.FILE)
        assert mod.combined == [1, 2, 3, 4, 5, 6]
        assert mod.natural == [1, 2, 3, 4, 5]
        assert mod.colours == ["red", "green", "blue", "red", "green", "blue"]
        assert mod.repeated == ["A", "A", "A", "A"]
        assert mod.outcomes == [(1, "head"), (1, "tail"), (2, "head"), (2, "tail")]

    def test_printed_output_matches_computed_lists(self):
        _, out = run_script(self.FILE)
        assert "chain: [1, 2, 3, 4, 5, 6]" in out
        assert "repeat: ['A', 'A', 'A', 'A']" in out
        assert "product: [(1, 'head'), (1, 'tail'), (2, 'head'), (2, 'tail')]" in out


# ---------------------------------------------------------------------------
# pure_functions.py
# ---------------------------------------------------------------------------

class TestPureFunctions:
    FILE = f"{FOLDER}/pure_functions.py"

    def test_pure_function_is_deterministic(self):
        mod, _ = run_script(self.FILE)
        assert mod.add_tax(10, 0.2) == 12.0
        assert mod.total_cost([5, 10, 15]) == 30

    def test_impure_function_mutates_external_state(self):
        mod, _ = run_script(self.FILE)
        assert mod.calls == 2

    def test_printed_output_in_call_order(self):
        _, out = run_script(self.FILE)
        lines = out.strip().splitlines()
        assert lines == [
            "add_tax(10, 0.2): 12.0",
            "add_tax(10, 0.2): 12.0",
            "total_cost([5, 10, 15]): 30",
            "next_number(): 1",
            "next_number(): 2",
        ]


# ---------------------------------------------------------------------------
# pipelines.py
# ---------------------------------------------------------------------------

class TestPipelines:
    FILE = f"{FOLDER}/pipelines.py"

    def test_pipeline_stages(self):
        mod, _ = run_script(self.FILE)
        assert mod.passing == [("Ahsan", 55), ("Hamza", 72), ("Bilal", 64), ("Alina", 91)]
        assert mod.boosted == [("Ahsan", 58), ("Hamza", 75), ("Bilal", 67), ("Alina", 94)]
        assert mod.ranked == [("Alina", 94), ("Hamza", 75), ("Bilal", 67), ("Ahsan", 58)]
        assert mod.winners == ["Alina", "Hamza"]
        assert mod.average == 64.0

    def test_source_data_is_unmodified(self):
        mod, _ = run_script(self.FILE)
        assert mod.students[2] == ("Zara", 38)

    def test_printed_output_matches_pipeline(self):
        _, out = run_script(self.FILE)
        assert "Ranked: [('Alina', 94), ('Hamza', 75), ('Bilal', 67), ('Ahsan', 58)]" in out
        assert "Winners: ['Alina', 'Hamza']" in out
        assert "Average score: 64.0" in out

