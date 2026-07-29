# super() -> Function used in a child's class (subclass) to call methods from the parent's class (superclass)
# Extends the functionality of the inherited methods

import math

class Shape:
    def __init__(self, colour, is_fill):
        self.colour = colour
        self.is_fill = is_fill

    def description(self):
        print(f"\nA(n) {"Filled" if self.is_fill else "Unfilled"} {self.colour} Shape")


class Circle(Shape):
    def __init__(self, colour, is_fill, radius):
        super().__init__(colour, is_fill) # super() . [ Parent's Method ] ( [ Parent's Parameters ] )
        self.radius = radius

    def description(self):
        print(f"AREA: {(math.pi * (self.radius ** 2)):.2f}")
        super().description()
    
class Square(Shape):
    def __init__(self, colour, is_fill, side):
        super().__init__(colour, is_fill)
        self.side = side

    def description(self):
        print(f"AREA: {(self.side ** 2):.2f}")
        super().description()

class Triangle(Shape):
    def __init__(self, colour, is_fill, length, height):
        super().__init__(colour, is_fill)
        self.length = length
        self.height = height 

    def description(self):
        print(f"AREA: {(self.length * self.height):.2f}")
        super().description()

circle = Circle(colour = "Red", is_fill = True, radius = 5)
# circle = Circle("Red", True, 5)

square = Square("Blue", False, 10)
# square = Square(colour = "Blue", is_fill = False, side = 10)

triangle = Triangle("Yellow", True, 2, 3)

print("\n--- CIRCLE ---")
print(f"COLOUR: {circle.colour}")
print(f"FILLED: {circle.is_fill}")
print(f"RADIUS: {circle.radius}")
circle.description()

print("\n--- SQUARE ---")
print(f"COLOUR: {square.colour}")
print(f"FILLED: {square.is_fill}")
print(f"SIDE: {square.side}")
square.description()

print("\n--- TRIANGLE ---")
print(f"COLOUR: {triangle.colour}")
print(f"FILLED: {triangle.is_fill}")
print(f"LENGTH: {triangle.length}")
print(f"HEIGHT: {triangle.height}")
triangle.description()

