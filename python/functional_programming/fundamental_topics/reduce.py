# reduce() = Accumulates an iterable down to a single value by applying a function to pairs of items.
# Works like a running total, flowing through each item once.
# from functools import reduce     reduce(function, iterable) -> single value


from functools import reduce

# Running total (sum)
numbers = [1, 2, 3, 4, 5]
total = reduce(lambda x, y: x + y, numbers)

# Running product (factorial of 5)
factorial = reduce(lambda x, y: x * y, range(1, 6))

# Finding the largest value
largest = reduce(lambda x, y: x if x > y else y, numbers)

# Joining words into a sentence
words = ["Python", "is", "functional"]
sentence = reduce(lambda a, b: a + " " + b, words)

print("Numbers:", numbers)
print("Sum:", total)
print("Factorial of 5:", factorial)
print("Largest:", largest)
print("Joined:", sentence)