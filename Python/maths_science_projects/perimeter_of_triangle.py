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

    print("\nPerimeter of a Triangle")
    a = get_float_input("Enter side a (cm): ")
    b = get_float_input("Enter side b (cm): ")
    c = get_float_input("Enter side c (cm): ")

    if a and b and c:
        print(f"\nResult: Perimeter is {round(a + b + c, 2)} cm")

