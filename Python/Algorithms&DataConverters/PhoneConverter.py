def num(phone): # Mapping a numeric digit to its string word from 0 to 9
    match phone:
        case 0:
            return "Zero"
        case 1:
            return "One"
        case 2:
            return "Two"
        case 3:
            return "Three"
        case 4:
            return "Four"
        case 5:
            return "Five"
        case 6:
            return "Six"
        case 7:
            return "Seven"
        case 8:
            return "Eight"
        case 9:
            return "Nine"
        case _: # The underscore acts as the 'default' or 'else' case
            return "Invalid Phone Digit"
        
while True: # Keeps looping until a valid input is received 
# Meaning it should be up to 9 characters long for the digits length

    phone = input("Phone: ") # Treated as a string on its default case

    if 0 < len(phone) < 10 and phone.isdigit(): # Checks if the length is 1-9 characters AND contains only numbers 

        break # Exits the loop to proceed to the processing stage

    else:
        print("Enter up to 9 digits from 0 to 9.") # Displays the error message

result = "" # Starts with an empty string 

for digit in phone: # Iterates through each validated digit in the string

    word = num(int(digit)) # calls the function directly
    result += word + " " # Seperates the "words"

print("Word:", result) # outputs the words of that phone number

