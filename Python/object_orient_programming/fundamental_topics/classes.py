# Object = "Bundle" of related attributes (variables) and methods (functions)
# e.g. phone, cup, book

# A "Class" is needed to create many objects
# Class = (Blueprint) used to design the structure and layout of an object

from car import Car # from car.py import class Car()

car1 = Car("Toyata Supra", 1998, "White", True)

print(car1) # Outputs memory address and not its attributes (variables)

print(car1.model)
print(car1.year)
print(car1.colour)
print(car1.for_sale)

car1.drive() # variable.method()
car1.stop() # car1 is within self.model assignment
car1.description()

# Logic about variables within methods
"""
car1 = Car(model... , colour...)

def Car(self, model... , colour...):
    self.model = model
    self.colour = colour

self.model = car1.model
self.colour = car1.colour
self = car1

car1.drive() = "You are driving a {self.colour == car1.colour} {self.model == car1.model}!"

{self.model == car1.model} = Toyota Supra
{self.colour == car1.colour} = White
"""


car2 = Car("BMW M3 GTR", 2005, "Blue", False)

print(car1) # Outputs a unique memory address dedicated for this line of code

print(car2.model)
print(car2.year)
print(car2.colour)
print(car2.for_sale)

car2.drive()
car2.stop()
car2.description()

