# Python - Idiomatic Alternative (optional/default parameters)
def add(a, b, c = None):

    if c is not None:
        return a + b + c

    return a + b

