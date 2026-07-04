import math


def circumference(radius):

    area = math.pi * 2 * radius 
    
    return area

try: 
    radius = input("Enter Radius: ")

    if float(radius) > 0:
        print(f"Circumference of Circle: {circumference(float(radius)):.2f}")

    else:
        print("Enter a valid radius")

except ValueError:
    print("Numbers only")

except TypeError:
    print("Positive Numbers only. Meaning greater than 0.")

except KeyboardInterrupt:
    print("Unusual Crash Detected.")

