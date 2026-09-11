class BankAccount():
    def __init__(self, account_number, account_holder, balance=0):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Deposited £{amount}. New balance: £{self.balance}.")
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            print(f"Withdrew £{amount}. New balance: £{self.balance}.")
        else:
            print("Withdrawal amount must be positive and less than or equal to the current balance.")

    def get_balance(self):
        return self.balance

    def __str__(self):
        # Total width inside the box frame (between "| " and " |")
        width = 30  

        # TUI Display
        return ( 
            f"\n{'=' * (width + 4)}\n"
            f"| {f'Account Number: {self.account_number}':<{width}} |\n"
            f"| {f'Account Holder: {self.account_holder}':<{width}} |\n"
            f"| {f'Balance: £{self.balance:.2f}':<{width}} |\n"
            f"{'=' * (width + 4)}\n"
        )

bank_account1 = BankAccount("12345678", "John Doe", 1000)
print(bank_account1)  # Outputs the account details

bank_account1.deposit(500)  # Deposits £500
bank_account1.withdraw(200)  # Withdraws £200

print(bank_account1)  # Outputs the updated account details

