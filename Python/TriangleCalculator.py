import math

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

def sine_rule():
    print("\nSine Rule")
    target = input("Do you want to find a 'side' or 'angle'? ").strip().lower()
    
    if target == "angle":
        print("Valid combinations: ab, ac, bc")
        sides = input("Which two sides do you know? ").strip().lower()
        
        match sides:
            
            case "ab":
                a = get_float_input("Enter side a: ")
                b = get_float_input("Enter side b: ")
                known_ang = input("Which angle do you know? (A or B): ").strip().upper()
            
                if a and b:
            
                    if known_ang == "A":
                        A = get_float_input("Enter Angle A (degrees): ")
            
                        if A:
                            sin_B = (b * math.sin(math.radians(A))) / a
                            print(f"\nResult: Angle B is {round(math.degrees(math.asin(sin_B)), 2)} degrees")
            
                    elif known_ang == "B":
                        B = get_float_input("Enter Angle B (degrees): ")
            
                        if B:
                            sin_A = (a * math.sin(math.radians(B))) / b
                            print(f"\nResult: Angle A is {round(math.degrees(math.asin(sin_A)), 2)} degrees")
            
                    else:
                        print("Error: For sides a and b, you must know angle A or B.")
            
            case "ac":
                a = get_float_input("Enter side a: ")
                c = get_float_input("Enter side c: ")
                known_ang = input("Which angle do you know? (A or C): ").strip().upper()
            
                if a and c:
            
                    if known_ang == "A":
                        A = get_float_input("Enter Angle A (degrees): ")
            
                        if A:
                            sin_C = (c * math.sin(math.radians(A))) / a
                            print(f"\nResult: Angle C is {round(math.degrees(math.asin(sin_C)), 2)} degrees")
            
                    elif known_ang == "C":
                        C = get_float_input("Enter Angle C (degrees): ")
            
                        if C:
                            sin_A = (a * math.sin(math.radians(C))) / c
                            print(f"\nResult: Angle A is {round(math.degrees(math.asin(sin_A)), 2)} degrees")
            
                    else:
                        print("Error: For sides a and c, you must know angle A or C.")
            
            case "bc":
                b = get_float_input("Enter side b: ")
                c = get_float_input("Enter side c: ")
                known_ang = input("Which angle do you know? (B or C): ").strip().upper()
            
                if b and c:
                    
                    if known_ang == "B":
                        B = get_float_input("Enter Angle B (degrees): ")
                    
                        if B:
                            sin_C = (c * math.sin(math.radians(B))) / b
                            print(f"\nResult: Angle C is {round(math.degrees(math.asin(sin_C)), 2)} degrees")
                    
                    elif known_ang == "C":
                        C = get_float_input("Enter Angle C (degrees): ")
                    
                        if C:
                            sin_B = (b * math.sin(math.radians(C))) / c
                            print(f"\nResult: Angle B is {round(math.degrees(math.asin(sin_B)), 2)} degrees")
                    
                    else:
                        print("Error: For sides b and c, you must know angle B or C.")
            
            case _:
                print("Invalid side combination.")

    elif target == "side":
        print("Valid combinations: AB, AC, BC")
        angles = input("Which two angles do you know? ").strip().upper()
        
        match angles:
     
            case "AB":
                A = get_float_input("Enter Angle A (degrees): ")
                B = get_float_input("Enter Angle B (degrees): ")
                known_side = input("Which side do you know? (a or b): ").strip().lower()
     
                if A and B:
     
                    if known_side == "a":
                        a = get_float_input("Enter side a: ")
     
                        if a:
                            b = (a * math.sin(math.radians(B))) / math.sin(math.radians(A))
                            print(f"\nResult: Side b is {round(b, 2)}")
     
                    elif known_side == "b":
                        b = get_float_input("Enter side b: ")
     
                        if b:
                            a = (b * math.sin(math.radians(A))) / math.sin(math.radians(B))
                            print(f"\nResult: Side a is {round(a, 2)}")
     
            case "AC":
                A = get_float_input("Enter Angle A (degrees): ")
                C = get_float_input("Enter Angle C (degrees): ")
                known_side = input("Which side do you know? (a or c): ").strip().lower()
     
                if A and C:
     
                    if known_side == "a":
                        a = get_float_input("Enter side a: ")
     
                        if a:
                            c = (a * math.sin(math.radians(C))) / math.sin(math.radians(A))
                            print(f"\nResult: Side c is {round(c, 2)}")
     
                    elif known_side == "c":
                        c = get_float_input("Enter side c: ")
     
                        if c:
                            a = (c * math.sin(math.radians(A))) / math.sin(math.radians(C))
                            print(f"\nResult: Side a is {round(a, 2)}")
     
            case "BC":
                B = get_float_input("Enter Angle B (degrees): ")
                C = get_float_input("Enter Angle C (degrees): ")
                known_side = input("Which side do you know? (b or c): ").strip().lower()
     
                if B and C:
     
                    if known_side == "b":
                        b = get_float_input("Enter side b: ")
     
                        if b:
                            c = (b * math.sin(math.radians(C))) / math.sin(math.radians(B))
                            print(f"\nResult: Side c is {round(c, 2)}")
     
                    elif known_side == "c":
                        c = get_float_input("Enter side c: ")
     
                        if c:
                            b = (c * math.sin(math.radians(B))) / math.sin(math.radians(C))
                            print(f"\nResult: Side b is {round(b, 2)}")
     
            case _:
                print("Invalid angle combination.")

def cosine_rule():
    print("\nCosine Rule")
    target = input("Do you want to find a 'side' or 'angle'? ").strip().lower()
    
    if target == "side":
        print("Valid combinations: ab, ac, bc")
        sides = input("Which two sides do you know? ").strip().lower()
        
        match sides:

            case "ab":
                print("To find side 'c', you must provide Angle C.")
                a = get_float_input("Enter side a: ")
                b = get_float_input("Enter side b: ")
                C = get_float_input("Enter Angle C (degrees): ")

                if a and b and C:
                    c = math.sqrt((a**2) + (b**2) - (2 * a * b * math.cos(math.radians(C))))
                    print(f"\nResult: Side c is {round(c, 2)}")

            case "ac":
                print("To find side 'b', you must provide Angle B.")
                a = get_float_input("Enter side a: ")
                c = get_float_input("Enter side c: ")
                B = get_float_input("Enter Angle B (degrees): ")

                if a and c and B:
                    b = math.sqrt((a**2) + (c**2) - (2 * a * c * math.cos(math.radians(B))))
                    print(f"\nResult: Side b is {round(b, 2)}")

            case "bc":
                print("To find side 'a', you must provide Angle A.")
                b = get_float_input("Enter side b: ")
                c = get_float_input("Enter side c: ")
                A = get_float_input("Enter Angle A (degrees): ")

                if b and c and A:
                    a = math.sqrt((b**2) + (c**2) - (2 * b * c * math.cos(math.radians(A))))
                    print(f"\nResult: Side a is {round(a, 2)}")

            case _:
                print("Invalid combination.")

    elif target == "angle":
        print("To find an angle using Cosine Rule, you MUST know all three sides (a, b, c).")
        a = get_float_input("Enter side a: ")
        b = get_float_input("Enter side b: ")
        c = get_float_input("Enter side c: ")
        
        if a and b and c:
            find_ang = input("Which angle do you want to find? (A, B, or C): ").strip().upper()

            match find_ang:

                case "A":
                    cos_A = ((b**2) + (c**2) - (a**2)) / (2 * b * c)
                    print(f"\nResult: Angle A is {round(math.degrees(math.acos(cos_A)), 2)} degrees")

                case "B":
                    cos_B = ((a**2) + (c**2) - (b**2)) / (2 * a * c)
                    print(f"\nResult: Angle B is {round(math.degrees(math.acos(cos_B)), 2)} degrees")

                case "C":
                    cos_C = ((a**2) + (b**2) - (c**2)) / (2 * a * b)
                    print(f"\nResult: Angle C is {round(math.degrees(math.acos(cos_C)), 2)} degrees")

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
        
    if c is None:
        print(f"\nResult: Hypotenuse (c) is {round(math.sqrt(a**2 + b**2), 2)}")

    elif a is None:
        print(f"\nResult: Adjacent side (a) is {round(math.sqrt(c**2 - b**2), 2)}")

    elif b is None:
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
            case "1": sine_rule()
            case "2": cosine_rule()
            case "3": pythagoras(triangle_type)
            case "4": area(triangle_type)
            case "5": perimeter(triangle_type)
            case "6": 
                print("Powering down...")
                break
            case _: print("Invalid selection.")

run_calculator()