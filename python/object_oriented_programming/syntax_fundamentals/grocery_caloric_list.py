class FoodItem:
    def __init__(self, name, calories, price):
        self.name = name
        self.calories = calories
        self.price = price

    def __repr__(self):
        return f"{self.name.title():<10} | {self.calories:>4} kcal | £{self.price:.2f}"


class OrderLine:
    def __init__(self, item, quantity):
        self.item = item
        self.quantity = quantity

    @property
    def total_calories(self):
        return self.item.calories * self.quantity

    @property
    def total_price(self):
        return self.item.price * self.quantity

    def __repr__(self):
        return (
            f"{self.item.name.title():<10} | Qty: {self.quantity:>2} | "
            f"{self.total_calories:>5} kcal | £{self.total_price:>6.2f}"
        )


def get_positive_float(prompt):
    while True:
        try:
            val = float(input(prompt))
            if val > 0:
                return val
            print("Please enter a value greater than 0.")
        except ValueError:
            print("Invalid input. Please enter a numerical value.")


def display_menu(title, menu_dict):
    print(f"\n--- {title} ---")
    for item in menu_dict.values():
        print(item)


def print_welcome():
    print("=" * 50)
    print(f'{"GROCERY & CALORIE TRACKER":^50}')
    print("=" * 50)
    print(f'{"Plan your meals, balance your budget,":^50}')
    print(f'{"and hit your calorie goals!":^50}')
    print("=" * 50 + "\n")


def generate_recommendations(order, catalogue, cal_excess, budget_excess, remaining_cals, remaining_budget):
    print("\n" + "=" * 50)
    print(f'{"ANALYSIS & RECOMMENDATIONS":^50}')
    print("=" * 50)

    over_calories = cal_excess > 0
    over_budget = budget_excess > 0

    # SCENARIO 1: Exceeds BOTH Calories and Budget
    if over_calories and over_budget:
        print(f"EXCEEDED BOTH LIMITS!")
        print(f"Caloric excess: {cal_excess:.0f} kcal")
        print(f"Budget excess:  £{budget_excess:.2f}\n")
        print("Recommended Removals (Fixes BOTH or significantly reduces both):")

        found_option = False
        for line in order:
            unit_cal = line.item.calories
            unit_price = line.item.price
            
            if unit_cal >= cal_excess and unit_price >= budget_excess:
                print(f"- Remove 1x '{line.item.name.title()}' "
                      f"(Saves {unit_cal} kcal and £{unit_price:.2f} - solves BOTH excesses!)")
                found_option = True
            elif unit_cal >= cal_excess or unit_price >= budget_excess:
                print(f"- Remove 1x '{line.item.name.title()}' "
                      f"(Saves {unit_cal} kcal and £{unit_price:.2f})")
                found_option = True

        if not found_option:
            print("- Consider reducing quantities across multiple items to balance both limits.")

    # SCENARIO 2: Exceeds Calories ONLY
    elif over_calories:
        print(f"EXCEEDED CALORIC LIMIT!")
        print(f"Caloric excess: {cal_excess:.0f} kcal")
        print(f"Budget remaining: £{abs(budget_excess):.2f}\n")
        print("Recommended Removals (To stay within calorie limit):")

        for line in order:
            unit_cal = line.item.calories
            if unit_cal >= cal_excess:
                print(f"- Remove 1x '{line.item.name.title()}' (Saves {unit_cal} kcal)")

    # SCENARIO 3: Exceeds Budget ONLY
    elif over_budget:
        print(f"EXCEEDED BUDGET LIMIT!")
        print(f"Budget excess:  £{budget_excess:.2f}")
        print(f"Calories remaining: {abs(cal_excess):.0f} kcal\n")
        print("Recommended Removals (To stay within budget):")

        for line in order:
            unit_price = line.item.price
            if unit_price >= budget_excess:
                print(f"- Remove 1x '{line.item.name.title()}' (Saves £{unit_price:.2f})")

    # SCENARIO 4: Within BOTH Limits
    else:
        print("Nice! You are within both your Caloric and Budget limits.")
        print(f"Remaining Calories: {remaining_cals:.0f} kcal")
        print(f"Remaining Budget:   £{remaining_budget:.2f}\n")

        additions = []
        for item in catalogue.values():
            max_by_budget = int(remaining_budget / item.price) if item.price > 0 else 0
            max_by_cals = int(remaining_cals / item.calories) if item.calories > 0 else 0
            max_qty = min(max_by_budget, max_by_cals)

            if max_qty > 0:
                total_item_cals = max_qty * item.calories
                total_item_cost = max_qty * item.price
                additions.append((item, max_qty, total_item_cals, total_item_cost))

        if additions:
            print("Optional Additions (Maximum quantity that fits into your remaining allowances):")
            for item, max_qty, total_cals, total_cost in additions:
                print(
                    f"- Add up to {max_qty}x '{item.name.title()}' "
                    f"({total_cals:.0f} kcal | £{total_cost:.2f} total)"
                )


def grocery_caloric_list():
    print_welcome()

    # Menus setup
    fruits_menu = {
        "banana": FoodItem("banana", 105, 0.30),
        "apple": FoodItem("apple", 72, 0.50),
        "orange": FoodItem("orange", 73, 0.40),
        "coconut": FoodItem("coconut", 354, 2.50)
    }

    vegetables_menu = {
        "carrot": FoodItem("carrot", 25, 0.15),
        "broccoli": FoodItem("broccoli", 55, 1.20),
        "potato": FoodItem("potato", 130, 0.25),
        "spinach": FoodItem("spinach", 23, 0.90)
    }

    catalogue = {**fruits_menu, **vegetables_menu}

    # Daily limits input
    max_calories = get_positive_float("Enter your maximum daily caloric intake (kcal): ")
    max_budget = get_positive_float("Enter your maximum budget (£): ")

    # Display menus
    display_menu("Fruits Menu", fruits_menu)
    display_menu("Vegetables Menu", vegetables_menu)

    order = []

    # Initial Item selection
    print("\nEnter the items you would like to order initially, separated by commas:")
    user_input = input("> ").strip().lower()
    
    if user_input:
        selected_names = list(dict.fromkeys([n.strip() for n in user_input.split(",") if n.strip()]))
        
        for name in selected_names:
            if name in catalogue:
                item = catalogue[name]
                while True:
                    try:
                        qty = int(input(f"How many {name}(s) would you like to order? "))
                        if qty > 0:
                            order.append(OrderLine(item, qty))
                            break
                        print("Quantity must be at least 1.")
                    except ValueError:
                        print("Please enter a valid whole number.")
            else:
                print(f"Notice: '{name}' is not on the menu and was skipped.")

    # Main Interactive Loop
    while True:
        if not order:
            print("\nYour order is currently empty.")
        else:
            # Calculations
            total_cals = sum(line.total_calories for line in order)
            total_cost = sum(line.total_price for line in order)

            # Print Receipt
            print("\n" + "=" * 50)
            print(f'{"YOUR GROCERY RECEIPT":^50}')
            print("=" * 50)

            for line in order:
                print(line)

            print("-" * 50)
            print(f"TOTAL CALORIES: {total_cals:.0f} / {max_calories:.0f} kcal")
            print(f"TOTAL COST:     £{total_cost:.2f} / £{max_budget:.2f}")
            print("=" * 50)

            # Scenario Analysis & Recommendations
            cal_excess = total_cals - max_calories
            budget_excess = total_cost - max_budget
            remaining_cals = max_calories - total_cals
            remaining_budget = max_budget - total_cost

            generate_recommendations(
                order, catalogue, cal_excess, budget_excess, remaining_cals, remaining_budget
            )

        # Prompt for Modification or Exit
        print("\n" + "-" * 50)
        print("Would you like to adjust your order?")
        action = input("Enter an item name to add/update, 'no' or press <ENTER> to finish: ").strip().lower()

        # Exit Condition
        if action in ['', 'no']:
            print("\n" + "=" * 70)
            print(f'{"HERE'S YOUR ORDER! THANKS FOR SHOPPING WITH OUR TRACKER!":^70}')
            print("=" * 70 + "\n")
            break
        
        # Modification Logic
        if action in catalogue:
            item = catalogue[action]
            while True:
                try:
                    qty = int(input(f"Enter the new total quantity for '{action.title()}' (0 to remove): "))

                    if qty >= 0:
                        # Search for the item in the current order to update it
                        found = False

                        for i, line in enumerate(order):
                            if line.item.name == action:
                                if qty == 0:
                                    order.pop(i)
                                    print(f"Removed '{action.title()}' from your order.")

                                else:
                                    line.quantity = qty
                                    print(f"Updated '{action.title()}' quantity to {qty}.")
                                found = True
                                break
                        
                        # If the item wasn't in the order and the user typed a quantity > 0, add it
                        if not found and qty > 0:
                            order.append(OrderLine(item, qty))
                            print(f"Added {qty}x '{action.title()}' to your order.")
                        break

                    else:
                        print("Quantity cannot be negative.")

                except ValueError:
                    print("Please enter a valid whole number.")
        else:
            print(f"Notice: '{action}' is not on the menu. Please check the spelling and try again.")


if __name__ == "__main__":
    grocery_caloric_list()

