"""
The importer half of the two-file math example.

Imports from math_module, which is a bare sibling import and therefore only
resolves when the folder is on sys.path. The smallest demonstration that
importing is how one file gets at another's names.
"""

import math_module

pi_result = math_module.pi
print(pi_result)

square_result = math_module.square(2)
print(square_result)

cube_result = math_module.cube(3)
print(cube_result)

circumference_result = math_module.circumference(4)
print(circumference_result)

area_result = math_module.area(5)
print(area_result)


