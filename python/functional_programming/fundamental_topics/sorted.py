# sorted() = Returns a NEW sorted list without changing the original.
# Commonly paired with a lambda to sort by a chosen feature.
# sorted(iterable, key=..., reverse=...) -> list


names = ["Alina", "Hamza", "Zara", "Bilal", "Ahsan"]
people = [("Ahsan", 21), ("Hamza", 20), ("Zara", 19), ("Bilal", 22)]

# Basic alphabetical sort (the original list is untouched)
sorted_names = sorted(names)
reverse_names = sorted(names, reverse=True)

# Sort tuples by their second item (age) using a key
by_age = sorted(people, key=lambda person: person[1])

print("Original:", names)
print("Sorted:", sorted_names)
print("Reverse:", reverse_names)
print("By age:", by_age)