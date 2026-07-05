def volume (x, y, z):
    return x * y * z

try:
    x = float(input("Enter Length (cm): "))
    y = float(input("Enter Width (cm): "))
    z = float(input("Enter Depth (cm): "))

    result = volume(x, y, z)

    print(f"Volume: {round(result, 2)} cm^3")

except ValueError:
    print("Numbers only")

