try: # A more accurate annual rate calculator with currency (£/$) and symbols like percentages (%)
    
    time = int(input("Enter the time period (in years): "))

    actual_income = input("Enter your income (up to 2 decimal places): ").strip()
    if "." in actual_income and len(actual_income.split(".")[1]) > 2:
        raise Exception("Income cannot have more than 2 decimal places.")
    
    # This raises an exception 
    # Meaning it calls the error message provided
    # It's an alternative way to use exceptions from this code below:

    # except Exception as error_message:
    #   print(error_message)
        
    income = float(actual_income) 
    currency = input("Enter your currency (only initial symbols): ").strip() 
    
    # Using strip() allows the user to write down the amount comfortably
    # If they accidentally made a whitespace (an extra space unintentionally made)

    if len(currency) != 1:
        raise Exception("Single Symbols only") # Has to be an initial only
    
    if income < 0:
        raise Exception("Enter a Valid Amount.") # Enter income greater than 0

    # The percentage rate formula 
    rate = income / time
    percentage_value = (rate / income) * 100 
    
    # Formatted Results
    formatted_income = f"{currency[0]}{income:.2f}"
    formatted_time = f"{time} years"
    formatted_rate = f"{currency[0]}{rate:.2f}" # gets the only currency symbol needed (assuming it's an initial) and places it next to the amount rate
    formatted_percentage = f"{percentage_value:.2f}%" # this is the converted/formatted rate amount as a percentage
    
    # The Annual Rate Calculator's Answers
    print("Income: " + formatted_income)
    print("Time: " + formatted_time)
    print("Amount Rate: " + formatted_rate + " per year")
    print("Percentage Rate: " + formatted_percentage + " Annual")

except ValueError:
    print("Only numbers are accepted for time and income.")

except ZeroDivisionError: 
    print("Has to be at least 1 year.")

except Exception as error_message: # prints out the terminal error messages that it found in its system
    print("Random Error Found: " + str(error_message))