# If and Else Statements  

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


# For Loops and While Loops

for i in range(5): # Iterates through a sequence (like a range of numbers, a string, or a list)
    if i % 2 == 0: # Condition satisfied scenario
        print(f"{i} is even") # f-string is used to format the output by embedding the value of i within the string.
    else: 
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


# Ternary Operators on all scenarios, including all data types

is_raining = True
weather = "rainy" if is_raining else "sunny" # Ternary operator assigns "rainy" to weather if is_raining is True, otherwise it assigns "sunny"
print(weather)

# Expected Output: "rainy"
# Actual Output:   "rainy"
# Reason: Since is_raining is True, the ternary operator evaluates to "rainy" and assigns it to the variable weather.

age = 20
status = "Allowed" if age >= 21 else "Rejected" # Ternary operator
print(status)

# Expected Output: "Rejected"
# Actual Output:   "Rejected"
# Reason: Since age is 20, which is less than 21
# The ternary operator evaluates to "Rejected".


# Switch Case Statements

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


# Logical Operators (and, or, not)

income = 50000
has_good_credit = True

if income >= 40000 and has_good_credit: # BOTH must be true
    print("Eligible for loan")
    
# Expected Output: "Eligible for loan"
# Actual Output:   "Eligible for loan"
# Reason: Both the income requirement AND the credit requirement are met simultaneously.

is_weekend = False
on_vacation = True

if is_weekend or on_vacation: # ONLY ONE needs to be true
    print("You don't have to work!")
    
# Expected Output: "You don't have to work!"
# Actual Output:   "You don't have to work!"
# Reason: Although 'is_weekend' is False, the 'or' operator allows execution because 'on_vacation' evaluates to True.


# Loop Control Statements (Break, Continue)

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

# Reason: The loop prints 0, 1, and 2. When 'number' equals 3, the break statement is triggered, forcing the entire loop to stop immediately before 3 can be printed.

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

# Reason: The loop prints 0 and 1. When 'number' equals 2, the continue statement forces Python to skip the rest of the loop block (skipping the print) and jump straight to the next iteration (3).


# Logical NOT (Reversing a boolean)


is_logged_in = False
if not is_logged_in: # Reads as: "If is_logged_in is NOT True"
    print("Please log in to continue.")

# Expected Output: "Please log in to continue."
# Actual Output:   "Please log in to continue."
# Reason: 'is_logged_in' is False. The 'not' operator flips it to True for the sake of the if-statement, allowing the code to run.


# Membership Operators (in, not in)


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


# The 'pass' Statement (Structural Placeholder)

x = 10
if x > 5:
    pass # A null operation. Tells Python "Do nothing, but don't crash."
    if x == 10: 
        print("x is exactly 10")

# Expected Output: "x is exactly 10"
# Actual Output:   "x is exactly 10"
# Reason: The outer condition allows the code inside to run. The 'pass' statement acts as a placeholder doing nothing, allowing the inner nested condition to evaluate and run.

# Nested Conditions and Loops
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
# The condition 'i == j' is only true when both 'i' and 'j' are 0 and when both are 1, resulting in the two print statements. When 'i' is 2, there is no match with 'j', so nothing is printed for that

# Iterables

fruits = ["apple", "banana", "cherry"]
for fruit in fruits: # Iterating through a list
    print(fruit)

# Expected Output:
# "apple"
# "banana"
# "cherry"

# Actual Output:
# "apple"
# "banana"
# "cherry"

# Reason: The for loop goes through each element in the 'fruits' list one by one, assigning it to the variable 'fruit' and printing it vertically, not horizontally.

# Infinite Loops (use with caution!)

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

# Reason: The while loop is designed to run indefinitely because the condition 'True' is always satisfied. However, we added a break condition to stop it after 5 iterations for testing purposes.
