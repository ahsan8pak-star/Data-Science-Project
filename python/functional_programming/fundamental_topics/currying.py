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