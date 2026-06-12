# Exceptions are mainly used for Error Catching
# That means it'll allow the error message to be outputted without crashing the program

try: # Used for the actual executable code to be run underneath
    age = int(input("Enter your age: "))
    print(age)

except ValueError: # Very common example
    print("Enter the age in integers (whole numbers).")
