# Constructor = Function's called at the time of the object's creation

class Point():

    def __init__ (self, x, y):
        self.x = x
        self.y = y

point = Point(5, 6)
print(f"x = {point.x}") 
print(f"y = {point.y}")

