"""
Area of a circle, pi * r squared.

Kept deliberately without an __main__ guard, which is the asymmetry this file
exists to demonstrate against circumference_of_circle.py, its sibling that
does have one. Running this file therefore produces no output at all, and a
test pins that. circle_calculator.py imports area_of_circle() from here.
"""

import math

def calculate_area(radius):

    area = math.pi * radius * radius
    
    return area

def area_of_circle():
    try: 
        radius = input("\nEnter Radius: ")

        if float(radius) > 0:
            print("\n-----------------------------------------")
            print(f"| {f'Area of Circle: {calculate_area(float(radius)):.2f}':^37} |")
            print("-----------------------------------------")
        else:
            print("Enter a valid radius")
        

    except ValueError:
        print("Numbers only")

    except TypeError:
        print("Positive Numbers only. Meaning numbers greater than 0.")

    except KeyboardInterrupt:
        print("Unusual Crash Detected.")


