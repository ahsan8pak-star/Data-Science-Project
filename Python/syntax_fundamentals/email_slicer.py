while True: # While the program is running
    try: # main code
        email = input("Enter your email (or 'q' to quit): ").strip() # prevents accidental <ENTER> imputs

        # Catch empty inputs safely before indexing to prevent IndexError
        if not email:
            print("No Input Made. Try again.")
            continue

        if email.lower() == 'q':
            print("Shutting down...")
            break

        else: # continues the main program
            index = email.index("@")

            username = email[: index] # username = email[: email.index("@")]

            domain = email[index + 1 :] # [index:] -> "@gmail.com" (@ included), [index + 1 :] -> "email.com" (@ excluded)
            # domain = email [email.index("@") + 1 :]

            if "@" in email and "." in email: # "@" and "." must be included in 'email'
                print(f"Email: {email}")
                print(f"Username: {username}")
                print(f"Email Domain: {domain}")
                break # Stops the program running i.e. it's done its task

            else:
                print("Invalid email. Try again.")

    except ValueError: # Allowing in the form of strings i.e. prevents unexpected crashes
        print("Invalid input. Avoid Typo Errors.")

    except KeyboardInterrupt:
        print("We apologise for any inconvenience.")
        print("Have a great day!")

