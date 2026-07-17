""" Module Descriptions """

# Files containing specific porgrams to execute wihin the program
# 'import' -> include modules
# Useful to use other in-built programs, making the program reusable

print(help("modules")) # Print all types of modules to be imported

print(help("math")) # show all 'math' module imports e.g. math.pi

print(help("string")) # show all 'string' module imports e.g. string.digits

print(help("time")) # show all 'time' module imports e.g. time.sleep()

""" Module Examples """

# Printing pi:

import math # module
print(math.pi) 

import math as m # module assignment
print(m.pi)

from math import pi # most risky due to potential conflicts
print(pi)

""" Module Conflict Example """

from math import e # exponential value

a, b, c, d, e = 1, 2, 3, 4, 5

print(e ** a) # 5
print(e ** b) # 25
print(e ** c) # 125
print(e ** d) # 625
print(e ** e) # 3125

# Reason: exponential value (e) has been replaced by integer 5

# Solution: use 'import math' instead and it'll be 'math.e'

""" Solution Example """

import math

a, b, c, d, e = 1, 2, 3, 4, 5

print(math.e ** a) # 5
print(math.e ** b) # 25
print(math.e ** c) # 125
print(math.e ** d) # 625
print(math.e ** e) # 3125