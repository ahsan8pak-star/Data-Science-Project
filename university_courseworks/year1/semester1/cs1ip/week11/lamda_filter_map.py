# Idiomatic Python list comprehension
names = ["Alice", "Bob", "Charlie"]
filtered_names = [name.upper() for name in names if name.startswith("A")]

# Alternative functional approach using lambda, filter, and map
filtered_names_func = list(map(str.upper, filter(lambda name: name.startswith("A"), names)))

