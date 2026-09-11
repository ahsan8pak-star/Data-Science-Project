# map() = Applies a given function to every item in one or more iterables, returning a new iterable of the results.
# Commonly paired with a lambda so no separate named function is needed.
# map(function, iterable, ...) -> map object (must wrap in list()/tuple() to view)

numbers = [1, 2, 3, 4, 5]
prices = ["9.99", "14.50", "3.25", "20.00"]

list_a = [1, 2, 3, 4]
list_b = [10, 20, 30, 40]

# Single-iterable map: transforming each value
squared = list(map(lambda x: x ** 2, numbers))
doubled = list(map(lambda x: x * 2, numbers))

# Type-conversion map: string prices -> float values
prices_as_floats = list(map(float, prices))

# Multi-iterable map: combining matching positions from two lists
# (distinct from zip.py, which pairs values -> this actually combines them)
sums = list(map(lambda a, b: a + b, list_a, list_b))
products = list(map(lambda a, b: a * b, list_a, list_b))

print("Original numbers:", numbers)
print("Squared:", squared)
print("Doubled:", doubled)

print("\nOriginal prices (strings):", prices)
print("Prices as floats:", prices_as_floats)

print("\nList A:", list_a)
print("List B:", list_b)
print("Sums (A + B):", sums)
print("Products (A * B):", products)

