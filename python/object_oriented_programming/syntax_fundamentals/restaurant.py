class Menu:
    def __init__(self, items):
        self.items = items

    def display_menu(self):
        return f"Menu: {', '.join(self.items)}"


class Restaurant:
    def __init__(self, name, location, cuisine_type, menu_items):
        self.name = name
        self.location = location
        self.cuisine_type = cuisine_type
        self.menu = Menu(menu_items)  # Restaurant owns its Menu (Composition)

    def display_restaurant(self):

        width = 45

        return (
            f"\n{'=' * (width + 4)}\n"
            f"| {f'Resturant: {self.name} ({self.cuisine_type})': <{width}} |\n"
            f"| {f'Location: {self.location}': <{width}} |\n"
            f"| {f'{self.menu.display_menu()}': <{width}} |\n"
            f"{'=' * (width + 4)}"
        )


indian = Restaurant(
    "Spice of India",
    "London",
    "Indian",
    ["Butter Chicken", "Naan Bread", "Biryani"]
)

chinese = Restaurant(
    "Dragon's Delight",
    "Manchester",
    "Chinese",
    ["Kung Pao Chicken", "Fried Rice", "Dim Sum"]
)

japanese = Restaurant(
    "Sakura Sushi",
    "Birmingham",
    "Japanese",
    ["Miso Soup", "Sashimi", "Ramen"]
)

print(indian.display_restaurant())
print(chinese.display_restaurant())
print(japanese.display_restaurant())

