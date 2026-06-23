import math

# This functions alone helps other functions to be called out without to type down input() constantly and repeatly

def get_float_input(prompt): 
    
    user_input = input(prompt) # user starts their input
    
    if user_input.strip() == "": # If input hasn't been typed down i.e. <ENTER>
        return None # Returns a NULL answer
    
    try:
        return float(user_input) # converts user input from string into float
    
    except ValueError:
        print("Invalid input. Numbers only.")
        return None # Safety net for incorrect values

print("\nPythagorean Theorem")
print("Leave the variable blank (press Enter) for the one you want to find.")
a = get_float_input("Enter side a (cm): ")
b = get_float_input("Enter side b (cm): ")
c = get_float_input("Enter hypotenuse c (cm): ")

missing = [a, b, c].count(None)

if missing != 1:
    print("Error: You must provide exactly TWO known values.")

else:
    if c is None:
        print(f"\nResult: Hypotenuse (c) is {round(math.sqrt(a**2 + b**2), 2)} cm")
    
    elif a is None:
        print(f"\nResult: Side (a) is {round(math.sqrt(c**2 - b**2), 2)} cm")
    
    elif b is None:
        print(f"\nResult: Side (b) is {round(math.sqrt(c**2 - a**2), 2)} cm")