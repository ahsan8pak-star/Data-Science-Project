# define functions first to prevent crashes of values not returning
def volume(x, y, z):
    return x * y * z

def area(x, y):
    return x * y

# Menu Screen
print("Geometry Calculator")
print()
print("1: Calculate Area")
print("2: Calculate Volume")

choice = input("Enter your choice (1 or 2): ").strip()

match choice:

    case "1":
        print("Area Calculator")
    
        try:
            x = float(input("Enter Length (cm): "))
            y = float(input("Enter Width (cm): "))
    
            print(f"Area: {round(area(x, y), 2)} cm²")
    
        except ValueError:
            print("Error: Numbers only.")

    case "2":
        print("Volume Calculator")
        
        try:
            x = float(input("Enter Length (cm): "))
            y = float(input("Enter Width (cm): "))
            z = float(input("Enter Depth (cm): "))
        
            print(f"Volume: {round(volume(x, y, z), 2)} cm³")
        
        except ValueError:
            print("Error: Numbers only.")

    case _: # The underscore (_) acts as the 'default' or 'else' case
        print("Invalid choice. Please run the program again.")