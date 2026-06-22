item = input("Item: ")
price = float(input("Price: "))
quantity = int(input("Amount: "))

total = round((price * quantity), 2) # rounds the prices to 2 decimal places
# works best for large values

if quantity == 0:
    print("You bought nothing. See you later!")

elif quantity == 1:
    print(f"You bought only 1 {item}")
    print(f"Price: £{price:.2f}") # Uses 2 decimal places to replicate actual prices via '[ANY]:.2f'

else:
    print(f"You bought {quantity} {item}s")
    print(f"Total: £{total:.2f}")