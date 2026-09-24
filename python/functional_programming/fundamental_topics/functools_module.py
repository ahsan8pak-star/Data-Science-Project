# functools = Higher-order functions for working with other functions.
# cache/lru_cache memoise results, partial pre-fills arguments, reduce
# folds an iterable, singledispatch routes on type, wraps copies metadata.


import functools


# cache() remembers the answer for each set of arguments
@functools.cache
def square(n): # The decorated function stores its results keyed by argument
    return n * n

print("cache:", square(4), square(5), square(4)) # Repeated square(4) reuses the stored 16


# lru_cache() remembers only the most recent results, dropping the oldest
@functools.lru_cache(maxsize=3)
def double(n): # Only the last 3 unique calls are kept in memory
    return n * 2

print("lru_cache:", double(1), double(2), double(1), double.cache_info()) # The 4th call evicts the 1st entry


# partial() locks in some arguments of a function up front
def multiply(a, b): # The original function still takes both arguments
    return a * b

times_two = functools.partial(multiply, 2) # b is left free, a is fixed to 2

print("partial:", times_two(5), times_two(10)) # Each call only supplies the missing b


# reduce() repeatedly folds an iterable into one accumulated value
total = functools.reduce(lambda a, b: a + b, [1, 2, 3, 4, 5])

print("reduce:", total)


# singledispatch() picks a different implementation based on the first argument's type
@functools.singledispatch
def describe(value): # The default implementation runs when no specific type matches
    return f"unknown: {value}"

@describe.register(int)
def _(value): # This overload replaces the default when the first argument is an int
    return f"integer: {value}"

@describe.register(str)
def _(value): # This overload replaces the default when the first argument is a str
    return f"text: {value}"

print("singledispatch:", describe(42), "|", describe("hello"), "|", describe([1, 2]))


# wraps() copies the original function's name and docstring onto the wrapper
def logging_decorator(func):
    @functools.wraps(func) # Without this the wrapper would expose its own name instead
    def wrapper(*args, **kwargs):
        print(f"calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@logging_decorator
def greet(): # The wrapper copies greet's metadata (name + docstring) over itself
    """Says a friendly hello."""
    return "Hello!"

print("wraps:", greet(), "| name:", greet.__name__, "| doc:", greet.__doc__)