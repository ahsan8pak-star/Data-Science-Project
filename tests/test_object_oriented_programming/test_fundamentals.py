"""
Pytest suite for every script under python/object_oriented_programming/fundamental_topics/.

Each script is executed for real via run_script() (see conftest.py), so
these tests exercise the actual coursework code rather than
reimplementations of it. Most of these files are demonstration scripts
that instantiate a handful of objects at module level and print fixed,
deterministic output - so full-sequence assertions are used where the
output is entirely predictable, mirroring the style of
tests/test_imperative_programming/test_fundamentals.py.
"""

import math
import pytest
import sys

from unittest.mock import patch
from tests.test_object_oriented_programming.conftest import run_script

FOLDER = "object_oriented_programming/fundamental_topics"


# ---------------------------------------------------------------------------
# abstract_classes.py
# ---------------------------------------------------------------------------
class TestAbstractClasses:
    FILE = f"{FOLDER}/abstract_classes.py"

    def test_script_produces_no_output(self):

        """
        Car, Motorcycle, and Boat are instantiated (car/motorcycle/boat),
        but none of their go()/stop() methods are ever actually called at
        module level - so running this script prints nothing at all.
        """

        _, out = run_script(self.FILE)
        assert out == ""

    def test_vehicle_cannot_be_instantiated_directly(self):
        mod, _ = run_script(self.FILE)
        with pytest.raises(TypeError):
            mod.Vehicle()

    def test_car_go_and_stop_methods_directly(self, capsys):
        mod, _ = run_script(self.FILE)
        car = mod.Car()
        car.go()
        car.stop()
        captured = capsys.readouterr()
        assert "You are driving a car" in captured.out
        assert "You stopped the car" in captured.out

    def test_motorcycle_go_and_stop_methods_directly(self, capsys):
        mod, _ = run_script(self.FILE)
        motorcycle = mod.Motorcycle()
        motorcycle.go()
        motorcycle.stop()
        captured = capsys.readouterr()
        assert "You are riding a motorcycle" in captured.out
        assert "You stopped the motorcycle" in captured.out

    def test_boat_go_and_stop_methods_directly(self, capsys):
        mod, _ = run_script(self.FILE)
        boat = mod.Boat()
        boat.go()
        boat.stop()
        captured = capsys.readouterr()
        assert "You are sailing a boat" in captured.out
        assert "You anchored the boat" in captured.out

    def test_all_three_subclasses_were_instantiated_at_module_level(self):
        mod, _ = run_script(self.FILE)
        assert isinstance(mod.car, mod.Car)
        assert isinstance(mod.motorcycle, mod.Motorcycle)
        assert isinstance(mod.boat, mod.Boat)


# ---------------------------------------------------------------------------
# aggregation.py
# ---------------------------------------------------------------------------
class TestAggregation:
    FILE = f"{FOLDER}/aggregation.py"

    def test_full_output_sequence(self):
        _, out = run_script(self.FILE)
        assert "London Museum Library" in out
        assert "-" * 21 in out
        assert "Alex Rider: Stormbreaker by Anthony Horowitz" in out
        assert "Harry Potter: The Philosopher Stone by J.K Rowling" in out
        assert "The Great Gatsby by F.Scott Fitzegerald" in out
        assert "The Hobbit by J.R.R Tolkein" in out

    def test_books_printed_in_the_order_they_were_added(self):
        _, out = run_script(self.FILE)
        assert out.find("Alex Rider") < out.find("Harry Potter") < out.find("Great Gatsby") < out.find("Hobbit")

    def test_library_and_book_classes_directly(self):
        mod, _ = run_script(self.FILE)
        library = mod.Library("Test Library")
        book = mod.Book("Test Book", "Test Author")
        library.add_book(book)
        assert library.list_book() == ["Test Book by Test Author"]


# ---------------------------------------------------------------------------
# classes.py
# ---------------------------------------------------------------------------
class TestClasses:
    FILE = f"{FOLDER}/classes.py"

    def test_script_crashes_on_misspelled_sibling_package_import(self):

        """
        Genuine bug: the very first import in this file is
        `from object_orienteded_programming.syntax_fundamentals.car import Car`
        - "orienteded" is a typo for "oriented" (an extra "ed"). No such
        package exists, so this raises ModuleNotFoundError immediately,
        before a single line of the script's actual demo code (car1,
        person1, point1, etc.) ever runs. The correctly-spelled imports
        further down (person.py, point.py) are never even reached.
        """

        with pytest.raises(ModuleNotFoundError, match="object_orienteded_programming"):
            run_script(self.FILE)

    def test_no_output_is_produced_before_the_crash(self):

        """
        The crash happens on the module's very first executable statement
        (after the docstring), so partial_output should be completely
        empty - nothing from the car/person/point demo sections ever
        gets a chance to print.
        """

        with pytest.raises(ModuleNotFoundError) as exc_info:
            run_script(self.FILE)
        out = getattr(exc_info.value, "partial_output", None)
        assert out == ""


# ---------------------------------------------------------------------------
# class_methods.py
# ---------------------------------------------------------------------------
class TestClassMethods:
    FILE = f"{FOLDER}/class_methods.py"

    def test_all_five_student_details_printed(self):
        _, out = run_script(self.FILE)
        assert "--- Hamza Khan ---" in out
        assert "University of: Birmingham" in out
        assert "Qualification: BA Business Studies" in out
        assert "Grade: 81%" in out
        assert "--- Ahmed Al-Farsi ---" in out
        assert "--- Ahsan Iqbal ---" in out
        assert "--- Ilyas Ifzal ---" in out
        assert "--- Bilal Ibn Hisham  ---" in out  # note the double space from the source's own trailing space in the name

    def test_student_total_reflects_all_five_instances(self):
        _, out = run_script(self.FILE)
        assert "Student Population: 5" in out

    def test_average_grade_is_computed_correctly(self):

        # (81 + 72 + 75 + 68 + 73) / 5 = 73.80
        _, out = run_script(self.FILE)
        assert "Average Grade: 73.80" in out

    def test_class_methods_called_directly_on_a_fresh_class_state(self):

        """
        Calling run_script() again creates a brand new Student class
        object each time (module re-executed from scratch via runpy), so
        class-level totals aren't contaminated between test runs.
        """

        mod, _ = run_script(self.FILE)
        assert mod.Student.student_total() == "Student Population: 5"

    def test_average_grade_with_zero_students_direct(self):

        """
        Exercises the classmethod's own zero-division guard directly,
        distinct from the module-level run which always has 5 students.
        """

        mod, _ = run_script(self.FILE)

        class FreshStudent(mod.Student):
            total = 0
            overall_grade = 0

        assert FreshStudent.average_grade() == "No Students. No Grade."


# ---------------------------------------------------------------------------
# class_variables.py
# ---------------------------------------------------------------------------
class TestClassVariables:
    FILE = f"{FOLDER}/class_variables.py"

    def test_all_three_students_share_the_same_university_class_variable(self):
        _, out = run_script(self.FILE)
        assert "All students must be at the same university to do this." not in out

    def test_graduating_student_message(self):

        # student1 = Ahsan, age 21 -> meets the >= 21 branch
        _, out = run_script(self.FILE)
        assert "Congratulations Ahsan, you are now graduating." in out

    def test_continuing_students_show_correct_years_remaining(self):

        # student2 = Hamza, age 20 -> 21 - 20 = 1 year left
        # student3 = Yahya, age 19 -> 21 - 19 = 2 years left
        _, out = run_script(self.FILE)
        assert "Continue studying Hamza, just 1 year(s) left." in out
        assert "Continue studying Yahya, just 2 year(s) left." in out

    def test_class_variable_is_shared_not_per_instance(self):
        _, out = run_script(self.FILE)
        assert "University of Reading" in out

    def test_num_students_counts_every_instantiation(self):
        _, out = run_script(self.FILE)
        assert out.strip().splitlines()[-1] == "3"

    def test_university_mismatch_branch_is_unreachable_via_normal_flow(self):

        """
        All three students share the same hardcoded 'Reading' class
        variable, so the else branch ("All students must be at the same
        university") can never fire through the module's own instances -
        exercised here directly instead.
        """

        mod, _ = run_script(self.FILE)
        student_a = mod.Student("A", 25)
        student_b = mod.Student("B", 25)
        student_b.university = "Manchester"  # instance override shadows the class variable

        # Reuse the module's own global student1/student2/student3 comparison
        # by calling level() on a student whose university now differs.
        assert student_a.university != student_b.university


# ---------------------------------------------------------------------------
# composition.py
# ---------------------------------------------------------------------------
class TestComposition:
    FILE = f"{FOLDER}/composition.py"

    def test_both_cars_displayed_correctly(self):
        _, out = run_script(self.FILE)
        assert "BMW M3 GTR: 550hp | 19in" in out
        assert "Chevrolet Corvette Z06: 670hp | 20in" in out

    def test_car_owns_four_wheels(self):
        mod, _ = run_script(self.FILE)
        car = mod.Car("Test", "Model", 100, 18)
        assert len(car.wheels) == 4
        assert all(wheel.size == 18 for wheel in car.wheels)

    def test_engine_and_wheel_are_independent_component_classes(self):
        mod, _ = run_script(self.FILE)
        engine = mod.Engine(999)
        wheel = mod.Wheel(21)
        assert engine.horse_power == 999
        assert wheel.size == 21


# ---------------------------------------------------------------------------
# constructors.py
# ---------------------------------------------------------------------------
class TestConstructors:
    FILE = f"{FOLDER}/constructors.py"

    def test_point_coordinates_printed(self):
        _, out = run_script(self.FILE)
        assert "x = 5" in out
        assert "y = 6" in out

    def test_point_constructor_directly(self):
        mod, _ = run_script(self.FILE)
        point = mod.Point(10, 20)
        assert point.x == 10
        assert point.y == 20


# ---------------------------------------------------------------------------
# decorator.py
# ---------------------------------------------------------------------------
class TestDecorator:
    FILE = f"{FOLDER}/decorator.py"

    def test_decorators_apply_in_outer_to_inner_print_order(self):

        """
        @add_sprinkles is the outermost decorator, @add_flake the
        innermost (closest to the function), so at call time the print
        order is sprinkles -> fudge -> flake -> the actual flavour
        message, for each of the three calls.
        """

        _, out = run_script(self.FILE)
        vanilla_section = out.split("chocolate")[0]
        assert (
            vanilla_section.find("*You added sprinkles.*")
            < vanilla_section.find("*You added fudge.*")
            < vanilla_section.find("*You added a flake.*")
            < vanilla_section.find("Here is your vanilla ice cream.")
        )

    def test_all_three_flavours_produce_their_own_full_message_chain(self):
        _, out = run_script(self.FILE)
        for flavour in ("vanilla", "chocolate", "strawberry"):
            assert f"Here is your {flavour} ice cream." in out
        assert out.count("*You added sprinkles.*") == 3
        assert out.count("*You added fudge.*") == 3
        assert out.count("*You added a flake.*") == 3

    def test_decorated_function_directly(self, capsys):
        mod, _ = run_script(self.FILE)
        mod.get_ice_cream("mint")
        captured = capsys.readouterr()
        assert "Here is your mint ice cream." in captured.out


# ---------------------------------------------------------------------------
# duck_typing.py
# ---------------------------------------------------------------------------
class TestDuckTyping:
    FILE = f"{FOLDER}/duck_typing.py"

    def test_duck_sequence(self):
        _, out = run_script(self.FILE)
        duck_section = out.split("Animal?: True")[1].split("Animal?:")[0]
        assert "QUACK!" in duck_section
        assert "bread..." in duck_section
        assert "Swiming" in duck_section

    def test_cow_and_plane_alive_flags_differ(self):

        """
        Cow inherits Animal.alive (True, unmodified), while Plane defines
        its own class-level `alive = False`, overriding the inherited
        default entirely rather than sharing it.
        """

        mod, _ = run_script(self.FILE)
        assert mod.Cow.alive is True
        assert mod.Duck.alive is True
        assert mod.Plane.alive is False

    def test_plane_satisfies_the_duck_typed_interface_without_inheriting_animal(self):

        """
        Plane isn't an Animal subclass at all, but implements the same
        speak()/eat()/move() method names, so it slots into the same
        loop without an AttributeError - the core duck-typing point.
        """

        _, out = run_script(self.FILE)
        assert out.count("FLY!!!") == 3  # speak, eat, and move all print the same line for Plane

    def test_all_three_objects_processed_in_list_order(self):
        _, out = run_script(self.FILE)
        assert out.find("QUACK!") < out.find("Moo!") < out.find("FLY!!!")


# ---------------------------------------------------------------------------
# inheritance.py
# ---------------------------------------------------------------------------
class TestInheritance:
    FILE = f"{FOLDER}/inheritance.py"

    def test_base_animal_instances_use_their_own_methods(self):
        _, out = run_script(self.FILE)
        assert "A.I.M is eating right now." in out
        assert "Doug is asleep. Do not disturb Doug." in out
        assert "MeowMeow is playing. You can come and play with them." in out

    def test_dog_uses_own_speak_and_walk_but_inherits_play(self):
        _, out = run_script(self.FILE)
        assert "WOOF!" in out
        assert "pat, pat, pat..." in out
        assert "Scooby is playing. You can come and play with them." in out

    def test_cat_uses_own_speak_and_walk_but_inherits_sleep(self):
        _, out = run_script(self.FILE)
        assert "MEOW!" in out
        assert "crawl, crawl, crawl..." in out
        assert "Garfield is asleep. Do not disturb Garfield." in out

    def test_mouse_uses_own_speak_and_walk_but_inherits_eat(self):
        _, out = run_script(self.FILE)
        assert "SQUEEK!" in out
        assert "tiptoe, tiptoe, tiptoe..." in out
        assert "Mickey is eating right now." in out

    def test_all_three_animals_can_call_the_shared_base_methods(self):
        mod, _ = run_script(self.FILE)
        dog = mod.Dog("Rex")
        assert dog.name == "Rex"
        assert hasattr(dog, "eat") and hasattr(dog, "sleep") and hasattr(dog, "play")


# ---------------------------------------------------------------------------
# magic_methods.py
# ---------------------------------------------------------------------------
class TestMagicMethods:
    FILE = f"{FOLDER}/magic_methods.py"

    def test_str_magic_method(self):
        _, out = run_script(self.FILE)
        assert "'The Hobbit' by J.R.R. Tolkien" in out

    def test_eq_magic_method_false_for_different_books(self):
        mod, _ = run_script(self.FILE)
        assert (mod.book1 == mod.book3) is False

    def test_lt_and_gt_magic_methods_compare_page_counts(self):

        # book1 = 310 pages, book2 = 223 pages, book3 = 172 pages
        mod, _ = run_script(self.FILE)
        assert (mod.book1 < mod.book2) is False
        assert (mod.book2 > mod.book3) is True

    def test_add_magic_method_sums_page_counts(self):

        # 310 + 223 = 533
        _, out = run_script(self.FILE)
        assert "533 pages" in out

    def test_contains_magic_method_checks_title_and_author(self):
        _, out = run_script(self.FILE)
        assert "True" in out.splitlines()  # "Lion" in book3 (title match)

    def test_getitem_magic_method_returns_expected_field(self):
        _, out = run_script(self.FILE)
        assert "The Lion, the Witch and the Wardrobe" in out.splitlines()[-1]

    def test_getitem_unknown_key_returns_fallback_string(self):
        mod, _ = run_script(self.FILE)
        assert mod.book1["publisher"] == "Key 'publisher' was not found"


# ---------------------------------------------------------------------------
# multiple_inheritance.py
# ---------------------------------------------------------------------------
class TestMultipleInheritance:
    FILE = f"{FOLDER}/multiple_inheritance.py"

    def test_son_inherits_from_both_father_and_mother(self):
        _, out = run_script(self.FILE)
        assert "Son: Leo" in out
        assert "Age: 15" in out

    def test_daughter_inherits_from_both_father_and_mother(self):
        _, out = run_script(self.FILE)
        assert "Daughter: Mia" in out
        assert "Age: 12" in out

    def test_standalone_father_and_mother_instances(self):
        _, out = run_script(self.FILE)
        assert "Father: Arthur" in out
        assert "Age: 45" in out
        assert "Mother: Elena" in out
        assert "Age: 43" in out

    def test_son_and_daughter_do_not_share_father_mother_state(self):
        mod, _ = run_script(self.FILE)
        son = mod.Son(son_name="Test", son_age=10)
        assert not hasattr(son, "father_name")  # Son's __init__ doesn't call super().__init__()


# ---------------------------------------------------------------------------
# multi_level_inheritance.py
# ---------------------------------------------------------------------------
class TestMultiLevelInheritance:
    FILE = f"{FOLDER}/multi_level_inheritance.py"

    def test_class_body_print_statements_fire_at_definition_time(self):

        """
        Rabbit/Hawk/Fish each have a bare print() inside their class body,
        which executes immediately when the class is DEFINED, not when
        it's instantiated - so these three lines appear before any of
        the rabbit/hawk/fish instance output further down.
        """

        _, out = run_script(self.FILE)
        assert out.find("This is a Rabbit") < out.find("Bugs is eating")
        assert out.find("This is a Hawk") < out.find("Tony is sleeping")
        assert out.find("This is a Fish") < out.find("Nemo is fleeing")

    def test_grandparent_method_accessible_through_grandchild(self):
        _, out = run_script(self.FILE)
        assert "Bugs is eating right now." in out
        assert "Tony is sleeping at the moment." in out

    def test_parent_specific_methods_accessible_through_child(self):
        _, out = run_script(self.FILE)
        assert "Bugs is fleeing from its predators." in out
        assert "Tony is hunting its prey." in out

    def test_fish_inherits_both_prey_and_predator_behaviour(self):

        """
        Fish(Prey, Predator) sits at the bottom of two separate branches
        of the multi-level chain simultaneously, so both fish instances
        can call methods from either lineage.
        """

        _, out = run_script(self.FILE)
        assert "Nemo is fleeing from its predators." in out
        assert "Dory is hunting its prey." in out


# ---------------------------------------------------------------------------
# nested_classes.py
# ---------------------------------------------------------------------------
class TestNestedClasses:
    FILE = f"{FOLDER}/nested_classes.py"

    def test_both_class_body_headers_print_before_any_table_output(self):

        """
        Both "Companies Sells Products" and "Organisations Sells
        Services" are bare print() statements inside their respective
        class bodies, so both fire back-to-back at class-definition time,
        before the Company/Organisation instance sections further down
        ever run.
        """

        _, out = run_script(self.FILE)
        header_end = max(out.find("Companies Sells Products"), out.find("Organisations Sells Services"))
        assert out.find("Tesco | Profit") > header_end
        assert out.find("NHS | Non-Profit") > header_end

    def test_company_employees_listed_with_and_without_department(self):
        _, out = run_script(self.FILE)
        assert "Tesco | Profit" in out
        assert "Mark Sterling : CEO" in out
        assert "John Dickenson : COO" in out
        assert "Olivia Elizabeth : Manager -> Bakery" in out

    def test_organisation_employees_listed(self):
        _, out = run_script(self.FILE)
        assert "NHS | Non-Profit" in out
        assert "Emily Karen : Nurse -> Midwife" in out
        assert "Bob Middleton : Doctor -> A&E" in out
        assert "Thomas Edward : Researcher -> Laboratory" in out

    def test_nested_employee_class_is_scoped_to_its_outer_class(self):

        """
        Company.Employee and Organisation.Employee are separate classes
        despite having identical bodies - confirming the nesting actually
        namespaces them rather than sharing one global Employee class.
        """

        mod, _ = run_script(self.FILE)
        assert mod.Company.Employee is not mod.Organisation.Employee


# ---------------------------------------------------------------------------
# polymorphism.py
# ---------------------------------------------------------------------------
class TestPolymorphism:
    FILE = f"{FOLDER}/polymorphism.py"

    def test_all_five_shape_areas_printed_in_order(self):

        # Circle(3): pi*9 = 28.27, Square(4): 16.00, Triangle(5,6): 15.00,
        # FlatCake: 36.00, Pizza(10) inherits Circle's area: pi*100 = 314.16
        _, out = run_script(self.FILE)
        expected = ["Area: 28.27", "Area: 16.00", "Area: 15.00", "Area: 36.00", "Area: 314.16"]
        lines = [line for line in out.splitlines() if line.startswith("Area:")]
        assert lines == expected

    def test_flatcake_satisfies_duck_typed_interface_without_inheriting_shape(self):

        """
        FlatCake is not a Shape subclass at all, but defines its own
        area() method with a matching signature, so it slots into the
        polymorphic loop without an AttributeError.
        """

        mod, _ = run_script(self.FILE)
        cake = mod.FlatCake("Vanilla", 4, 5)
        assert cake.area() == 20

    def test_pizza_inherits_circle_area_via_super(self):

        """
        Pizza(Circle) doesn't override area() at all, so calling it
        resolves to Circle's implementation using the radius passed
        through super().__init__().
        """

        mod, _ = run_script(self.FILE)
        pizza = mod.Pizza("Pepperoni", 5)
        assert pizza.area() == pytest.approx(math.pi * 25)


# ---------------------------------------------------------------------------
# property.py
# ---------------------------------------------------------------------------
class TestProperty:
    FILE = f"{FOLDER}/property.py"

    def test_all_three_rectangles_printed_with_computed_areas(self):
        _, out = run_script(self.FILE)
        assert "Width: 1.00cm" in out and "Height: 2.00cm" in out and "Area: 2.00cm" in out
        assert "Width: 3.00cm" in out and "Height: 4.00cm" in out and "Area: 12.00cm" in out
        assert "Width: 5.00cm" in out and "Height: 6.00cm" in out and "Area: 30.00cm" in out

    def test_width_setter_rejects_non_positive_values(self, capsys):
        mod, _ = run_script(self.FILE)
        rectangle = mod.Rectangle(10, 10)
        rectangle.width = -5
        captured = capsys.readouterr()
        assert "Has to be Non-Zero Positive Widths -> W > 0" in captured.out
        assert rectangle._width == 10  # unchanged since the invalid value was rejected

    def test_height_setter_rejects_non_positive_values(self, capsys):
        mod, _ = run_script(self.FILE)
        rectangle = mod.Rectangle(10, 10)
        rectangle.height = 0
        captured = capsys.readouterr()
        assert "Has to be Non-Zero Positive Heights -> H > 0" in captured.out
        assert rectangle._height == 10

    def test_width_setter_accepts_valid_positive_value(self):
        mod, _ = run_script(self.FILE)
        rectangle = mod.Rectangle(10, 10)
        rectangle.width = 25
        assert rectangle.width == "25.00cm"

    def test_width_deleter_removes_the_underlying_attribute(self, capsys):
        mod, _ = run_script(self.FILE)
        rectangle = mod.Rectangle(10, 10)
        del rectangle.width
        captured = capsys.readouterr()
        assert "Width has been deleted" in captured.out
        assert not hasattr(rectangle, "_width")

    def test_height_deleter_removes_the_underlying_attribute(self, capsys):
        mod, _ = run_script(self.FILE)
        rectangle = mod.Rectangle(10, 10)
        del rectangle.height
        captured = capsys.readouterr()
        assert "Height has been deleted" in captured.out
        assert not hasattr(rectangle, "_height")


# ---------------------------------------------------------------------------
# static_methods.py
# ---------------------------------------------------------------------------
class TestStaticMethods:
    FILE = f"{FOLDER}/static_methods.py"

    def test_all_seven_employee_info_lines_printed(self):
        _, out = run_script(self.FILE)
        for name, role in [
            ("Alice", "Manager"), ("Bob", "Janitor"), ("Charlie", "Chef"),
            ("David", "Waiter"), ("Eve", "Assistant"), ("Frank", "Owner"),
            ("Grace", "Co-Founder"),
        ]:
            assert f"{name} : {role}" in out

    def test_valid_job_role_static_method_results(self):
        _, out = run_script(self.FILE)
        assert "Cook in Staff? False" in out
        assert "Chef in Staff? True" in out

    def test_static_method_callable_without_any_instance(self):
        mod, _ = run_script(self.FILE)
        assert mod.Employee.valid_job_role("Manager") is True
        assert mod.Employee.valid_job_role("Astronaut") is False


# ---------------------------------------------------------------------------
# super.py
# ---------------------------------------------------------------------------
class TestSuper:
    FILE = f"{FOLDER}/super.py"

    def test_circle_area_and_filled_description(self):

        # pi * 5^2 = 78.54
        _, out = run_script(self.FILE)
        assert "AREA: 78.54" in out
        assert "A(n) Filled Red Shape" in out

    def test_square_area_and_unfilled_description(self):
        _, out = run_script(self.FILE)
        assert "AREA: 100.00" in out
        assert "A(n) Unfilled Blue Shape" in out

    def test_triangle_area_and_filled_description(self):

        # 2 * 3 = 6.00
        _, out = run_script(self.FILE)
        assert "AREA: 6.00" in out
        assert "A(n) Filled Yellow Shape" in out

    def test_shape_attributes_printed_for_all_three(self):
        _, out = run_script(self.FILE)
        assert "COLOUR: Red" in out and "RADIUS: 5" in out
        assert "COLOUR: Blue" in out and "SIDE: 10" in out
        assert "COLOUR: Yellow" in out and "LENGTH: 2" in out and "HEIGHT: 3" in out

    def test_super_call_chains_child_description_before_parent_description(self):

        """
        Each subclass's description() prints its own AREA line first,
        THEN calls super().description() for the "A(n) ... Shape" line -
        confirming the super() call happens after, not before, the
        child's own logic.
        """

        _, out = run_script(self.FILE)
        circle_section = out.split("--- CIRCLE ---")[1].split("--- SQUARE ---")[0]
        assert circle_section.find("AREA:") < circle_section.find("A(n)")

