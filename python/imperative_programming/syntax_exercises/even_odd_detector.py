"""
Even or odd - remainders as the test for divisibility.

n % 2 == 0 identifies an even number. The file also sweeps 0 to 10, which
shows why a leading zero in a result is a formatting artefact rather than a
numbering error.
"""

# For finding all even numbers from 0 to 10

count  = 0
for i in range (0, 11): # 11 is not included, making the range 0 to 10
    if i % 2 == 0:
        print(i)
        count += 1
print ("We have " + str(count) + " even numbers")

# Finding all odd numbers from the first 10 numbers

count = 0
for i in range (0, 11): 
    if i % 2 == 1:
        print(i)
        count += 1
print ("We have " + str(count) + " odd numbers")


