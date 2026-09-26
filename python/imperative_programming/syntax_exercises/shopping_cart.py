"""
Shopping cart - add items, update quantities and total the basket.

cart() holds the items in a dictionary keyed by name, so a repeated add
updates the quantity rather than duplicating the row. Totalling walks
.items() and multiplies price by count.
"""

def cart():

    # Starting Point

    fruits = [] 
    prices = []

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
    
    return fruits, prices # returns the main variables back to the function

try:
    fruits, prices = cart() # calls the function IN ORDER Respectively

    print("=================")
    print("  SHOPPING CART  ")
    print("=================")

    total = 0

    # zip() is used neatly pair the 'fruits' and 'prices'
    for fruit, price in zip(fruits, prices): # Has to be in order respectively
        print(f"{fruit}: £{price:.2f}") # Shows the price of each fruit
        total += price # Every price is added to the total

    print(f"Total: £{total:.2f}")

except ValueError:
    print("Enter a valid number")

except KeyboardInterrupt:
    print("Program Crashed!")

except EOFError:
    print("Program Completed.")


