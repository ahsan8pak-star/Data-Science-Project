# Comprehensions = A shorthand way to build a new iterable from another.
# [expression for item in iterable if condition] -> compact loops


numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
votes = ["yes", "no", "yes", "abstain", "yes"]
students = ["Ahsan", "Hamza", "Zara"]

# List comprehension with a filter
squares = [n ** 2 for n in numbers]
evens = [n for n in numbers if n % 2 == 0]

# Set comprehension (removes duplicates automatically)
unique_votes = {v for v in votes}

# Dictionary comprehension
lengths = {name: len(name) for name in students}

print("Numbers:", numbers)
print("Squares:", squares)
print("Evens:", evens)
print("Unique votes:", unique_votes)
print("Name lengths:", lengths)