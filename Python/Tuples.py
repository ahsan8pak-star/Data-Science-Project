# Tuples 

numbers = (1, 2, 3) # Immutable = can't be changed at all

# Example of this:

# numbers[0] = 10
# print(numbers[0]) 
# Output:
# TypeError - Meaning tuples can't be changed once the items has been made

print(numbers[0]) # 1
print(numbers[1]) # 2
print(numbers[2]) # 3

print(numbers[-1]) # 3
print(numbers[-2]) # 2
print(numbers[-3]) # 1

print(numbers.index(1)) # Finds position index of item 1
print(numbers.index(2)) # Finds position index of item 2
print(numbers.index(3)) # Finds position index of item 3

print(numbers.count(0)) # Number of times item 0 appeared
print(numbers.count(1)) # Number of times item 1 has appeared
print(numbers.count(2)) # Number of times item 2 has appeared
print(numbers.count(3)) # Number of times item 3 has appeared
print(numbers.count(4)) # Number of times item 4 has appeared

# Unpacking

coordinates = (1, 2, 3)

result = coordinates[0] * coordinates[1] * coordinates[2]
print(result) # Outputs the multiplication of the coordinates values

'''

x = coordinates[0]
y = coordinates[1]
z = coordinates[2]

'''
x, y, z = coordinates # an alternative to the code above made as a multi line comment
print(x) # 1
print(y) # 2
print(z) # 3

