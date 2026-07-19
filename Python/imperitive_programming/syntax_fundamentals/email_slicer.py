# Essential for the specific Exception to be called via pytest cases to be executed as a function
def slice_email(email):
            
    if "@" not in email: 
        raise ValueError("Invalid email: missing @ symbol")
    
    index = email.index("@")
        
    username = email[: index] # username = email[: email.index("@")]

    domain = email[index + 1 :] # [index:] -> "@gmail.com" (@ included), [index + 1 :] -> "email.com" (@ excluded)
    # domain = email [email.index("@") + 1 :]


    return username, domain

if __name__ == "__main__":
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

                # This calls the function that raises the ValueError
                username, domain = slice_email(email)

                if "@" in email and "." in email: # "@" and "." must be included in 'email'
                    print(f"Email: {email}")
                    print(f"Username: {username}")
                    print(f"Email Domain: {domain}")
                    break # Stops the program running i.e. it's done its task

                else:
                    print("Invalid email. Try again.")

        except ValueError as e: # Prints the specific error from the function to allow pytest case to run the raise exception test casing
            print(e)

        except KeyboardInterrupt: # Stops the program even if it unexpectedly crashes to reduce further conflict
            print("\nWe apologise for any inconvenience.")
            print("Have a great day!")
            break

