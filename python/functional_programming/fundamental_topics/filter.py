# filter() = Builds a new iterable containing only the items where a given function returns True for each item.
# Commonly paired with a lambda so no separate named function is needed.
# filter(function, iterable) -> filter object (must wrap in list() / tuple() to view)

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
ages = [15, 18, 12, 21, 17, 25, 16]
words = ["hello", "", "world", "", "python", ""]

# Even/odd numeric predicate
evens = list(filter(lambda x: x % 2 == 0, numbers))
odds = list(filter(lambda x: x % 2 == 1, numbers))

# Threshold predicate (mirrors lamda.py's own age_check style)
adults = list(filter(lambda age: age >= 18, ages))
minors = list(filter(lambda age: age < 18, ages))

# Non-empty string predicate
non_empty_words = list(filter(lambda word: word != "", words))

# filter() also accepts None as the function
# Only keeping "truthy" values (removes 0, "", None, False, empty lists, etc.)
mixed_values = [0, 1, "", "text", None, 3.5, False, True]
truthy_only = list(filter(None, mixed_values))

print("All numbers:", numbers)
print("Even numbers:", evens)
print("Odd numbers:", odds)

print("\nAll ages:", ages)
print("Adults (18+):", adults)
print("Minors (under 18):", minors)

print("\nAll words:", words)
print("Non-empty words:", non_empty_words)

print("\nMixed values:", mixed_values)
print("Truthy-only values:", truthy_only)

