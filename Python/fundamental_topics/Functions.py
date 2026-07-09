def name(): # def - define function
    print("A.I.M")


name() # PEP 8 styling suggests being 2 lines apart from the function

# Not required but a good practice for cleaner code


def decrement(a, b): # Parameters - a and b are parameters of the function decrement.
    return a - b # Return - the value that the function gives back after execution.


result = decrement (5, 3) # Arguments - 5 and 3 are arguments passed to the function decrement.
print(result) # Output: 2


def increment(number, by=1): # Default parameter - by has a default value of 1.
    return number + by


result = increment(10, 5)
print(result) # Output: 15
print(increment(20, 10)) # Output: 30
print(increment(7, by=3)) # Output: 10
print(increment(15)) # Output: 16 (uses default value of by)

def hello(greeting, title, first, last): # Standard parameters i.e. basic / generic variable assignment
    print(f"{greeting} {title} {first} {last}") # Spacing matters on how the message is formatted
    # Ordering keywords can vary its location i.e. Unordered format


hello("Hello", title="Mr.", last="Iqbal", first="Ahsan") # Keyword - various parameter types for various inputs in out of order, i.e. unordered
# Positional Argument ( "Hello" ) + Keyword Arguement ( title="Mr.", last="Iqbal", first="Ahsan" )

def divide(*numbers): # xArgs - *numbers allows the function to accept a variable number of arguments.
    total = 100
    for n in numbers:
        total /= n
    return total


print(divide(5, 4, 2)) # Output: 2.5

