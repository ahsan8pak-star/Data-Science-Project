"""
Compound interest - the growth on a principal over a number of periods.

    A = P(1 + r/100)^t

Kept deliberately parallel to compound_debt_calculator.py, which computes
the same figure; the pair shows how one formula serves two different
framings. Both catch ZeroDivisionError on a zero rate.
"""

def compound_interest(p, r, t):

    a = p * ((1 + r / 100) ** t)  # A = P(1 + r/100)^n
    return a

try:

    while True: # While this function is true, hence program running.
    
        p = float(input("Enter your amount (£): "))
        
        if p < 0:
            print("Amount can't be negative (-).")
            print("Go to the Compound Debt Calculator for such values.\n")
            break 
            
        elif p == 0:
            print("Result will be 0, regardless of the interest and time.")
            print("Give a positive (+) non-zero (p > 0) amount.\n")
            break
            
        else:
            r = float(input("Enter your rate (%): ")) 
            t = int(input("Enter your time (years): "))

            result = compound_interest(p, r, t)
            print(f"Initial Amount: £{p:.2f}")
            print(f"Annual Rate: {r:.2f}%")
            print(f"# of years: {t}")
            print(f"Total Amount: £{result:.2f}\n")
            break # Ends the If-Else statement to prevent the program constantly running

except ValueError:
    print("Enter a valid input.")


