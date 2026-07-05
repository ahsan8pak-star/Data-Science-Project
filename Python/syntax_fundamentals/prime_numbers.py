def is_prime(n):
    
    # Assume the number is prime and tries to find other numbers which aren't i.e. counter examples
    flag = True

    # Deals with special cases i.e. only these unique numbers in this scenario
    if n == 0 or n == 1:
        flag = False
    
    # Loop through all numbers between 2 and n - 1, and check if n is NOT prime
    i = 2
    while i < n:
        if n % i == 0:
            flag = False
        i = i + 1
    
    # Output the current value of flag back to the execution zone below
    return flag


try: # opens a safe execution zone to process user entries and catch typing errors
    
    # Prompts the user to type a number and captures it as a string by default
    num = input("Enter your number: ")
    
    # Converts the text into an integer 
    n = int(num)
    
    # Runs the prime checker function and evaluates the true/false return flag
    if is_prime(n): 
        print("The number " + str(n) + " is a prime number!") # confirms prime status safely to the user as a string
    else:
        print("The number " + str(n) + " isn't prime.") # updates the user that a clean factor was discovered
        
except ValueError: # prevents a crash in the system if the user enters other than integers like floats for example
    print("Error: Invalid number format. Enter integers only (whole numbers).") # specifies the input rules to guide the operator

