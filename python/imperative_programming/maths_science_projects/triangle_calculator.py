import sys
import os

# Tells Python to look inside this exact folder for modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import math 
import cosine_rule
import sine_rule

# This functions alone helps other functions to be called out without to type down input() constantly

def get_float_input(prompt): 
    
    user_input = input(prompt) # user starts their input
    
    if user_input.strip() == "": # If input hasn't been typed down i.e. <ENTER>
        return None # Returns a NULL answer
      
    try:
        return float(user_input) # converts user input from string into float
    
    except ValueError:
        print("Invalid input. Please enter numbers only.")
        return None # Safety net for incorrect values

def pythagoras(triangle_type):

    print("\nPythagorean Theorem")

    if triangle_type in ["scalene", "equilateral", "isosceles"]:
        print(f"Error: Pythagoras ONLY works on Right-Angled triangles. You selected {triangle_type.title()}.")
        return

    print("Leave the variable blank (press Enter) for the one you want to find.")
    a = get_float_input("Enter adjacent side (a): ")
    b = get_float_input("Enter opposite side (b): ")
    c = get_float_input("Enter hypotenuse (c): ")
    
    missing = [a, b, c].count(None)

    if missing != 1:
        print("Error: You must provide exactly TWO known values.")
        return
        
    if c is None and a is not None and b is not None: # side a and b
        print(f"\nResult: Hypotenuse (c) is {round(math.sqrt(a**2 + b**2), 2)}")
   
    elif a is None and b is not None and c is not None: # side b and c
        if c <= b:
            print("Error: Hypotenuse (c) MUST be strictly greater than side (b).")
        
        else:
            print(f"\nResult: Adjacent side (a) is {round(math.sqrt(c**2 - b**2), 2)}")
   
    elif b is None and a is not None and c is not None: # side a and c
        if c <= a:
            print("Error: Hypotenuse (c) MUST be strictly greater than side (a).")
        
        else:
            print(f"\nResult: Opposite side (b) is {round(math.sqrt(c**2 - a**2), 2)}")

def area(triangle_type):
    print(f"\nArea of a {triangle_type.title()} Triangle")

    if triangle_type == "equilateral":
        a = get_float_input("Enter the length of any side: ")

        if a:
            print(f"\nResult: Area is {round((math.sqrt(3) / 4) * (a**2), 2)}")

    elif triangle_type == "right":
        a = get_float_input("Enter leg a: ")
        b = get_float_input("Enter leg b: ")

        if a and b:
            print(f"\nResult: Area is {round((a * b) / 2, 2)}")

    else:
        b = get_float_input("Enter the base: ")
        h = get_float_input("Enter the height: ")

        if b and h:
            print(f"\nResult: Area is {round((b * h) / 2, 2)}")

def perimeter(triangle_type):
    print(f"\nPerimeter of a {triangle_type.title()} Triangle")

    match triangle_type:

        case "equilateral":
            a = get_float_input("Enter the length of one side: ")

            if a: print(f"\nResult: Perimeter is {round(a * 3, 2)}")

        case "isosceles":
            equal_side = get_float_input("Enter length of one of the equal sides: ")
            base = get_float_input("Enter the base side: ")

            if equal_side and base:
                print(f"\nResult: Perimeter is {round((equal_side * 2) + base, 2)}")

        case _:
            a = get_float_input("Enter side a: ")
            b = get_float_input("Enter side b: ")
            c = get_float_input("Enter side c: ")

            if a and b and c:
                print(f"\nResult: Perimeter is {round(a + b + c, 2)}")

def run_calculator():
    print("========================================")
    print("          TRIANGLE  CALCULATOR          ")
    print("========================================")
    print("Specify triangle type:")
    print("A. Right-Angled")
    print("B. Equilateral")
    print("C. Isosceles")
    print("D. Scalene")
    
    type_choice = input("\nSelect triangle type (A-D): ").strip().upper()

    match type_choice:

        case "A": triangle_type = "right"

        case "B": triangle_type = "equilateral"

        case "C": triangle_type = "isosceles"

        case "D": triangle_type = "scalene"

        case _: triangle_type = "scalene"
            
    print(f"\n>>> Calculator locked into {triangle_type.title()} mode. <<<")

    while True:
        print("------------------------------")
        print(" 1. Sine Rule")
        print(" 2. Cosine Rule")
        print(" 3. Pythagorean Theorem")
        print(" 4. Area")
        print(" 5. Perimeter")
        print(" 6. Quit")
        choice = input("Select a mode (1-6): ").strip()
        
        match choice:
  
            case "1": sine_rule.calculate()
 
            case "2": cosine_rule.calculate()
 
            case "3": pythagoras(triangle_type)
 
            case "4": area(triangle_type)
 
            case "5": perimeter(triangle_type)
 
            case "6": 
                print("Powering down...")
                break
 
            case _: print("Invalid selection.")

if __name__ == "__main__": # allow this to be an imported module by protecting the main execution
    run_calculator()

