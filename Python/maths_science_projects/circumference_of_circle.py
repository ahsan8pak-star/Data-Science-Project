import math


def calculate_circumference(radius):

    area = math.pi * 2 * radius 
    
    return area

def circumference():
    try: 
        radius = input("\nEnter Radius: ")

        if float(radius) > 0:
            print("\n-----------------------------------------")
            print(f"| {f'Circumference of Circle: {calculate_circumference(float(radius)):.2f}':^37} |")
            print("-----------------------------------------")

        else:
            print("Enter a valid radius")

    except ValueError:
        print("Numbers only")

    except TypeError:
        print("Positive Numbers only. Meaning greater than 0.")

    except KeyboardInterrupt:
        print("Unusual Crash Detected.")

if __name__ == "__main__":
    circumference()

