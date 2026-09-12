# partial() = Pre-fills some of a function's arguments, creating a specialised version.
# from functools import partial     partial(function, argument) -> new function with the argument locked in


from functools import partial


# A general function made specific
def power(base, exponent):
    return base ** exponent


square = partial(power, exponent=2)
cube = partial(power, exponent=3)

print("square(4):", square(4))
print("cube(3):", cube(3))

# Fixing a style option for rounding
formatted = partial(round, ndigits=2)
print("formatted(3.14159):", formatted(3.14159))