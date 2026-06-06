# For finding all even numbers from 1 to 10

count  = 0
for i in range (1, 10): # 10 is not included
    if i % 2 == 0:
        print(i)
        count += 1
print ("We have " + str(count) + " even numbers")

# Finding all odd numbers from the first 10 numbers

count = 0
for i in range (1, 10): # 10 is not included
    if i % 2 == 1:
        print(i)
        count += 1
print ("We have " + str(count) + " odd numbers")
