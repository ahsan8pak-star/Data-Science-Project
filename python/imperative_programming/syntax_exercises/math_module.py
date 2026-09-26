"""
A module of constants - pi, Euler's number and friends.

The leaf of a two-file import pair: math_file.py imports from here, which is
the simplest possible demonstration that a plain .py file can be a module.
"""

pi = 3.14159

def square(x):
   return x ** 2

def cube(x):
   return x ** 3

def circumference(radius):
   return 2 * pi * radius

def area(radius):
   return pi * radius ** 2


