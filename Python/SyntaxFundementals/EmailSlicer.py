email = input("Enter your email: ")

index = email.index("@")

username = email[: index] # username = email[: email.index("@")]

domain = email[index + 1 :] # [index:] -> "@gmail.com" (@ included), [index + 1 :] -> "email.com" (@ excluded)
# domain = email [email.index("@") + 1 :]

print(f"Email: {email}")
print(f"Username: {username}")
print(f"Email Domain: {domain}")

