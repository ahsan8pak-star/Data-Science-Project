menu = {
    "pizza": 2.99,
    "nachos": 3.99,
    "tacos": 5.99,
    "fries": 1.99,
    "chips": 1.49,
    "pretzels": 3.49,
    "cupcakes": 0.99,
    "soda": 1.99,
    "lemonade": 3.99
}

# Used a dictionary ( {} )rather than a list ( [] ) to track local quantities per item
order = {} 
total = 0

print("======== MENU ========")
for key, value in menu.items():
    print(f"| {key:11}: £{value:.2f} |") 
print("======================\n")

while True:
    food = input("Select your order (q to quit): ").lower()
    if food == "q":
        print("Thank you for your order!")
        break
    elif menu.get(food) is not None:
        # Local increment: if item exists, add 1; otherwise, stay at 1
        order[food] = order.get(food, 0) + 1

print("--------- ORDER ---------")
# Unpack both the food name and its local quantity
for food, quantity in order.items():
    item_price = menu.get(food)
    item_total = item_price * quantity  # Calculate price based on quantity
    total += item_total
    
    # Correctly prints the actual quantity and the total price for that item
    print(f"| x{quantity} {food:11}: £{item_total:.2f} |")
    print("-------------------------")

print("===== PRICE =====")
print(f"| Total:  £{total:.2f} |")
print("=================")

print("==== PAYMENT ====")
print("| Cash or Card? |")
print("=================")