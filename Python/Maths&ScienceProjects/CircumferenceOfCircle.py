def circumference(radius):

    pi = 3.14
    area = pi * 2 * radius 
    
    return area

try: 
    radius = input("Enter Radius: ")

    while radius > 0:
        print(circumference(radius))

except ValueError:
    print("Numbers only")

except TypeError:
    print("Positive Numbers only. Meaning greater than 0.")

except KeyboardInterrupt:
    print("Unusual Crash Detected.")

