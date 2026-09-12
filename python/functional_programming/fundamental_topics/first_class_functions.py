# First-class functions = Functions can be treated like any other value.
# They can be stored in variables, passed as arguments, and returned from other functions.


def square(x):
    return x ** 2


def cube(x):
    return x ** 3


# Storing a function in a variable
operation = square
print("square stored as operation:", operation(4))

# Passing a function as an argument (higher-order function)
def apply(func, value):
    return func(value)


print("apply(square, 5):", apply(square, 5))
print("apply(cube, 5):", apply(cube, 5))

# Returning a function from another function
def make_power(exponent):
    def power(base):
        return base ** exponent
    return power


doubler = make_power(2)
cubed = make_power(3)
print("doubler(6):", doubler(6))
print("cubed(6):", cubed(6))