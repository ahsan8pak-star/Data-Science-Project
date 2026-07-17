def compound_debt(p, r, t):

    a = p * ((1 + r / 100) ** t)  # A = P(1 + r/100)^n
    return a

try:

    while True: # While this function is true, hence program running.
    
        p = float(input("Enter your amount (£): "))
        
        if p > 0:
            print("This is only for negative (-) values.")
            print("Go to Compound Interest Calculator for positive (+) values.\n")
            break 
            
        elif p == 0:
            print("Result will be 0, regardless of the interest and time.")
            print("Give a negative non-zero (p < 0) amount.\n")
            break
            
        else:
            r = float(input("Enter your rate (%): ")) 
            t = int(input("Enter your time (years): "))

            result = compound_debt(p, r, t)
            print(f"Initial Amount: £{p:.2f}")
            print(f"Annual Rate: {r:.2f}%")
            print(f"# of years: {t}")
            print(f"Total Amount: £{result:.2f}\n")
            break # Ends the If-Else statement to prevent the program constantly running

except ValueError:
    print("Enter a valid input.")

