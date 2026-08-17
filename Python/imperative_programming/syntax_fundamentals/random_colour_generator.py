from random import randint

def random_colours():
    # TUI Heading
    print("\n --- Random Colour Generator --- \n")

    max_num = int(input("Enter the maximum range (i.e. number of colours): "))
    
    # Present the multiple-choice options clearly to the user
    print("\nWhat type of colour generator is it?")
    print("1. Hexadecimal (e.g. 0xA623F6)")
    print("2. RGB (e.g. (10, 20, 30))")
    print("3. Octal (e.g. 0x16032743)")
    print("4. HSL (e.g. (80, 60%, 40%))\n")
    
    # Accept either the menu number or the name to prevent accidental issues / crashes
    colour_type = input("Enter your choice: ").strip().lower()

    print(f"\nGenerating {max_num} random colour(s):")
    print("-" * 30) # TUI Separater Line

    for _ in range(max_num):
        match colour_type:
            
            # The pipe '|' acts as an 'or', allowing multiple valid answers for one case
            case "1" | "hexadecimal" | "hexa" | "hex" | "he":
                hex_colour = f"#{randint(0, 0xFFFFFF):06X}"
                print(hex_colour)
                
            case "2" | "rgb" | "r" | "b" | "g":
                r = randint(0, 255)
                g = randint(0, 255)
                b = randint(0, 255)
                print(f"RGB({r}, {g}, {b})")
                
            case "3" | "octal" | "oct" | "oc" | "o":
                octal_colour = oct(randint(0, 0xFFFFFF))
                print(octal_colour)
                
            case "4" | "hsl" | "hs":
                h = randint(0, 360)
                s = randint(0, 100)
                l = randint(0, 100)
                print(f"HSL({h}, {s}%, {l}%)")
                
            # The underscore '_' is the wildcard / default case (equivalent to 'else')
            case _:
                print(f"Error: '{colour_type}' is not a recognised option.\nUse the 4 main options mentioned above.")
                break


if __name__ == "__main__":
    try:
        random_colours()

    except ValueError:
        print("Wrong Data Values.\nCheck the question being asked for the correct data type.")

