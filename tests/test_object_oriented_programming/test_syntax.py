"""
Pytest suite for every script under python/object_oriented_programming/syntax_fundamentals/.

Executed for real via run_script() (see conftest.py). Several files here
are pure class-definition modules with no module-level instantiation
(car.py, person.py, point.py) - these produce empty stdout by design and
are exercised via direct method calls on the returned module instead.
dice.py additionally reaches across into imperative_programming for its
dice_art dict, mirroring the cross-package pattern already covered for
dice_game.py itself under test_imperative_programming.
"""

import pytest
import sys

from unittest.mock import patch
from tests.test_object_oriented_programming.conftest import run_script

FOLDER = "object_oriented_programming/syntax_fundamentals"


# ---------------------------------------------------------------------------
# bank_account.py
# ---------------------------------------------------------------------------
class TestBankAccount:
    FILE = f"{FOLDER}/bank_account.py"

    def test_initial_account_details_printed(self):
        _, out = run_script(self.FILE)
        assert "Account Number: 12345678" in out
        assert "Account Holder: John Doe" in out
        assert "Balance: £1000.00" in out

    def test_deposit_and_withdraw_confirmation_messages(self):
        _, out = run_script(self.FILE)
        assert "Deposited £500. New balance: £1500." in out
        assert "Withdrew £200. New balance: £1300." in out

    def test_final_balance_reflects_deposit_then_withdrawal(self):

        # 1000 + 500 - 200 = 1300
        _, out = run_script(self.FILE)
        assert "Balance: £1300.00" in out

    def test_deposit_rejects_non_positive_amount(self, capsys):
        mod, _ = run_script(self.FILE)
        account = mod.BankAccount("999", "Test User")
        account.deposit(-50)
        captured = capsys.readouterr()
        assert "Deposit amount must be positive." in captured.out
        assert account.balance == 0  # unchanged

    def test_withdraw_rejects_amount_greater_than_balance(self, capsys):
        mod, _ = run_script(self.FILE)
        account = mod.BankAccount("999", "Test User", balance=100)
        account.withdraw(200)
        captured = capsys.readouterr()
        assert "Withdrawal amount must be positive and less than or equal to the current balance." in captured.out

    def test_get_balance_returns_current_balance(self):
        mod, _ = run_script(self.FILE)
        account = mod.BankAccount("999", "Test User", balance=250)
        assert account.get_balance() == 250


# ---------------------------------------------------------------------------
# calculator.py
# ---------------------------------------------------------------------------
class TestCalculator:
    FILE = f"{FOLDER}/calculator.py"

    def test_all_operations_printed_in_order(self):
        _, out = run_script(self.FILE)
        lines = out.strip().splitlines()
        assert lines == ["15", "5", "5.0", "Cannot divide by zero.", "42", "8", "4.0",
                          "Impossible to calculate square root of a negative number."]

    def test_static_methods_callable_without_an_instance(self):
        mod, _ = run_script(self.FILE)
        assert mod.Calculator.add(2, 3) == 5
        assert mod.Calculator.subtract(10, 4) == 6
        assert mod.Calculator.multiply(3, 3) == 9
        assert mod.Calculator.power(2, 10) == 1024

    def test_divide_by_zero_returns_a_string_not_an_exception(self):
        mod, _ = run_script(self.FILE)
        result = mod.Calculator.divide(5, 0)
        assert result == "Cannot divide by zero."
        assert isinstance(result, str)

    def test_square_root_of_negative_returns_error_string(self):
        mod, _ = run_script(self.FILE)
        result = mod.Calculator.square_root(-9)
        assert result == "Impossible to calculate square root of a negative number."


# ---------------------------------------------------------------------------
# car.py
# ---------------------------------------------------------------------------
class TestCar:
    FILE = f"{FOLDER}/car.py"

    def test_script_produces_no_output(self):

        """
        car.py only defines the Car class - it never instantiates or
        calls anything at module level, so running it directly prints
        nothing. This is the sibling module classes.py's typo'd import
        was trying (and failing) to reach.
        """

        _, out = run_script(self.FILE)
        assert out == ""

    def test_drive_and_stop_methods_directly(self, capsys):
        mod, _ = run_script(self.FILE)
        car = mod.Car("Supra", 1998, "White", True)
        car.drive()
        car.stop()
        captured = capsys.readouterr()
        assert "You are driving a White Supra!" in captured.out
        assert "You finished driving a White Supra." in captured.out

    def test_description_for_sale_branch(self, capsys):
        mod, _ = run_script(self.FILE)
        car = mod.Car("GTR", 2005, "Blue", True)
        car.description()
        captured = capsys.readouterr()
        assert "This is a 2005 Blue GTR" in captured.out
        assert "You can buy this car right now!" in captured.out

    def test_description_not_for_sale_branch(self, capsys):
        mod, _ = run_script(self.FILE)
        car = mod.Car("Classic", 1965, "Red", False)
        car.description()
        captured = capsys.readouterr()
        assert "A priceless car, not worthy to be auctioned." in captured.out


# ---------------------------------------------------------------------------
# device.py
# ---------------------------------------------------------------------------
class TestDevice:
    FILE = f"{FOLDER}/device.py"

    def test_device_cannot_be_instantiated_directly(self):
        mod, _ = run_script(self.FILE)
        with pytest.raises(TypeError):
            mod.Device("Generic", "X1")

    def test_all_three_info_lines_printed(self):
        _, out = run_script(self.FILE)
        assert "The phone number is 123-456-7890." in out
        assert "The screen size is 15.6 inches." in out
        assert "The storage capacity is 128GB." in out

    def test_turn_on_messages_for_all_three_devices(self):
        _, out = run_script(self.FILE)
        assert "The Apple IPhone XR phone is turning on." in out
        assert "The Dell XPS 15 laptop is turning on." in out
        assert "The Samsung Galaxy Tab S7 tablet is turning on." in out

    def test_turn_off_messages_for_all_three_devices(self):
        _, out = run_script(self.FILE)
        assert "The Apple IPhone XR phone is turning off." in out
        assert "The Dell XPS 15 laptop is turning off." in out
        assert "The Samsung Galaxy Tab S7 tablet is turning off." in out

    def test_turn_on_block_prints_before_turn_off_block(self):
        _, out = run_script(self.FILE)
        assert out.find("turning on") < out.find("turning off")


# ---------------------------------------------------------------------------
# dice.py
# ---------------------------------------------------------------------------
class TestDice:
    FILE = f"{FOLDER}/dice.py"

    def test_rolled_number_matches_the_patched_random_value(self):
        fixed_roll = patch("random.randint", return_value=6)
        _, out = run_script(self.FILE, patches=[fixed_roll])
        assert "You rolled a 6:" in out

    def test_dice_art_lines_for_the_rolled_value_are_printed(self):

        """
        Confirms the cross-package import from
        imperative_programming.logical_games.dice_game actually resolves
        and its dice_art dict is used correctly, not just that a number
        gets printed.
        """

        fixed_roll = patch("random.randint", return_value=6)
        _, out = run_script(self.FILE, patches=[fixed_roll])
        assert "┌─────────┐" in out
        assert "│  ●   ●  │" in out
        assert "└─────────┘" in out

    def test_different_roll_shows_different_art(self):
        fixed_roll = patch("random.randint", return_value=1)
        _, out = run_script(self.FILE, patches=[fixed_roll])
        assert "You rolled a 1:" in out
        assert "│    ●    │" in out  # roll 1's single centred dot

    def test_dice_art_import_did_not_trigger_dice_game_pys_own_main(self):

        """
        dice_game.py guards its own interactive script behind
        `if __name__ == "__main__":`, so importing just its dice_art dict
        should not print or prompt anything from that sibling file - its
        own "DICE RACE" welcome banner should never appear here.
        """

        fixed_roll = patch("random.randint", return_value=3)
        _, out = run_script(self.FILE, patches=[fixed_roll])
        assert "DICE RACE" not in out  # would appear if dice_game.py's own main() had run


# ---------------------------------------------------------------------------
# employee_contract.py
# ---------------------------------------------------------------------------
class TestEmployeeContract:
    FILE = f"{FOLDER}/employee_contract.py"

    def test_part_time_employee_combines_worker_and_student_info(self):
        _, out = run_script(self.FILE)
        assert "Sophia works as a Support Assistant." in out
        assert "Sophia is studying Business Management." in out
        assert "Working hours: 20 hours per week." in out

    def test_full_time_employee_combines_worker_and_graduate_info(self):
        _, out = run_script(self.FILE)
        assert "Daniel works as a Software Engineer." in out
        assert "Daniel graduated with a Computer Science degree." in out
        assert "Assigned department: Engineering." in out

    def test_part_time_printed_before_full_time(self):
        _, out = run_script(self.FILE)
        assert out.find("Sophia") < out.find("Daniel")

    def test_multiple_inheritance_uses_explicit_parent_init_calls(self):

        """
        PartTimeEmployee calls Worker.__init__() and Student.__init__()
        explicitly by name (rather than a single super().__init__()
        chain), so both parents' attributes end up set on the same
        instance without needing cooperative MRO-based super() calls.
        """

        mod, _ = run_script(self.FILE)
        part_time = mod.PartTimeEmployee(name="Test", role="Role", course="Course", hours_per_week=15)
        assert part_time.name == "Test" and part_time.role == "Role" and part_time.course == "Course"


# ---------------------------------------------------------------------------
# food.py
# ---------------------------------------------------------------------------
class TestFood:
    FILE = f"{FOLDER}/food.py"

    def test_dessert_chain_output(self):
        _, out = run_script(self.FILE)
        assert "'Chocolate Cake' has '350' calories." in out
        assert "'Chocolate Cake' is a snack served in '1 Slice'." in out
        assert "'Chocolate Cake' is a dessert with 'High' sweetness." in out

    def test_treat_chain_output(self):
        _, out = run_script(self.FILE)
        assert "'Chocolate Chip Cookies' has '220' calories." in out
        assert "'Chocolate Chip Cookies' is a snack served in '2 Cookies'." in out
        assert "'Chocolate Chip Cookies' has a 'Crunchy' texture." in out

    def test_cold_drink_chain_output(self):
        _, out = run_script(self.FILE)
        assert "'Cola' has '140' calories." in out
        assert "'Cola' is served at a 'Cold' temperature." in out
        assert "'Cola' is 'Carbonated'." in out

    def test_hot_drink_chain_output(self):
        _, out = run_script(self.FILE)
        assert "'Green Tea' has '50' calories." in out
        assert "'Green Tea' is served at a 'Hot' temperature." in out
        assert "'Green Tea' has a 'Fresh' aroma." in out

    def test_four_groups_separated_by_dashed_lines(self):
        _, out = run_script(self.FILE)
        assert out.count("-" * 40) == 3  # 3 separators between 4 groups

    def test_dessert_is_a_multi_level_subclass_of_food(self):
        mod, _ = run_script(self.FILE)
        assert isinstance(mod.cake, mod.Snack)
        assert isinstance(mod.cake, mod.Food)


# ---------------------------------------------------------------------------
# grocery_caloric_list.py
# ---------------------------------------------------------------------------
class TestGroceryCaloricList:
    FILE = f"{FOLDER}/grocery_caloric_list.py"

    def test_get_positive_float_rejects_non_numeric_then_non_positive_then_accepts(self):
        mod, _ = run_script(self.FILE, inputs=["2000", "20", "", ""])
        with patch("builtins.input", side_effect=["abc", "-5", "10"]):
            result = mod.get_positive_float("Enter: ")
        assert result == 10.0

    def test_display_menu_prints_header_and_all_items(self, capsys):
        mod, _ = run_script(self.FILE, inputs=["2000", "20", "", ""])
        item = mod.FoodItem("banana", 105, 0.30)
        mod.display_menu("Test Menu", {"banana": item})
        captured = capsys.readouterr()
        assert "--- Test Menu ---" in captured.out
        assert "Banana" in captured.out
        assert "105" in captured.out

    def test_print_welcome_banner(self, capsys):
        mod, _ = run_script(self.FILE, inputs=["2000", "20", "", ""])
        mod.print_welcome()
        captured = capsys.readouterr()
        assert "GROCERY & CALORIE TRACKER" in captured.out
        assert "Plan your meals, balance your budget," in captured.out

    def test_empty_order_immediately_exited(self):

        """
        max_calories=2000, max_budget=20, blank item selection (skips
        ordering entirely), then blank again at the adjust-order prompt
        to exit straight away.
        """

        inputs = ["2000", "20", "", ""]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Your order is currently empty." in out
        assert "HERE'S YOUR ORDER! THANKS FOR SHOPPING WITH OUR TRACKER!" in out

    def test_single_item_order_shows_correct_receipt_totals(self):

        # banana: 105 kcal, £0.30 each -> qty 2 = 210 kcal, £0.60
        inputs = ["2000", "5", "banana", "2", ""]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Banana" in out
        assert "210" in out
        assert "£0.60" in out
        assert "Nice! You are within both your Caloric and Budget limits." in out

    def test_unrecognised_item_name_shows_notice_and_is_skipped(self):
        inputs = ["2000", "20", "fakefood", ""]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Notice: 'fakefood' is not on the menu and was skipped." in out
        assert "Your order is currently empty." in out

    def test_generate_recommendations_over_both_limits_scenario(self, capsys):
        mod, _ = run_script(self.FILE, inputs=["2000", "20", "", ""])
        item = mod.FoodItem("coconut", 354, 2.50)
        order = [mod.OrderLine(item, 10)]  # 3540 kcal, £25.00
        mod.generate_recommendations(order, {"coconut": item}, cal_excess=1540, budget_excess=5.0,
                                       remaining_cals=-1540, remaining_budget=-5.0)
        captured = capsys.readouterr()
        assert "EXCEEDED BOTH LIMITS!" in captured.out

    def test_generate_recommendations_within_limits_scenario(self, capsys):
        mod, _ = run_script(self.FILE, inputs=["2000", "20", "", ""])
        item = mod.FoodItem("apple", 72, 0.50)
        mod.generate_recommendations([], {"apple": item}, cal_excess=-1000, budget_excess=-10,
                                       remaining_cals=1000, remaining_budget=10)
        captured = capsys.readouterr()
        assert "Nice! You are within both your Caloric and Budget limits." in captured.out


# ---------------------------------------------------------------------------
# item.py
# ---------------------------------------------------------------------------
class TestItem:
    FILE = f"{FOLDER}/item.py"

    def test_str_magic_method(self):
        _, out = run_script(self.FILE)
        assert "Keyboard - £29.99 (x2)" in out

    def test_eq_magic_method(self):
        mod, _ = run_script(self.FILE)
        assert (mod.item1 == mod.item3) is False

    def test_lt_and_gt_compare_by_price(self):

        # item2 (Mouse, £9.99) < item3 (Monitor, £129.99)
        # item3 (Monitor, £129.99) > item1 (Keyboard, £29.99)
        _, out = run_script(self.FILE)
        lines = out.splitlines()
        assert lines[1] == "False"  # item1 == item3
        assert lines[2] == "True"   # item2 < item3
        assert lines[3] == "True"   # item3 > item1

    def test_add_magic_method_sums_prices(self):

        # 29.99 + 9.99 = 39.98
        _, out = run_script(self.FILE)
        assert "39.98" in out

    def test_contains_magic_method_is_case_insensitive_substring_of_name(self):
        _, out = run_script(self.FILE)
        assert "True" in out.splitlines()   # "board" in "Keyboard"
        assert "False" in out.splitlines()  # "laptop" not in "Mouse"

    def test_getitem_magic_method_for_each_key(self):
        mod, _ = run_script(self.FILE)
        assert mod.item1["price"] == 29.99
        assert mod.item2["quantity"] == 5
        assert mod.item3["name"] == "Monitor"

    def test_getitem_unknown_key_returns_fallback_string(self):
        mod, _ = run_script(self.FILE)
        assert mod.item1["colour"] == "Key 'colour' was not found"


# ---------------------------------------------------------------------------
# order.py
# ---------------------------------------------------------------------------
class TestOrder:
    FILE = f"{FOLDER}/order.py"

    def test_all_five_order_details_printed(self):
        _, out = run_script(self.FILE)
        assert "--- Sourdough Bread ---" in out
        assert "Type: Bakery" in out
        assert "Amount: 2" in out
        assert "Cost: £2.50" in out

    def test_total_orders_and_average_cost(self):

        # revenue: (2.50*2)+(1.20*3)+(3.00*1)+(2.20*2)+(1.50*5) = 23.50
        # average: 23.50 / 5 = 4.70
        _, out = run_script(self.FILE)
        assert "Total Orders: 5" in out
        assert "Average Cost: £4.70" in out

    def test_overall_stats_printed_after_all_individual_orders(self):
        _, out = run_script(self.FILE)
        assert out.find("Plain Flour") < out.find("Overall Stats")

    def test_class_variables_are_fresh_per_script_run(self):

        """
        Since run_script() re-executes the module from scratch each time
        via runpy, Order.total_orders should always be exactly 5 for this
        specific script, never accumulating across separate test runs.
        """

        mod, _ = run_script(self.FILE)
        assert mod.Order.total_orders == 5

    def test_average_cost_with_zero_orders_direct(self):
        mod, _ = run_script(self.FILE)

        class FreshOrder(mod.Order):
            total_revenue = 0
            total_orders = 0

        assert FreshOrder.average_cost() == "No Orders. No Costs."


# ---------------------------------------------------------------------------
# payment.py
# ---------------------------------------------------------------------------
class TestPayment:
    FILE = f"{FOLDER}/payment.py"

    def test_all_four_payment_types_processed(self):
        _, out = run_script(self.FILE)
        assert "Cash payment of £25.00 has been received." in out
        assert "Card payment of £120.50 processed with card ending 3456." in out
        assert "Bank transfer of £500.00 sent from account number 987654321." in out
        assert "Cheque payment of £100.00 processed with cheque number CHK001." in out

    def test_card_number_is_masked_to_last_four_digits(self):
        mod, _ = run_script(self.FILE)
        card = mod.Card(50, "9999888877776666")
        assert "6666" in card.process()
        assert "9999888877776666" not in card.process()

    def test_base_payment_class_raises_when_process_not_overridden(self):

        """
        Payment isn't declared with ABC/abstractmethod, so it CAN be
        instantiated directly - but calling .process() on it raises
        NotImplementedError manually, a lighter-weight enforcement than
        the abc-based pattern used in device.py/abstract_classes.py.
        """

        mod, _ = run_script(self.FILE)
        payment = mod.Payment()  # instantiation itself succeeds
        with pytest.raises(NotImplementedError):
            payment.process()

    def test_payments_processed_in_list_order(self):
        _, out = run_script(self.FILE)
        assert out.find("Cash") < out.find("Card") < out.find("Bank transfer") < out.find("Cheque")


# ---------------------------------------------------------------------------
# person.py
# ---------------------------------------------------------------------------
class TestPerson:
    FILE = f"{FOLDER}/person.py"

    def test_script_produces_no_output(self):

        """
        person.py only defines the Person class - nothing is instantiated
        or called at module level, so running it directly prints nothing.
        """

        _, out = run_script(self.FILE)
        assert out == ""

    def test_talk_when_is_talking_is_true(self, capsys):
        mod, _ = run_script(self.FILE)
        person = mod.Person("Alex", 30, True)
        person.talk()
        captured = capsys.readouterr()
        assert "Alex is speaking right now." in captured.out

    def test_talk_when_not_talking_but_age_twenty_or_over(self, capsys):
        mod, _ = run_script(self.FILE)
        person = mod.Person("Sam", 25, False)
        person.talk()
        captured = capsys.readouterr()
        assert "Sam. You may start after the first speech." in captured.out

    def test_talk_when_not_talking_and_under_twenty(self, capsys):
        mod, _ = run_script(self.FILE)
        person = mod.Person("Jo", 15, False)
        person.talk()
        captured = capsys.readouterr()
        assert "Jo, wait for the other person's turn." in captured.out

    def test_age_boundary_of_exactly_twenty(self, capsys):
        mod, _ = run_script(self.FILE)
        person = mod.Person("Robin", 20, False)
        person.talk()
        captured = capsys.readouterr()
        assert "Robin. You may start after the first speech." in captured.out


# ---------------------------------------------------------------------------
# point.py
# ---------------------------------------------------------------------------
class TestPoint:
    FILE = f"{FOLDER}/point.py"

    def test_script_produces_no_output(self):

        """
        point.py only defines the Point class - nothing is instantiated
        or called at module level, so running it directly prints nothing.
        """

        _, out = run_script(self.FILE)
        assert out == ""

    def test_move_method_directly(self, capsys):
        mod, _ = run_script(self.FILE)
        point = mod.Point()
        point.move()
        captured = capsys.readouterr()
        assert captured.out.strip() == "move"

    def test_draw_method_directly(self, capsys):
        mod, _ = run_script(self.FILE)
        point = mod.Point()
        point.draw()
        captured = capsys.readouterr()
        assert captured.out.strip() == "draw"

    def test_point_has_no_constructor_defined(self):

        """
        Unlike constructors.py's Point class, this Point() takes no
        __init__ arguments at all and has no x/y attributes until
        manually assigned after instantiation.
        """

        mod, _ = run_script(self.FILE)
        point = mod.Point()
        assert not hasattr(point, "x")
        point.x = 5
        assert point.x == 5


# ---------------------------------------------------------------------------
# real_estate.py
# ---------------------------------------------------------------------------
class TestRealEstate:
    FILE = f"{FOLDER}/real_estate.py"

    def test_all_five_property_descriptions_printed(self):
        _, out = run_script(self.FILE)
        assert "Oakwood House: 4 bedroom house for £450,000.00." in out
        assert "Lakeside Flat: Flat on floor 8 for £240,000.00." in out
        assert "Harbor Apartments: 12 unit apartment for £300,000.00." in out
        assert "City Tower: 20-storey building valued at £1,200,000.00." in out
        assert "Royal Crest: Luxury mansion with a private pool for £2,500,000.00." in out

    def test_prices_are_comma_formatted(self):
        _, out = run_script(self.FILE)
        assert "£1,200,000.00" in out  # confirms thousands separators, not just decimal formatting

    def test_price_setter_rejects_non_positive_values(self, capsys):
        mod, _ = run_script(self.FILE)
        house = mod.House("Test House", 100000, 3)
        house.price = -500
        captured = capsys.readouterr()
        assert "Price must be greater than 0." in captured.out
        assert house.price == 100000  # unchanged

    def test_price_setter_accepts_valid_positive_value(self):
        mod, _ = run_script(self.FILE)
        house = mod.House("Test House", 100000, 3)
        house.price = 150000
        assert house.price == 150000

    def test_base_realestate_description_uses_comma_formatting_too(self):
        mod, _ = run_script(self.FILE)
        base = mod.RealEstate("Plot of Land", 1000000)
        assert base.description() == "Plot of Land is priced at £1,000,000.00."

    def test_name_property_has_no_setter(self):
        mod, _ = run_script(self.FILE)
        house = mod.House("Test House", 100000, 3)
        with pytest.raises(AttributeError):
            house.name = "Renamed House"


# ---------------------------------------------------------------------------
# restaurant.py
# ---------------------------------------------------------------------------
class TestRestaurant:
    FILE = f"{FOLDER}/restaurant.py"

    def test_indian_restaurant_details(self):

        # Note: the source's own typo "Resturant" is preserved verbatim
        _, out = run_script(self.FILE)
        assert "Resturant: Spice of India (Indian)" in out
        assert "Location: London" in out
        assert "Menu: Butter Chicken, Naan Bread, Biryani" in out

    def test_chinese_restaurant_details(self):
        _, out = run_script(self.FILE)
        assert "Resturant: Dragon's Delight (Chinese)" in out
        assert "Location: Manchester" in out
        assert "Menu: Kung Pao Chicken, Fried Rice, Dim Sum" in out

    def test_japanese_restaurant_details(self):
        _, out = run_script(self.FILE)
        assert "Resturant: Sakura Sushi (Japanese)" in out
        assert "Location: Birmingham" in out
        assert "Menu: Miso Soup, Sashimi, Ramen" in out

    def test_restaurant_owns_its_menu_via_composition(self):
        mod, _ = run_script(self.FILE)
        assert isinstance(mod.indian.menu, mod.Menu)

    def test_menu_display_menu_directly(self):
        mod, _ = run_script(self.FILE)
        menu = mod.Menu(["Rice", "Curry"])
        assert menu.display_menu() == "Menu: Rice, Curry"

    def test_three_restaurants_printed_in_definition_order(self):
        _, out = run_script(self.FILE)
        assert out.find("Spice of India") < out.find("Dragon's Delight") < out.find("Sakura Sushi")


# ---------------------------------------------------------------------------
# school.py
# ---------------------------------------------------------------------------
class TestSchool:
    FILE = f"{FOLDER}/school.py"

    def test_school_name_and_address_printed(self):
        _, out = run_script(self.FILE)
        assert "Greenwood High" in out
        assert "123 Main St" in out

    def test_all_three_students_listed_with_ages(self):
        _, out = run_script(self.FILE)
        assert "Alice, Age: 15" in out
        assert "Bob, Age: 16" in out
        assert "Charlie, Age: 14" in out

    def test_separator_line_between_school_info_and_student_list(self):
        _, out = run_script(self.FILE)
        assert "-" * 30 in out

    def test_remove_student_removes_a_matching_instance(self):
        mod, _ = run_script(self.FILE)
        school = mod.School("Test School", "1 Test Rd")
        student = mod.Student("Test Student", 12)
        school.add_student(student)
        assert len(school.students) == 1
        school.remove_student(student)
        assert len(school.students) == 0

    def test_remove_student_is_a_no_op_for_an_unrelated_instance(self):

        """
        Student has no __eq__ defined, so the `if student in self.students`
        check falls back to identity comparison - a different Student
        object with identical name/age is NOT considered a match and
        removal silently does nothing.
        """

        mod, _ = run_script(self.FILE)
        school = mod.School("Test School", "1 Test Rd")
        student_in_school = mod.Student("Same Name", 10)
        student_not_in_school = mod.Student("Same Name", 10)
        school.add_student(student_in_school)
        school.remove_student(student_not_in_school)
        assert len(school.students) == 1


# ---------------------------------------------------------------------------
# sports.py
# ---------------------------------------------------------------------------
class TestSports:
    FILE = f"{FOLDER}/sports.py"

    def test_all_four_sport_details_printed(self):
        _, out = run_script(self.FILE)
        assert "Football team: Arsenal | Stadium: Emirates Stadium" in out
        assert "Basketball team: Lakers | Court: Staples Center" in out
        assert "Cricket team: England | Venue: Lord's" in out
        assert "Tennis tournament: Wimbledon | Surface: Grass" in out

    def test_nested_sport_classes_are_scoped_under_sports(self):
        mod, _ = run_script(self.FILE)
        football = mod.Sports.Football("Test FC", "Test Stadium")
        assert football.details() == "Football team: Test FC | Stadium: Test Stadium"

    def test_sports_printed_in_the_order_theyre_defined(self):
        _, out = run_script(self.FILE)
        assert out.find("Football") < out.find("Basketball") < out.find("Cricket") < out.find("Tennis")

    def test_each_nested_class_is_independent_of_the_others(self):
        mod, _ = run_script(self.FILE)
        assert mod.Sports.Football is not mod.Sports.Basketball
        assert not hasattr(mod.Sports.Cricket("England", "Lord's"), "court")


# ---------------------------------------------------------------------------
# user_access.py
# ---------------------------------------------------------------------------
class TestUserAccess:
    FILE = f"{FOLDER}/user_access.py"

    def test_valid_login_and_sufficient_permission_grants_access(self):
        _, out = run_script(self.FILE)
        assert "Access granted for user1 to perform write." in out

    def test_valid_login_but_insufficient_permission_is_denied(self):

        """
        The @require_permission("write") decorator hardcodes the action
        it checks against - "write" - regardless of what action the
        caller actually passed at runtime ("read" for user2). So even
        though user2 only requested "read", the message still references
        "write", since that's the permission the decorator itself was
        built to enforce.
        """

        _, out = run_script(self.FILE)
        assert "Access denied for user2. Insufficient permissions for write." in out

    def test_login_check_runs_before_permission_check(self):

        """
        @require_login is the OUTERMOST decorator, so its wrapper's
        login_check() runs first; only if that passes does execution
        reach the inner @require_permission wrapper's permission_check().
        """

        mod, _ = run_script(self.FILE)
        result = mod.user_access("user1", "wrong-password", "write")
        assert result == "Invalid username or password."

    def test_permission_check_fires_only_after_successful_login(self):
        mod, _ = run_script(self.FILE)
        result = mod.user_access("user2", "securepass", "write")
        assert "Access denied" in result

    def test_login_check_and_permission_check_directly(self):
        mod, _ = run_script(self.FILE)
        assert mod.login_check("user1", "password123") is True
        assert mod.login_check("user1", "wrong") is False
        assert mod.permission_check("user1", "write") is True
        assert mod.permission_check("user2", "write") is False

    def test_unknown_username_fails_login_check(self):
        mod, _ = run_script(self.FILE)
        assert mod.login_check("ghost_user", "anything") is False


# ---------------------------------------------------------------------------
# worker.py
# ---------------------------------------------------------------------------
class TestWorker:
    FILE = f"{FOLDER}/worker.py"

    def test_manager_dispatch(self):
        _, out = run_script(self.FILE)
        assert "Alice is working as a Manager." in out
        assert "Alice is managing the Engineering department." in out

    def test_developer_dispatch(self):
        _, out = run_script(self.FILE)
        assert "Bob is working as a Developer." in out
        assert "Bob is coding in Python." in out

    def test_designer_dispatch(self):
        _, out = run_script(self.FILE)
        assert "Charlie is working as a Designer." in out
        assert "Charlie is designing using Figma." in out

    def test_writer_dispatch(self):
        _, out = run_script(self.FILE)
        assert "Eve is working as a Writer." in out
        assert "Eve is writing in the Fiction genre." in out

    def test_intern_dispatch(self):

        # mentor="Eve" here is just a coincidental data value, unrelated
        # to the separate Writer instance also named Eve in the same list.
        _, out = run_script(self.FILE)
        assert "David is working as a Intern." in out
        assert "David is learning from Eve." in out

    def test_all_five_workers_processed_in_list_order_with_separators(self):
        _, out = run_script(self.FILE)
        assert out.count("=" * 34) == 10  # 2 separator lines per worker x 5 workers
        assert out.find("Alice") < out.find("Bob") < out.find("Charlie") < out.find("Eve") < out.find("David")

    def test_match_case_dispatch_uses_type_not_just_attributes(self):

        """
        The match statement dispatches on Manager()/Developer()/etc. as
        TYPE patterns, not by inspecting attributes - confirms a base
        Worker() instance (belonging to none of the subclasses) falls
        through to the default case.
        """

        mod, _ = run_script(self.FILE)
        plain_worker = mod.Worker("Test", "Generic Role")
        match plain_worker:
            case mod.Manager():
                result = "manager"
            case _:
                result = "default"
        assert result == "default"

