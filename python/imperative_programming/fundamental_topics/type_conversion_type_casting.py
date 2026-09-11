a = "A.I.M"
b = 8
c = 3.14
d = True

print(str(a)) # converts variable a to a string
# Expected Output: "A.I.M"
# Actual Output:   "A.I.M"
# Reason: Variable a is already a string, so the str() function returns it unchanged.

print(str(b)) # converts variable b to a string
# Expected Output: "8"
# Actual Output:   "8"
# Reason: The integer 8 is converted to the string "8" by the str() function.

print(str(c)) # converts variable c to a string
# Expected Output: "3.14"
# Actual Output:   "3.14"
# Reason: The float 3.14 is converted to the string "3.14" by the str() function.  

print(str(d)) # converts variable d to a string
# Expected Output: "True"
# Actual Output:   "True"
# Reason: The boolean value True is converted to the string "True" by the str() function.

print (f"a = {a}, b = {b}, c = {c}, d = {d}") # concatenates the string representations of a, b, c, and d with commas and spaces
# Expected Output: "a = A.I.M, b = 8, c = 3.14, d = True"
# Actual Output:   "a = A.I.M, b = 8, c = 3.14, d = True"
# Reason: Each variable is converted to its string representation and concatenated with commas and spaces, resulting in the final string "a = A.I.M, b = 8, c = 3.14, d = True".

e = float(b) + c # converts variable b to a float and adds it to variable c
print(e)
# Expected Output: 11.14
# Actual Output:   11.14
# Reason: The integer 8 is converted to the float 8.0, and then added to 3.14, resulting in 11.14.

f = int(c) + b # converts variable c to an integer and adds it to variable b
print(f)
# Expected Output: 11
# Actual Output:   11
# Reason: The float 3.14 is converted to the integer 3 (truncating the decimal part), and then added to 8, resulting in 11.

print(type(a)) # checks the type of variable a
# Expected Output: <class 'str'>
# Actual Output:   <class 'str'>
# Reason: Variable a is a string, so the type() function returns <class 'str>

print(type(b)) # checks the type of variable b
# Expected Output: <class 'int'>
# Actual Output:   <class 'int'>
# Reason: Variable b is an integer, so the type() function returns <class 'int>

print(type(c)) # checks the type of variable c
# Expected Output: <class 'float'>
# Actual Output:   <class 'float'>
# Reason: Variable c is a float, so the type() function returns <class 'float>

print(type(d)) # checks the type of variable d
# Expected Output: <class 'bool'>
# Actual Output:   <class 'bool'>
# Reason: Variable d is a boolean, so the type() function returns <class 'bool>

