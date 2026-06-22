# Strings

first_name = "Ahsan"
last_name = "Iqbal"
date_of_birth = "28/09/2006"
email = "ahsan8pak@gmail.com"
favourite_team = "Arsenal"

print(f"Hi, {first_name} {last_name}.")
print(f"You are born from {date_of_birth}.")
print(f"This is your email: '{email}'.")
print(f"And {favourite_team} is your favourite team!")


# Integers

age = 21
quantity = 85
number_of_games = 100
left = number_of_games - quantity

print(f"You are {age} years old.")
print(f"You have {quantity} Xbox 360 games.")
print(f"You need {left} more games, to complete your {number_of_games} Xbox collection!")

# Float

price = 12.99
quantity = input("How many orders? ")
total = price * int(quantity)

print(f"Price: £{total}")


revenue = 100000

costs = input("How much did you spend? ")

income = revenue - int(costs)

debt = int(costs) - revenue

if income <= 0:
    print(f"You're broke. You have £{income}. You owe £{debt}")

else:
    print(f"You have £{income} in your account.")


# Boolean

is_student = True
is_admin = False
is_new = False
is_regular = True
is_online = True

print(f"Student: {is_student}")
print(f"Admin: {is_admin}")
print(f"Starting: {is_new}")
print(f"Currently Studying: {is_regular}")
print(f"Online: {is_online}")

if is_online == True:

    if is_student and is_admin == True:
        print("Stop Lying, or you will be kicked out.")

    elif is_new and is_regular == True:
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