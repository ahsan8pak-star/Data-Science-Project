# This file should run only standalone OR imported as a module

def favourite_food(food):
    print(f"\nYour favourite food is '{food.upper()}'!")

def main():
    print("\nYou are seeing SCRIPT 1!")

    favourite_food("chicken") # function being called
    
    print("\nBye Bye!")


if __name__ == "__main__":
    main()

