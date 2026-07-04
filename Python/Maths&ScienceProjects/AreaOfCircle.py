import math

def area_of_circle(radius):

    area = math.pi * radius * radius
    
    return area

try: 
    radius = input("Enter Radius: ")

    if float(radius) > 0:
        print(f"Area of Circle: {area_of_circle(float(radius)):.2f}")

    else:
        print("Enter a valid radius")
        

except ValueError:
    print("Numbers only")

except TypeError:
    print("Positive Numbers only. Meaning numbers greater than 0.")

except KeyboardInterrupt:
    print("Unusual Crash Detected.")

