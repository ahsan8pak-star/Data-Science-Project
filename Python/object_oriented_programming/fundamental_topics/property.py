# @property = Decorator used to define a method as a property (it can be accessed like an attribute)
# Adds additional logic when reading, writing, or deleting attributes
# Provides a getter, setter, and deleter method

class Rectangle:
    def __init__(self, width, height):
        self._width = width
        self._height = height

    @property # under (centimeters) cm units
    def width(self):
        return f"{self._width:.2f}cm"

    @property
    def height(self):
        return f"{self._height:.2f}cm"

    @property
    def area(self):
        return f"{self._width * self._height:.2f}cm²"

    @width.setter 
    def width(self, new_width):
        if new_width > 0:
            self._width = new_width
        else:
            print("Has to be Non-Zero Positive Widths -> W > 0")

    @height.setter
    def height(self, new_height):
        if new_height > 0:
            self._height = new_height
        else:
            print("Has to be Non-Zero Positive Heights -> H > 0")

    @width.deleter
    def width(self):
        del self._width
        print("Width has been deleted")

    @height.deleter
    def height(self):
        del self._height
        print("Height has been deleted")

    def __str__(self):
        return (
            f"--- Rectangle ---\n"
            f"Width: {self._width:.2f}cm\n"
            f"Height: {self._height:.2f}cm\n"
            f"Area: {self._width * self._height:.2f}cm²\n"
        )

rectangle1 = Rectangle(1, 2)
rectangle2 = Rectangle(3, 4)
rectangle3 = Rectangle(5, 6)

print(rectangle1)
print(rectangle2)
print(rectangle3)

