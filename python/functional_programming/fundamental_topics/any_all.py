"""
any() and all() - quantifiers over an iterable.

any(iterable) returns True if AT LEAST ONE item is truthy.
all(iterable) returns True if EVERY item is truthy.
Both return a bool, and both short-circuit: any() stops at the first
truthy item, all() stops at the first falsy one. On an empty iterable any()
is False and all() is True, which follows from the quantifier logic rather
than being a special case.
"""

# any() = Returns True if AT LEAST ONE item is truthy.
# all() = Returns True if EVERY item is truthy.
# any(iterable) -> bool     all(iterable) -> bool


scores = [45, 62, 78, 91]
languages = ["Python", "Java", "C++"]

# any(): did anyone reach 70+?
any_passed = any(score >= 70 for score in scores)
all_passed = all(score >= 40 for score in scores)

# Checking for a specific pattern
has_python = any("Python" in lang for lang in languages)

# Empty iterables behave differently
print("any([]) is", any([]))
print("all([]) is", all([]))

print("Scores:", scores)
print("Anyone scored 70+:", any_passed)
print("Everyone scored 40+:", all_passed)
print("Includes Python:", has_python)


