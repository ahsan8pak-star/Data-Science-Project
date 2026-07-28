# Polymorphism = Objects taking Many Forms

# Two ways to achieve this:

# 1) Inheritence -> An Object treated the same type as a parent class
# 2) "Duck Typing" -> Object must have necessary attributes / methods

# Type 1 of Polymorphism, based from super.py and abstract_classes.py

import math

from abc import ABC, abstractmethod


class Shape:

    @abstractmethod
    def area(self):
        pass

class Circle(Shape):
    def __init__ (self, radius):
        self.radius = radius

    def area(self):
        return math.pi * (self.radius ** 2)

class Square(Shape):
    def __init__ (self, side):
        self.side = side

    def area(self):
        return self.side ** 2
    

class Triangle(Shape):
    def __init__ (self, base, height):
        self.base = base
        self.height = height

    def area(self):
        return  0.5 * self.base * self.height

class Cake: # Since 'def area(self)', This passes through a No AttributeError
    def __init__ (self, flavour, length, height):
        self.flavour = flavour
        self.length = length
        self.height = height

    def area(self):
        return  self.length * self.height

# Due to not having 'def area()' this cause an AttributeError 
# Since this is using an abstract class requiring ALL its abstract methods
class Pizza:
    def __init__ (self, toppings, radius):
        self.toppings = toppings
        self.radius = radius

shapes = [Circle(3), Square(4), Triangle(5, 6), Cake("Chocolate", 6, 6), Pizza("Magherita", 10) ]

for shape in shapes:
    print(f"Area: {shape.area():.2f}")

