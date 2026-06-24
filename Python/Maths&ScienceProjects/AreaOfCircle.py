def area_of_circle(radius):

    pi = 3.14
    area = pi * radius * radius
    
    return area

try: 
    radius = input("Enter Radius: ")

    while radius > 0:
        print(area_of_circle(radius))

except ValueError:
    print("Numbers only")

except TypeError:
    print("Positive Numbers only. Meaning greater than 0.")

except KeyboardInterrupt:
    print("Unusual Crash Detected.")

