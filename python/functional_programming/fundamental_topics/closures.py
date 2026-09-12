# Closure = A nested function that remembers ("captures") a value from its outer function
# even after the outer function has finished running.


def make_multiplier(factor):
    def multiply(value):
        return value * factor
    return multiply


double = make_multiplier(2)
triple = make_multiplier(3)

print("double(5):", double(5))
print("triple(5):", triple(5))

# A counter that remembers its own count
def make_counter():
    count = 0

    def counter():
        nonlocal count
        count += 1
        return count

    return counter


tickets = make_counter()
print("ticket 1:", tickets())
print("ticket 2:", tickets())
print("ticket 3:", tickets())