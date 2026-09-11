# Food -> Snack -> Dessert / Treats
# Food -> Drink -> Cold Drink / Hot Drink

class Food:
    def __init__(self, name, calories):
        self.name = name
        self.calories = calories

    def describe(self):
        return f"'{self.name}' has '{self.calories}' calories."


class Snack(Food):
    def __init__(self, name, calories, serving_size):
        super().__init__(name, calories)
        self.serving_size = serving_size

    def snack_info(self):
        return f"'{self.name}' is a snack served in '{self.serving_size}'."

class Dessert(Snack):
    def __init__(self, name, calories, serving_size, sweetness):
        super().__init__(name, calories, serving_size)
        self.sweetness = sweetness

    def dessert_info(self):
        return f"'{self.name}' is a dessert with '{self.sweetness}' sweetness."


class Treat(Snack):
    def __init__(self, name, calories, serving_size, texture):
        super().__init__(name, calories, serving_size)
        self.texture = texture

    def treat_info(self):
        return f"'{self.name}' has a '{self.texture}' texture."


class Drink(Food):
    def __init__(self, name, calories, temperature):
        super().__init__(name, calories)
        self.temperature = temperature

    def drink_info(self):
        return f"'{self.name}' is served at a '{self.temperature}' temperature."


class ColdDrink(Drink):
    def __init__(self, name, calories, temperature, carbonation):
        super().__init__(name, calories, temperature)
        self.carbonation = carbonation

    def cold_drink_info(self):
        return f"'{self.name}' is '{self.carbonation}'."


class HotDrink(Drink):
    def __init__(self, name, calories, temperature, aroma):
        super().__init__(name, calories, temperature)
        self.aroma = aroma

    def hot_drink_info(self):
        return f"'{self.name}' has a '{self.aroma}' aroma."

cake = Dessert("Chocolate Cake", 350, "1 Slice", "High")
cookies = Treat("Chocolate Chip Cookies", 220, "2 Cookies", "Crunchy")
cola = ColdDrink("Cola", 140, "Cold", "Carbonated")
tea = HotDrink("Green Tea", 50, "Hot", "Fresh")

print(cake.describe())
print(cake.snack_info())
print(cake.dessert_info())

print("-" * 40)

print(cookies.describe())
print(cookies.snack_info())
print(cookies.treat_info())

print("-" * 40)

print(cola.describe())
print(cola.drink_info())
print(cola.cold_drink_info())

print("-" * 40)

print(tea.describe())
print(tea.drink_info())
print(tea.hot_drink_info())

