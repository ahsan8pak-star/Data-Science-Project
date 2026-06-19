def is_leap(year):
    
    leap = False # Assumes it's false since we have no confirmation at the start
    
    if year % 4 == 0: # Fundemental rule that every year has to be a multiple of 4 hence every 4 years
        leap = True
    
    else:
        leap = False
    
    return leap

try:
    year = int(input("Is it a leap year?: ")) # Makes sure that the input is converted to integers since we are using years in that form
    print(is_leap(year))

except ValueError: # Captures the main error when the user inputs their answer into this function
    print("Integers only")


