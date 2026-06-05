count  = 0
for i in range (1, 10):
    if i % 2 == 0:
        print(i)
        count += 1
print ("We have " + str(count) + " even numbers")

count = 0
for i in range (1, 10):
    if i % 2 == 1:
        print(i)
        count += 1
print ("We have " + str(count) + " odd numbers")
