def get_value(char): # Case Switch for Roman Numerals Individually

    match char:
        case "M": return 1000
        case "D": return 500
        case "C": return 100
        case "L": return 50
        case "X": return 10
        case "V": return 5
        case "I": return 1
        case _: 
            raise ValueError() # triggers a system error if an illegal character is typed to trip the try-except safety net

def roman_to_int(numeral):

    final_answer = 0 # begins the function, meaning it starts at a baseline of zero
    
    numeral = numeral.upper() # ensures leverage of typing roman numerals regardless of its case
    
    for i in range(len(numeral)): # loops using index positions so we have numbers to peek ahead
        current_val = get_value(numeral[i])    

        if i + 1 < len(numeral): # checks for the next roman numeral to be compared
            next_val = get_value(numeral[i+1])
            
            if current_val < next_val: # if the first roman numeral is smaller than the second one
                final_answer -= current_val # e.g. CM = 900 -> (M = 1000) - (C = 100)
            
            else: # if the first roman numeral is bigger than or equal to the second one
                final_answer += current_val # e.g. MC = 1100 -> (M = 1000) + (C = 100)     
                
        else: # handles the very last roman numeral since there is no next character left to compare
            final_answer += current_val 
            
    return final_answer # returns the number back in the roman numeral function

try: # opens a safe execution zone to run the program and catch any input errors
    
    roman_input = input("Enter Roman Numerals: ")
    arabic_result = roman_to_int(roman_input)
    print("Arabic Numerals: " + str(arabic_result)) 

except ValueError: # prevents a crash in the system i.e. replaces it with an error message
    print("Error: Roman Numerals Only (I, V, X, L, C, D, M)") # specifies what the roman numerals are to give a guide to the user

