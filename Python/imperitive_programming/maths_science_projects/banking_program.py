def show_balance(balance):

    print("\n---------------------------")
    print(f"| {f'Balance: £{balance:.2f}':^23} |")
    print("---------------------------")

def deposit():

    user_input = input("\nEnter Deposit: ")    

    try:
        amount = float(user_input)
        
        if amount < 0:
            print("\nInvalid Amount. ")
            print("Enter Positive Deposits.")
            return 0
        
        # Checks for 2 conditions:
        # 1) If a decimal point ( . ) is present [Important for Condition 2]
        # 2) If the digits after the decimal point is greater than 2 [ESSENTIAL]

        elif "." in user_input and len(user_input.split(".")[1]) > 2:
            print("\nInvalid Amount.")
            print("Funds have to be within 2 decimal places.")
            return 0
        
        else:
            return amount
            
    except ValueError:
        print("\nInvalid Input. Numbers Only.")
        return 0

def withdraw(balance):
    
    try:
        amount = float(input("\nEnter Withdrawl: "))
        
        if amount > balance:
            insufficient_funds = amount - balance

            print("\nInsufficient Funds.")
            print(f"Balance: £{balance:.2f}")
            print(f"You need £{insufficient_funds:.2f} to complete transaction.")

            return 0
            
        elif amount < 0:
            print("\nNo Negative Amounts.")
            return 0
            
        else:
            leftover = balance - amount

            print(f"\nYou have withdrew £{amount:.2f}.")
            print(f"You have £{leftover:.2f} left.")
            return amount
            
    except ValueError:
        print("\nInvalid Input. Numbers Only.")
        return 0

def main():
    balance = 0
    is_running = True

    print("\n-----------------------")
    print("|   Banking Program   |")
    print("-----------------------")

    while is_running:
        
        print("\n-------------------")
        print("|    Main Menu    |")
        print("-------------------")
        print("| 1. Show Balance |")
        print("| 2. Deposit      |")
        print("| 3. Withdraw     |")
        print("| 4. Exit         |")
        print("-------------------")

        choice = input("\nEnter Option (1-4): ")

        match choice:
            case "1":
                show_balance(balance)
            
            case "2":
                balance += deposit()

            case "3":
                balance -= withdraw(balance)
            
            case "4":
                is_running = False   

            case _:
                print("\nInvalid Choice.")
                print("Try Again.")

    print("\n>>> Shutting Down... <<<")

if __name__ == '__main__':
    main()

