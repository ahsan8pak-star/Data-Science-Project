# Starting Point

fruits = [] 
prices = []
total = 0

while True: # While this entire function is True i.e. Program Running
    fruit = input("Enter your fruit item (c = checkout): ")

    if fruit.lower() == "c":
        break # Breaks the while loop

    else:
        price = input(f"Enter the price for {fruit} (c = checkout): £ ")

        if price.lower() == "c":
            break # Essential if they accidentally added an extra item not needed 

        else:
            fruits.append(fruit) # Adds the new fruit in the list 'fruits'
            prices.append(float(price)) # Adds the new price under 'prices' as a floating point number

print("=================")
print("  SHOPPING CART  ")
print("=================")

for fruit in fruits:
    print(fruit, end=" ") # Every fruit item under the list 'fruits' gets printed
    # [ end=" " ] -> provides a space after every item

for price in prices:
    total += price # Every price item under the list 'prices' gets added to the total

print(f"Total: £{total:.2f}") # Print the total in 2 decimal places

