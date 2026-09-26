"""
Constructors - __init__ and the other dunder methods Python calls implicitly.

__init__ sets up state and runs after the object exists; __new__ allocates it.
Also shows the str and repr methods, since object.__str__ falling back to repr
is a common source of confusing output.
"""

# Constructor = Function's called at the time of the object's creation

class Point():

    def __init__ (self, x, y):
        self.x = x
        self.y = y

point = Point(5, 6)
print(f"x = {point.x}") 
print(f"y = {point.y}")


