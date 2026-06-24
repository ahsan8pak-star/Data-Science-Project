import math

def arithmetic (num1, op, num2):
    
    match op:
        case "+":
            return num1 + num2
    
        case "-":
            return num1 - num2
    
        case "*":
            return num1 * num2
    
        case "/":
            if num2 == 0:
                return "Error: ndefined. You can't divide anything by 0." # return allows the function to retrive the value rather than print() -> program crash
    
            else:
                return num1 / num2 
    
        case "//":
            if num2 == 0:
                return "Error: Undefined. You can't divide anything by 0." # "Error" is essential for the type() function to work in lines 84 & 85
            else:
                return num1 // num2
    
        case "%":
            if num2 == 0:
                return "Error: Undefined. You can't divide anything by 0."
            else:
                return num1 % num2 
        
        case "**":
            return num1 ** num2
            
try:
    print("=======================")
    print(" ARITHMETIC CALCULATOR ")        
    print("=======================")
    print("")
    print("<================>")
    print("<  MENU   GUIDE  >")
    print("<================>")
    print("")
    print("  _______________________________________________________ ")
    print(" /                                                       \ ")
    print(" | 1) + = addition         5) // = base / quotient       | ")
    print(" | 2) - = subtraction      6) % = remainder / modulus    | ") 
    print(" | 3) * = multiplication   7) ** = power / exponent      | ")
    print(" | 4) / = division         8) <ENTER> = Calculate result | ")
    print(" \                                                       / ")
    print("  ``````````````````````````````````````````````````````` ")
    print("")


    first_num = input("Enter the 1st number: ").strip()

    if not first_num: # When <ENTER> is pressed first
    
        print("No input provided. Exiting.")
    
        exit()

    total = float(first_num)

    
    for count in range(2, 51): # Up to 50 numbers (Very Excessive)
        
        op = input(f"Enter operation {count-1}: ").strip() # decrements numbers for every operation used (next_num - 1)
    
        if not op:  # Hit <ENTER> for result
            break

        # Next number to be inputted after the 1st i.e. 2nd -> op -> 3rd -> op -> 4th etc.
        next_num = input(f"Enter the number [{count}]: ").strip()

        if not next_num:  # Hit Enter to calculate resuly
            break

        total = arithmetic(total, op, float(next_num))

        # Safety Check: If an error string comes back (like division by zero), break immediately
        if type(total) is str and "Error" in total:
            break # Stops the program from excessive memory wasted

    # Rounding & Significant Figures [Optional]
    result = total

    if type(total) in (int, float):
        round_choice = (input("\nFormat answer? (d = Decimals / s = Significant Figures / n = No): ").strip().lower())

        if round_choice and round_choice[0].lower() == "d":
            places = int(input("Enter the number of Decimal Places to be rounded to: ").strip())
            result = round(total, places)

        elif round_choice and round_choice[0].lower() == "s":
            sf = int(input("Enter the amount of Significant Figures to be rounded to: ").strip())

            # Uses f-string with the 'g' specifier for accurate significant figures
            result = f"{total:.{sf}g}"
        
        elif round_choice and round_choice[0].lower() == "n":
            result = total
        
        else:
            print("Invalid choice. Try again.")
            result = total

        # Strip trailing .0 from clean integers for better box formatting
        if type(result) is float and result.is_integer():
            result = int(result)
    else:
        result = total  # Pass through the division by zero error string

    # Dynamic TUI Box Display Engine
    result_payload = f"| Result: {result} |"
    box_border = "-" * len(result_payload)

    print("\n" + box_border)
    print(result_payload)
    print(box_border)

except ValueError:
    print("\nIncorrect Format. Enter valid numbers.")

