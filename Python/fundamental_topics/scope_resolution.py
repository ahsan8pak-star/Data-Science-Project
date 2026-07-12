# LOCAL

def function_local1():
    x = 1 #local
    print(x)

def function_local2():
    x = 2 #local
    print(x)

function_local1()
function_local2()

# ENCLOSED

def function_enclosed_3():
    x = 1 # enclosed variable

    def function_enclosed4():
        print(x)
    function_enclosed4()

function_enclosed_3()

# GLOBAL

def function_global5():
    print(x)

def function_global6():
    print(x)

x = 3 # global variable

function_global5()
function_global6()

# BUILT-IN

from math import e 

def function_built_in7():
    print(e)

function_built_in7()

