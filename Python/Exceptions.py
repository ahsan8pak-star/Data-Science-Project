# Exceptions are mainly used for Error Catching
# That means it'll allow the error message to be outputted without crashing the program

try: # Used for the actual executable code to be run underneath
    age = int(input("Enter your age: "))
    print(age)

except ValueError: # Very common example
    print("Enter the age in integers (whole numbers).")

try: # A more accurate rate currency calculator
    time = int(input("Enter the time period (in years): "))

    actual_income = input("Enter your income (up to 2 decimal places): ").strip()
    if "." in actual_income and len(actual_income.split(".")[1]) > 2:
        raise Exception("Income cannot have more than 2 decimal places.")
    
    # This raises an exception 
    # Meaning it calls the error message provided
    # An alternative way to use exceptions from this code below:
    # except Exception as error_message:
    #   print(error_message)
        
    income = float(actual_income) 
    currency = input("Enter your currency (only symbols): ").strip()

    if len(currency) != 1:
        raise Exception("Single Symbols only") 
    
    if income < 0:
        raise Exception("Enter a Valid amount.") 

    rate = income / time
    actual_rate = f"{currency[0]}{rate:.2f}" 
    print(actual_rate)

except ValueError:
    print("Only numbers are accepted for time and income.")

except ZeroDivisionError: 
    print("Has to be at least 1 year.")

except Exception as error_message: # prints out the terminal error messages that it found in its system
    print("Random Error Found: " + str(error_message))