# Pipeline = Passing data through a chain of functional steps
# (filter -> map -> sorted -> reduce) without changing any input list.
# Each step returns a NEW value; the original data stays untouched.


from functools import reduce

students = [
    ("Ahsan", 55),
    ("Hamza", 72),
    ("Zara", 38),
    ("Bilal", 64),
    ("Alina", 91),
]

# One pipeline: keep passes, add a bonus, sort by score, name the winners
passing = list(filter(lambda s: s[1] >= 40, students))
boosted = list(map(lambda s: (s[0], s[1] + 3), passing))
ranked = sorted(boosted, key=lambda s: s[1], reverse=True)
winners = [name for name, score in ranked if score >= 70]

print("Original:", students)
print("Passing:", passing)
print("Boosted:", boosted)
print("Ranked:", ranked)
print("Winners:", winners)

# Reduce a list of scores down to a single average
scores = [55, 72, 38, 64, 91]
average = reduce(lambda a, b: a + b, scores) / len(scores)
print("Average score:", round(average, 2))