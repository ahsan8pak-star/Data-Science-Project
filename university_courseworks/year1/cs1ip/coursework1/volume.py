import math

def Volume(diameter):
    radius = (1 / 2.0) * float(diameter) # Diameter = 2 x Radius
    volume = (4.0 / 3.0) * math.pi * math.pow(float(radius), 3) # Sphere's Volume
    return float(volume)

if __name__ == "__main__":
    print(Volume(20.24))

