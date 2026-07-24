# Abstract Classes: Can't be instantiatied (i.e. can't be used for its main constructor e.g. def __init__ (self...):)
# Contain abstract methods, declaring no implementation
# Prevents Instantiation of the class itself (prevents error executable files)
# Require 'children' (child classes) to use inherited abstract methods

# from (a)bstract (b)ase (c)lass import (A)bstract(B)ase(C)lass
from abc import ABC, abstractmethod 

class Vehicle(ABC):

    @abstractmethod 
    def go(self):
        pass

    @abstractmethod
    def stop(self):
        pass

# vehicle = Vehicle() # TypeError -> Can't instantiate abstract classes with abstract methods

class Car(Vehicle): # Parent(Abstract Child Class) -> Must Use Abstract Classes & Methods

    def go(self):
        print("You are driving a car")

    def stop(self):
        print("You stopped the car")

car = Car()

class Motorcycle(Vehicle): # If Abstract Class used, ALL Abstract Methods must be used

    def go(self):
        print("You are riding a motorcycle")

    def stop(self):
        print("You stopped the motorcycle")

motorcycle = Motorcycle()

class Boat(Vehicle):

    def go(self):
        print("You are sailing a boat")

    def stop(self):
        print("You anchored the boat")

boat = Boat()

