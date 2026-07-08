import time

def count(end, start=0): # prevents an error when the user starts their input as START rather than END
    for seconds in range(start, end + 1): # [ end + 1 ] is exclusive, making [ end ] as the final index
        print(seconds)
        time.sleep(1)
    print("TIMES UP!")

# INDIVIDUAL Outputs:

print(count(1))

print(count(2))

print(count(3))

print(count(4))

print(count(5))

print(count(10))

print(count(15))

print(count(20))

print(count(25))

print(count(30))