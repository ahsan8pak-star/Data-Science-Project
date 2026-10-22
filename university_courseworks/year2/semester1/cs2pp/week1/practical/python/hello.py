def greet(name):
    return f"Hello, {name}!"

try:
    name = input("What's your name? ")
    print(greet(name))

except Exception: 
    print("I didn't quite get that.\n Could you try again?")

