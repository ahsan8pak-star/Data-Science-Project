import math

# This functions alone helps other functions to be called out without to type down input() constantly and repeatly

def get_float_input(prompt): 
    
    user_input = input(prompt) # user starts their input
    
    if user_input.strip() == "": # If input hasn't been typed down i.e. <ENTER>
        return None # Returns a NULL answer
    
    if __name__ == "__main__": # allow this to be an imported module
        try:
            return float(user_input) # converts user input from string into float
    
        except ValueError:
            print("Invalid input. Numbers only.")
            return None # Safety net for incorrect values

def calculate(): # Main function for importing directly to triangle calculator

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
   
                    if -1 <= cos_A <= 1:
                        print(f"\nResult: Angle A is {round(math.degrees(math.acos(cos_A)), 2)} degrees")
   
                    else:
                        print("Error: Impossible triangle. These sides cannot connect.")
   
                case "B":
                    cos_B = ((a**2) + (c**2) - (b**2)) / (2 * a * c)
   
                    if -1 <= cos_B <= 1:
                        print(f"\nResult: Angle B is {round(math.degrees(math.acos(cos_B)), 2)} degrees")
   
                    else:
                        print("Error: Impossible triangle. These sides cannot connect.")
   
                case "C":
                    cos_C = ((a**2) + (b**2) - (c**2)) / (2 * a * b)
   
                    if -1 <= cos_C <= 1:
                        print(f"\nResult: Angle C is {round(math.degrees(math.acos(cos_C)), 2)} degrees")
   
                    else:
                        print("Error: Impossible triangle. These sides cannot connect.")

if __name__ == "__main__":  # allows this to be an imported module by protecting the main execution
    calculate() # This allows the file to run if opened directly

