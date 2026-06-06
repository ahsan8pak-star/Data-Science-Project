def name(): # def - define function
    print("A.I.M")


name() # PEP 8 styling suggests being 2 lines apart from the function

# but it is not required to execute the function.



def add(a, b): # Parameters - a and b are parameters of the function add.
    return a + b # Return - the value that the function gives back after execution.


result = add(5, 3) # Arguments - 5 and 3 are arguments passed to the function add.
print(result) # Output: 8



def multiply(x, y):
    return x * y


product = multiply(4, 6)
print(product) # Output: 24



def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)
    

print(factorial(5)) # Output: 120


def greet(name): 
    return f"{name}"


message = greet("A.I.M")
file = open("AIM.txt", "w") # Opens a file in write mode.
file.write(message) # Writes the greeting message to the file.
file.close() # Closes the file.



def increment(number, by=1): # Default parameter - by has a default value of 1.
    return number + by


result = increment(10, 5)
print(result) # Output: 15
print(increment(20, 10)) # Output: 30
print(increment(7, by=3)) # Output: 10
print(increment(15)) # Output: 16 (uses default value of by)



def divide(*numbers): # xArgs - *numbers allows the function to accept a variable number of arguments.
    total = 100
    for n in numbers:
        total /= n
    return total

print(divide(5, 4, 2)) # Output: 2.5


