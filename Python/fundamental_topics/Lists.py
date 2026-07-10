"""Lists Indexing"""

# [START : END : STEP] -> Ordered, Changable and can include Duplicate items.

names = ["Ahsan", "Yahya", "Matthew", "Ahnaf", "Hamza"]
# names = [0, 1, 2, 3, 4] -> [1st, 2nd, 3rd, 4th, 5th]
# names = [-5, -4, -3, -2, -1] -> [1st, 2nd, 3rd, 4th, 5th]

print(names[0]) # Ahsan
print(names[1]) # Yahya
print(names[2]) # Matthew
print(names[3]) # Ahnaf
print(names[4]) # Hamza

print(names[-1]) # print(names[4]) -> Hamza
print(names[-2]) # print(names[3]) -> Ahnaf
print(names[-3]) # print(names[2]) -> Matthew
print(names[-4]) # print(names[1]) -> Yahya
print(names[-5]) # print(names[0]) -> Ahsan

print(names[:]) # [Ahsan, Yahya, Matthew, Ahnaf, Hamza] 

print(names[0:]) # [Ahsan, Yahya, Matthew, Ahnaf, Hamza] 
print(names[1:]) # [Yahya, Matthew, Ahnaf, Hamza]
print(names[2:]) # [Matthew, Ahnaf, Hamza]
print(names[3:]) # [Ahnaf, Hamza]
print(names[4:]) # [Hamza]
print(names[5:]) # []

print(names[-5:]) # [Ahsan, Yahya, Matthew, Ahnaf, Hamza] 
print(names[-4:]) # [Yahya, Matthew, Ahnaf, Hamza]
print(names[-3:]) # [Matthew, Ahnaf, Hamza]
print(names[-2:]) # [Ahnaf, Hamza]
print(names[-1:]) # [Hamza]

print(names[:0]) # [] 
print(names[:1]) # ['Ahsan']
print(names[:2]) # ['Ahsan', 'Yahya']
print(names[:3]) # ['Ahsan', 'Yahya', 'Matthew']
print(names[:4]) # ['Ahsan', 'Yahya', 'Matthew', 'Ahnaf']
print(names[:5]) # ['Ahsan', 'Yahya', 'Matthew', 'Ahnaf', 'Hamza']

print(names[:-5]) # []
print(names[:-4]) # ['Ahsan']
print(names[:-3]) # ['Ahsan', 'Yahya']
print(names[:-2]) # ['Ahsan', 'Yahya', 'Matthew']
print(names[:-1]) # ['Ahsan', 'Yahya', 'Matthew', 'Ahnaf']
print(names[:-0]) # [] 


"""List Methods"""

numbers = [5, 2, 1, 7, 4]

numbers.append(8) # [5, 2, 1, 7, 4, 8]
numbers.insert(0, 3) # [3, 5, 2, 1, 7, 4]
numbers.remove(7) # [5, 2, 1, 4]
numbers.clear() # []
numbers.count(1) # 1
numbers.pop() # [5, 2, 1, 7]
numbers.index(1) # 2
numbers.sort() # [1, 2, 4, 5, 7]
numbers.reverse() # [4, 7, 1, 2, 5] 
numbers.sort() # [1, 2, 4, 5, 7] 
# With numbers.sort() for numbers.reverse(): [7, 5, 4, 2, 1] 

print(numbers) # Testing each function, can't do all at once
print(numbers.index(1)) # 2
print(2 in numbers) # True
print(21 in numbers) # False
print(88 not in numbers) # True
print(numbers.count(1)) # 1

number = numbers.copy()
print(number) # [5, 2, 1, 7, 4]
# This when we can do whatever we do that new list (number)


""" Duplicates solution """

duplicates = [2, 2, 4, 6, 3, 4, 6, 1]

uniques = []

for duplicate in duplicates:
    if duplicate not in uniques:
        uniques.append(duplicate)
print(uniques)


""" Find Max iten in the list """

items = [3, 6, 2, 8, 4, 9]

max = items[0]

for item in items:
    if item > max:
        max = item
print(max)

# Output: 9


""" Find Min item in the list """

items = [3, 6, 2, 8, 4, 9]

min = items[0]

for item in items:
    if item < min:
        min = item
print(min) 

# Output: 2


""" 2D Lists / Matrices """

matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

print(matrix[0][0]) # row 1 column 1 -> 1
print(matrix[0][1]) # row 1 column 2 -> 2
print(matrix[0][2]) # row 1 column 3 -> 3
print(matrix[1][0]) # row 2 column 1 -> 4
print(matrix[1][1]) # row 2 column 2 -> 5
print(matrix[1][2]) # row 2 column 3 -> 6
print(matrix[2][0]) # row 3 column 1 -> 7
print(matrix[2][1]) # row 3 column 2 -> 8
print(matrix[2][2]) # row 3 column 3 -> 9


""" Identity Matrix """

for i in range(len(matrix)):
    row_output = []
    for j in range(len(matrix[i])):
        row_output.append(matrix[i][j] if i == j else 0)
    print(row_output)

"""
Output:

[1, 0, 0]
[0, 5, 0]
[0, 0, 9]

"""


""" Show matrix in a vertical list """

for row in matrix:
    for item in row:
        print(item)

"""
Output:
1
2
3
4
5
6
7
8
9
"""


""" Show matrix in a horizontal list """

horizontal_list = []

for row in matrix:
    for item in row:
        horizontal_list.append(item)
print(horizontal_list)

# [1, 2, 3, 4, 5, 6, 7, 8, 9]


""" List Comprehensions """


doubles = [x * 2 for x in range(1, 11)]
# Output: [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
# Reason: range(1, 11) generates numbers 1 to 10. Each number is multiplied by 2.

triples = [y * 3 for y in range(1, 11)]
# Output: [3, 6, 9, 12, 15, 18, 21, 24, 27, 30]
# Reason: Each number from 1 to 10 is multiplied by 3.

squares = [z * z for z in range(1, 11)]
# Output: [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
# Reason: Each number from 1 to 10 is squared (multiplied by itself).


fruits = ["apple", "orange", "banana", "coconut"]

uppercase_words = [fruit.upper() for fruit in fruits]
# Output: ['APPLE', 'ORANGE', 'BANANA', 'COCONUT']
# Reason: Runs the .upper() method on each fruit string to capitalize them.

fruit_chars = [fruit[0] for fruit in fruits]
# Output: ['a', 'o', 'b', 'c']
# Reason: Targets and extracts index 0 (the first character) of each fruit string.


number_list = [1, -2, 3, -4, 5, -6, 8, -7]

positive_number = [x for x in number_list if x >= 0]
# Output: [1, 3, 5, 8]
# Reason: Only includes numbers that are greater than or equal to 0.

negative_number = [x for x in number_list if x < 0]
# Output: [-2, -4, -6, -7]
# Reason: Only includes numbers that are strictly less than 0.

even_number = [x for x in number_list if x % 2 == 0]
# Output: [-2, -4, -6, 8]
# Reason: Only includes numbers where the remainder of division by 2 is 0.

odd_number = [x for x in number_list if x % 2 == 1]
# Output: [1, 3, 5, -7]
# Reason: Only includes numbers where division by 2 leaves a remainder of 1. (Note: In Python, negative odd numbers like -7 also return 1 when moduloed by 2!)


grades = [85, 42, 79, 90, 56, 61, 30]

passing_grades = [grade for grade in grades if grade >= 60]
# Output: [85, 79, 90, 61]
# Reason: Filters the grade list to only keep values of 60 or higher.


""" List Methods """

print(dir(names)) # Print all list methods as a help guide under ANY list variable name

print(help(names)) # Prints all the list methods and functions under a help guide and specify its uses accordingly

