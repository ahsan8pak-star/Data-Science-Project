class Item:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return f"{self.name} - £{self.price:.2f} (x{self.quantity})"

    def __eq__(self, other):
        return self.name == other.name and self.price == other.price

    def __lt__(self, other):
        return self.price < other.price

    def __gt__(self, other):
        return self.price > other.price

    def __add__(self, other):
        return self.price + other.price

    def __contains__(self, keyword):
        return keyword.lower() in self.name.lower()

    def __getitem__(self, key):

        if key == "name":
            return self.name

        elif key == "price":
            return self.price

        elif key == "quantity":
            return self.quantity

        return f"Key '{key}' was not found"


item1 = Item("Keyboard", 29.99, 2)
item2 = Item("Mouse", 9.99, 5)
item3 = Item("Monitor", 129.99, 1)

print(item1)            # __str__
print(item1 == item3)   # __eq__ -> Keyboard == Monitor?
print(item2 < item3)    # __lt__ -> Mouse < Monitor? True
print(item3 > item1)    # __gt__ -> Monitor > Keyboard? True
print(item1 + item2)    # __add__ -> 29.99 + 9.99 = 39.98
print("board" in item1) # __contains__ -> "board" in Keyboard? True
print("laptop" in item2) # __contains__ -> "laptop" in Mouse? False
print(item1["price"])   # __getitem__ -> 29.99
print(item2["quantity"]) # __getitem__ -> 5
print(item3["name"])    # __getitem__ -> Monitor

