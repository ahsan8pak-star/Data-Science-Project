import sys

with open(sys.argv[1], 'w') as file:
    username = input("Enter your name:\n")
    file.write(f'Hello {username}!\n')

