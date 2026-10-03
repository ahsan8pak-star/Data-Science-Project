# Factorial Example

def factorial(n):

    if n == 0:
        return 1  # Base case: terminates recursive chain

    return n * factorial(n - 1)  # Recursive case: invokes itself with reduced input

# Fibonacci Example

def fibonacci(n):
    if n == 0:
        return 0  # Base case 1

    if n == 1:
        return 1  # Base case 2

    return fibonacci(n - 1) + fibonacci(n - 2)  # Double recursive call

