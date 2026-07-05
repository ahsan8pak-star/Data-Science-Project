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

                            if -1 <= sin_B <= 1:
                                print(f"\nResult: Angle B is {round(math.degrees(math.asin(sin_B)), 2)} degrees")

                            else:
                                print("Error: Impossible dimensions (Domain Error).")

                    elif known_ang == "B":
                        B = get_float_input("Enter Angle B (degrees): ")

                        if B:
                            sin_A = (a * math.sin(math.radians(B))) / b

                            if -1 <= sin_A <= 1:
                                print(f"\nResult: Angle A is {round(math.degrees(math.asin(sin_A)), 2)} degrees")

                            else:
                                print("Error: Impossible dimensions (Domain Error).")

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

                            if -1 <= sin_C <= 1:
                                print(f"\nResult: Angle C is {round(math.degrees(math.asin(sin_C)), 2)} degrees")

                            else:
                                print("Error: Impossible dimensions (Domain Error).")

                    elif known_ang == "C":
                        C = get_float_input("Enter Angle C (degrees): ")

                        if C:
                            sin_A = (a * math.sin(math.radians(C))) / c

                            if -1 <= sin_A <= 1:
                                print(f"\nResult: Angle A is {round(math.degrees(math.asin(sin_A)), 2)} degrees")

                            else:
                                print("Error: Impossible dimensions (Domain Error).")

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

                            if -1 <= sin_C <= 1:
                                print(f"\nResult: Angle C is {round(math.degrees(math.asin(sin_C)), 2)} degrees")

                            else:
                                print("Error: Impossible dimensions (Domain Error).")

                    elif known_ang == "C":
                        C = get_float_input("Enter Angle C (degrees): ")

                        if C:
                            sin_B = (b * math.sin(math.radians(C))) / c

                            if -1 <= sin_B <= 1:
                                print(f"\nResult: Angle B is {round(math.degrees(math.asin(sin_B)), 2)} degrees")

                            else:
                                print("Error: Impossible dimensions (Domain Error).")

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

