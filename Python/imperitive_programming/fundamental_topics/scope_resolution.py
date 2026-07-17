""" Scope Resolution """

# Variable Scope = Variable Visibility and Accessibility

# Scope Resolution = (L)ocal -> (E)nclosed -> (G)lobal -> (B)uilt-In
# from smallest to biggest i.e. ascending

# LOCAL

def local1():
    x = 1 # local variable
    print(x)

def local2():
    x = 2 # local variable
    print(x)

local1()
local2()

# ENCLOSED

def enclosed1():
    x = 1 # enclosed variable

    def enclosed2():
        print(x)
    enclosed2()

enclosed1()

# GLOBAL

def global1():
    print(x)

def global2():
    print(x)

x = 3 # global variable

global1()
global2()

# BUILT-IN

from math import e # from MODULE import FUNCTION

def built_in():
    print(e) # built-in variable

built_in()

