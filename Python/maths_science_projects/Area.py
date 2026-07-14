def area (x, y):
    return x * y

def calculate():

    try:
        x = float(input("Enter Length (cm): "))
        y = float(input("Enter Width (cm): "))

        result = area(x, y)

        print(f"Area: {round(result, 2)} cm^2")

    except ValueError:
        print("Numbers only")

if __name__ == "__main__":
    calculate()