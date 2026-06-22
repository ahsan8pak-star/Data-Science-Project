is_student = input("Are you a student? (True / False): ")
is_admin = input("Are you an admin? (True / False): ")
is_new = input("Are you starting university? (True / False): ")
is_regular = input("Are you a current university student? (True / False): ")
is_online = input("Are you in your university account? (True or False): ")

print(f"Student: {is_student}")
print(f"Admin: {is_admin}")
print(f"Starting: {is_new}")
print(f"Currently Studying: {is_regular}")
print(f"Online: {is_online}")

try:
    if is_online[0].upper() == "T":
        
        if is_student[0].upper and is_admin[0].upper == "T":
            print("Stop Lying, or you will be kicked out.")

        elif is_new[0].upper() and is_regular[0].upper() == "T":
            choice = input("Accident or Intented? (A/I) ")
    
            if choice[0].upper() == "A":
                print("No problem. Try Again.")
    
            elif choice[0].upper() == "I":
                print("Leave or we will suspend you permanently!")
    
            else:
                print("Stop Messing Around! What is your answer?")

        else:
            print("Welcome to our university!")

    else:
        print(f"{is_online}. You are offline. You are unable to access this.")

except ValueError:
    print("Please type within boolean logic. True or False.")

