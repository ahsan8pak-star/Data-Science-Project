username = input("Username: ").strip() # Allows the user to write down the username clearly
# it'll automatically strip / compress after execution

print(f"Welcome, {username}!" if len(username) <= 12 and " " not in username and not any(char.isdigit() for char in username) else "Bye!")

# This translates to:

# if len(username) <= 12 and " " not in username and not any(char.isdigit() for char in username):
#   print(f"Welcome, {username}!")
# else:
#   print("Bye!")

# [ len(username) <= 12 ] -> checks the length of the username by characters individually and sees if it's up to 12 characters.
# This includes spaces as well

# [ " " not in username ] -> confirms if " " (meaning whitespace) is not in username
# If detected it will print the else function -> [ "Bye!" ]

# [ not any(char.isdigit() for char in username) ] -> makes sure the username doesn't contain any digits i.e. numbers MIXED within the string
# The reason for this is to include other characters such as symbols like . , / , \ , | , etc.
# otherwise, else will be exceuted -> [ "Bye!" ]

