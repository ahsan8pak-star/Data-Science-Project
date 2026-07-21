class Point(): # Pascal Naming Convention - > Initialise every word in capital letters

    def move(self):
        print("move")

    def draw(self):
        print("draw")


point1 = Point() # variable = class
point1.draw() # "draw"
point1.move() # "move"

# Another example of variable assignment
# Better to use a constructor to improve this

point1.x = 1
point1.y = 2

print(point1.x)
print(point1.y)

point2 = Point()

point2.x = 3
point2.y = 4

print(point2.x)
print(point2.y)

