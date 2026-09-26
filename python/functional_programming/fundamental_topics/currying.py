"""
Currying - turning one function that takes multiple arguments into a chain
of functions that each take a single argument.

    add(a, b)  becomes  add(a)(b)

Useful when an argument is fixed early and reused, or when a function has to
satisfy a callback that expects exactly one parameter. The counterpart is
partial application, where some arguments are bound up front instead.
"""

# Currying = Turning one function that takes multiple arguments
# into a chain of functions that each take a single argument.
# add(a, b) becomes add(a)(b)


# Regular function
def add(a, b):
    return a + b


print("regular add(2, 3):", add(2, 3))

# Curried version
curried_add = lambda a: lambda b: a + b
print("curried add(2)(3):", curried_add(2)(3))

# Practical example: reusing the first argument
greet = lambda greeting: lambda name: f"{greeting}, {name}!"
say_hello = greet("Hello")
say_hi = greet("Hi")

print(say_hello("Ahsan"))
print(say_hi("Hamza"))


