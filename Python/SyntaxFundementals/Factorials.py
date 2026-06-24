def factorial(n):
    if n == 0 or n == 1: # confirms if the number is 0 or 1
        return 1 # result from these two special case scenarios
    else:
        return n * factorial(n - 1) # factorial function / formula
    

try: # opens a safe execution zone to process user entries and catch typing errors
    
    # Prompts the user to type a number and captures it as a string by default
    num = input("Enter your number: ")

    n = int(num) # converts the number into an integer

    print(factorial(n))

        
except ValueError: # prevents a crash in the system if the user enters other than integers like floats for example
    print("Error: Invalid number format. Enter integers only (whole numbers).") # specifies the input rules to guide the operator

