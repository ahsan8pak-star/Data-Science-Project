"""If and Else Statements"""

temperature = 25
if temperature > 30: # Condition satisfied scenario
    print("It's a hot day")
elif temperature > 20: # elif = else if
    print("It's a nice day")
elif temperature > 10:
    print("It's a bit cold")
else: # default / final condition 
    print("It's cold")

# Expected Output: "It's a nice day"

# Actual Output:   "It's a nice day"

# Reason: temperature doesn't meet the first condition (temperature > 30) is false
# It moves to the next condition (temperature > 20) which is true, and prints "It's a nice day".
# The remaining conditions are not evaluated because one of the conditions has already been satisfied.


"""For Loops and While Loops"""

for i in range(5): # Iterates through a sequence (like a range of numbers, a string, or a list)
    if i % 2 == 0: # Condition satisfied scenario
        print(f"{i} is even") 
    else: # (f"") method is used to format the output by embedding the value of i within the string
        print(f"{i} is odd")

# Expected Output:
# "0 is even"
# "1 is odd"
# "2 is even"
# "3 is odd"
# "4 is even"

# Actual Output:
# "0 is even"
# "1 is odd"
# "2 is even"
# "3 is odd"
# "4 is even"

# Reason: The loop iterates through the numbers 0 to 4. For each number
# It checks if the number is even (i % 2 == 0). 
# If the condition is true, it prints that the number is even; otherwise, it prints that the number is odd.


for num in range (1, 11, 2):
    print(num)

# Expected Output: 
"""
2
4
6
8
10
"""
# Actual Output:
"""
1
3
5
7
9
"""
# Reason: for num in range (1, 11, 2) -> (START, END, STEP) -> It goes theough every 2nd step / index of that range between 1 and 10.
# It doesn't mean every number divisble by 2 i.e. even is shown, rather it's for odd numbers due to its starting point being odd (1).


age = 15
while age < 18: # Condition satisfied scenario
    print("You are a minor: " + str(age))
    age += 1 # Incrementing age to eventually break the loop
# This runs when the while loop condition is no longer satisfied
print("You are an adult")

# Expected Output:
# "You are a minor: 15"
# "You are a minor: 16"
# "You are a minor: 17"
# "You are an adult"

# Actual Output:
# "You are a minor: 15"
# "You are a minor: 16"
# "You are a minor: 17"
# "You are an adult"

# Reason: The while loop continues to execute as long as the condition (age < 18) is true. 
# It prints the message indicating that the person is a minor along with their current age.
# Once age reaches 18, the condition becomes false, and the loop terminates.
# The normal code execution resumes after the loop terminates, printing "You are an adult".


name = "A.I.M"
while name == "": # while not name != ""
    print("Enter your name")
    break
print(f"Username: {name}")

# Expected Output:
# "Username: A.I.M"

# Actual Output:
# "Username: A.I.M"

# Reason: Since 'name' variable has been assigned by its string "A.I.M", it skips the while loop and directly prints out the name.
# break was used to prevent a constant recurring message of "Enter your name", leading to memory overload i.e. program crashing.


"""Ternary Operators on all scenarios, including all data types"""

is_raining = True
weather = "rainy" if is_raining else "sunny" # Ternary operator assigns "rainy" to weather if is_raining is True, otherwise it assigns "sunny"
print(weather)

# Expected Output: "rainy"

# Actual Output:   "rainy"

# Reason: Since is_raining is True, the ternary operator evaluates to "rainy" and assigns it to the variable weather.


age = 20
status = "Allowed" if age >= 21 else "Rejected" # Ternary operator
print(status)

# Expected Output: 
# "Rejected"

# Actual Output:   
# "Rejected"

# Reason: Since age is 20, which is less than 21
# The ternary operator evaluates to "Rejected".


"""Switch Case Statements"""

def get_day_name(day):
    match day: # match statement is used to compare the value of day against multiple cases
        case 1:
            return "Monday"
        case 2:
            return "Tuesday"
        case 3:
            return "Wednesday"
        case 4:
            return "Thursday"
        case 5:
            return "Friday"
        case 6:
            return "Saturday"
        case 7:
            return "Sunday"
        case _: # The underscore acts as the 'default' or 'else' case
            return "Invalid day"

print(get_day_name(3)) 
# Expected Output: "Wednesday"
# Actual Output:   "Wednesday"
# Reason: The match statement evaluates '3' and successfully matches it to 'case 3'.

print(get_day_name(7)) 
# Expected Output: "Sunday"
# Actual Output:   "Sunday"
# Reason: The match statement evaluates '7' and successfully matches it to 'case 7'.

print(get_day_name(0)) 
# Expected Output: "Invalid day"
# Actual Output:   "Invalid day"
# Reason: '0' does not match any of the defined cases (1 through 7), triggering the default 'case _'.


"""Logical Operators (and, or, not)"""

# AND

income = 50000
has_good_credit = True

if income >= 40000 and has_good_credit: # BOTH must be true
    print("Eligible for loan")
    
# Expected Output: "Eligible for loan"
# Actual Output:   "Eligible for loan"
# Reason: Both the income requirement AND the credit requirement are met simultaneously.

# OR

is_weekend = False
on_vacation = True

if is_weekend or on_vacation: # ONLY ONE needs to be true
    print("You don't have to work!")
    
# Expected Output: "You don't have to work!"
# Actual Output:   "You don't have to work!"
# Reason: Although 'is_weekend' is False, the 'or' operator allows execution because 'on_vacation' evaluates to True.

# NOT

is_admin = True

if is_admin != False: # NONE has to be true, meaning it's literally the opposite value
    print("Access Granted!") 

# Expected Output: "Access Granted!"
# Actual Ouput:    "Access Granted!"
# Reason: This means is_admin HAS to be True since NOT False == True

# Logical NOT (Reversing a boolean)

is_logged_in = False
if not is_logged_in: # Reads as: "If is_logged_in is NOT True"
    print("Please log in to continue.")

# Expected Output: "Please log in to continue."
# Actual Output:   "Please log in to continue."
# Reason: 'is_logged_in' is False. The 'not' operator flips it to True for the sake of the if-statement, allowing the code to run.


"""Loop Control Statements (Break, Continue)"""

for number in range(5):
    if number == 3:
        break # Stops the entire loop permanently
    print(number)

# Expected Output: 
# 0
# 1
# 2

# Actual Output: 
# 0
# 1
# 2

# Reason: The loop prints 0, 1, and 2. When 'number' equals 3
# The break statement is triggered, forcing the entire loop to stop immediately before 3 can be printed.


for number in range(4):
    if number == 2:
        continue # Skips the current iteration, but keeps looping
    print(number)

# Expected Output: 
# 0
# 1
# 3

# Actual Output: 
# 0
# 1
# 3

# Reason: The loop prints 0 and 1. When 'number' equals 2 
# The continue statement forces Python to skip the rest of the loop block (skipping the print) and jump straight to the next iteration (3).



"""Membership Operators (in, not in)"""

user_role = "Admin"
valid_roles = ["Admin", "Editor", "Moderator"]

if user_role in valid_roles: # Checks if the value exists inside the list
    print("Access Granted")

# Expected Output: "Access Granted"
# Actual Output:   "Access Granted"
# Reason: Python checks the entire 'valid_roles' list and finds an exact match for "Admin".


name = "A.I.M"
if "z" not in name: # Checks if the value is missing from the string
    print("The letter 'z' is missing.")

# Expected Output: "The letter 'z' is missing."
# Actual Output:   "The letter 'z' is missing."
# Reason: Python scans the string "A.I.M". Since "z" is nowhere to be found, the 'not in' condition evaluates to True.


"""The 'pass' Statement (Structural Placeholder)"""

x = 10
if x > 5:
    pass # A null operation. Tells Python "Do nothing, but don't crash."
    if x == 10: 
        print("x is exactly 10")

# Expected Output: "x is exactly 10"
# Actual Output:   "x is exactly 10"
# Reason: The outer condition allows the code inside to run. 
# The 'pass' statement acts as a placeholder doing nothing, allowing the inner nested condition to evaluate and run.


"""Nested Conditions and Loops"""

for i in range(3):
    for j in range(2):
        if i == j:
            print(f"i and j are equal: {i}")
        else:
            print(f"({i}, {j} are not equal)")

# Expected Output:
# "i and j are equal: 0"
# "(0, 1 are not equal)"
# "(1, 0 are not equal)"
# "i and j are equal: 1"
# "(2, 0 are not equal)"
# "(2, 1 are not equal)"

# Actual Output:
# "i and j are equal: 0"
# "(0, 1 are not equal)"
# "(1, 0 are not equal)"
# "i and j are equal: 1"
# "(2, 0 are not equal)"
# "(2, 1 are not equal)"

# Reason: The outer loop iterates through values of 'i' (0, 1, 2) and the inner loop iterates through values of 'j' (0, 1).
# The condition 'i == j' is only true when both 'i' and 'j' are 0 and when both are 1, resulting in the two print statements. 
# When 'i' is 2, there is no match with 'j', so the 'else' condition executes and prints that they are not equal.


for x in range (5): # for 5 times
    for y in range(1, 11): # from 1 to 10 (11 exclusive)
        print(y, end=" ") # print 1-10, 5 times. [ end=" " ] allows spaces in between numbers
    print() #  Allows each interation done (y) under a single line, meaning the next one will go to a new line (x)

# Expected Output:
"""
1 2 3 4 5 6 7 8 9 10
1 2 3 4 5 6 7 8 9 10
1 2 3 4 5 6 7 8 9 10
1 2 3 4 5 6 7 8 9 10
1 2 3 4 5 6 7 8 9 10
"""

# Actual Output:
"""
1 2 3 4 5 6 7 8 9 10
1 2 3 4 5 6 7 8 9 10
1 2 3 4 5 6 7 8 9 10
1 2 3 4 5 6 7 8 9 10
1 2 3 4 5 6 7 8 9 10
"""
# Reason: for x in range(5) -> every function underneath it, repeat it 5 times
# for y in range (1, 11) -> from number 1 to 10 (11 is exclusive)
# print(y, end=" ") # print 1-10 (function y). 
# end=" " -> This is the most crucial bit since this prevents all numbers printed vertically
# print() -> This means once the y function has been exceuted, repeat it under function x in a new line.
# This means repeat number 1 to 10 being outputted 5 times under each new line.


"""Iterables"""

# An object/collection that can return its elements one at a time, allowing it to be iterated over in a loop

name = "AIM"

for char in name:
    print(char, end=" | ")

# Expected Output:
# A | I | M

# Actual Output: 
# A | I | M

# Reason: Using for loop iterates every 'char(acter)' under the 'word' 'name'
# end= " | " -> two spaces in between the character symbol '|' i.e. prints in the same single line

# LISTS

numbers = [1, 2, 3, 4, 5]
for number in numbers:
    print(number, end=" ")

# Expected Output:
# 1 2 3 4 5

# Actual Output: 
# 1 2 3 4 5

# Reason: for loop iterates every 'number' under the list 'numbers' 
# and prints them under a single line with spaces based on the function 'end=" "'

countries = ["Algeria", "Belgium", "Canada"]
for country in countries: # Iterating through a list
    print(country)

# Expected Output:
# "Algeria"
# "Belgium"
# "Canada"

# Actual Output:
# "Algeria"
# "Belgium"
# "Canada"

# Reason: The for loop goes through each element in the 'countries' list one by one
# Assigning it to the variable 'country' and printing it vertically, not horizontally.

# TUPLES

coordinates = (1, 2, 3, 4, 5, 6)
for point in coordinates:
    print(point, end=" ")

# Expected Output:
# 1 2 3 4 5 6

# Actual Output: 
# 1 2 3 4 5 6

# Reason: for loop iterates every 'point' under the tuple 'coordinates' 
# and prints them under a single line with spaces based on the function 'end=" "'

# SETS

fruits = {"apple", "banana", "cherry"}
for fruit in fruits:
    print(fruit, end=" ")

# Expected Output:
# "apple" "banana" "cherry"

# Actual Output: FULLY RANDOM
# "apple" "banana" "cherry"
# OR
# "banana" "cherry" "apple"
# OR
# "cherry" "apple" "banana"

# Reason: for loop checks each element in the 'fruits' set individually
# Assigning to 'fruit' and prints it horizontally i.e. a single line through 'end=" "'
# Due to the nature of sets, it is Unordered, meaning it will print randomly

# DICTIONARIES

alphabet = {'A': 1, 'B': 2, 'C': 3}
for key in alphabet:
    print(key)

# Expected Output:
# A
# B
# C

# Actual Output:
# A
# B
# C

# Reason: Prints on the 'first' column i.e. only the keys vertically 
# Meaning after the first row has been printed, the next gets printed out i.e. a new line for every new key

for value in alphabet.values():
    print(value)

# Expected Output:
# 1
# 2
# 3

# Actual Output:
# 1
# 2
# 3

# Reason: Similar to keys except its the 'second / last' column being printed vertically

for key, value in alphabet.items():
    print(f"{key} = {value}")

# Expected Output:
# A = 1
# B = 2
# C = 3

# Actual Output:
# A = 1
# B = 2
# C = 3

alphabet = {'A': 1, 'B': 2, 'C': 3}
for key in alphabet:
    print(key)

# Expected Output:
# A
# B
# C

# Actual Output:
# A
# B
# C

# Reason: The .items() method returns both the key and value as a pair
# allowing the for loop to instantly unpack into two distinct variables (key and value) 
# and printed horizontally using an f-string.


"""Infinite Loops (Extreme Caution!!!)"""

counter = 0
while True: # This creates an infinite loop because the condition is always True
    print("This will run forever!")
    counter += 1
    if counter >= 5: # Adding a break condition to prevent actual infinite loop during testing
        break

# Expected Output:
# "This will run forever!"
# (repeated indefinitely until counter reaches 5)

# Actual Output:
# "This will run forever!"
# (repeated 5 times)

# Reason: The while loop is designed to run indefinitely because the condition 'True' is always satisfied. 
# However, we added a break condition to stop it after 5 iterations for testing purposes.


"""Conditional Expressions"""

num1 = 7
num2 = 8

print("Positive" if num1 > 0 else "Negative") # Similar to If-Else statements alone
print("Even" if num2 % 2 == 0 else "Odd")

a = 4
b = 6

max_num = a if num1 > num2 else b
min_num = a if num1 < num2 else b # Even works for assignments

print(max_num)
print(min_num)

age = 21

status = "Adult" if age >= 18 else "Child"

print(status)

temperature = 30

weather = "Hot" if temperature >= 20 else "Cold"

print(weather)

user_role = "admin"

access_level = "Access Granted" if user_role == "admin" else "Access Denied"

print(access_level)

