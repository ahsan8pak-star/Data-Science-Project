"""
Area of a rectangle from two sides.

The smallest of the geometry calculators, kept as the plain example the
rectangle-based scripts build on. area(x, y) is deliberately a single
unvalidated call: validation lives in the callers that prompt.
"""

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


