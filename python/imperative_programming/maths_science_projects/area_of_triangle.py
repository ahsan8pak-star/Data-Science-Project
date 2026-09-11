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

def calculate():
    
    print("\nArea of a Triangle")
    b = get_float_input("Enter the base (cm): ")
    h = get_float_input("Enter the perpendicular height (cm): ")

    if b and h:
        print(f"\nResult: Area is {round((b * h) / 2, 2)} cm^2")

if __name__ == "__main__": # allow this to act as an imported module
    calculate()

