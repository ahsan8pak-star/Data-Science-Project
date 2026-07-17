import sys
import os

# Tells Python to look inside this exact folder for modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# imported files as modules to undergo D.R.Y (Don't Repeat Yourself)
# from [FILE NAME] import [FUNCTION] allows the specific def function to be imported

from area import area 
from volume import volume

# Menu Screen
print("\n=======================")
print("| Geometry Calculator |")
print("=======================")
print("| 1: Calculate Area   |")
print("| 2: Calculate Volume |")
print("=======================")

choice = input("\nEnter your choice (1 or 2): ").strip()

match choice:

    case "1":
        print("\n===================")
        print("| Area Calculator |")
        print("===================")
    
        try:
            x = float(input("\nEnter Length (cm): "))
            y = float(input("\nEnter Width (cm): "))
            
            print("\n=================================")
            print(f"| {f'Area: {round(area(x, y), 2)} cm²':^29} |")
            print("=================================")
    
        except ValueError:
            print("Error: Numbers only.")

    case "2":
        print("\n=====================")
        print("| Volume Calculator |")
        print("=====================")
        
        try:
            x = float(input("\nEnter Length (cm): "))
            y = float(input("\nEnter Width (cm): "))
            z = float(input("\nEnter Depth (cm): "))

            print("\n=================================")
            print(f"| {f'Volume: {round(volume(x, y, z), 2)} cm³':^29} |")
            print("=================================")
        
        except ValueError:
            print("Error: Numbers only.")

    case _: # The underscore (_) acts as the 'default' or 'else' case
        print("Invalid choice. Please run the program again.")

