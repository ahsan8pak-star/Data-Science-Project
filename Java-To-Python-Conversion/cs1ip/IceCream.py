# Constants defined outside the loop/function
CONE_PRICE = 100
VANILLA_PRICE = 19
CHOCOLATE_PRICE = 34
STRAWBERRY_PRICE = 0

def IceCream():

    while True:
        flavour = input("Would you like (v)anilla, (c)hocolate or (s)trawberry? ").lower()

        if flavour not in ("v", "c", "s"):
            print("We don't have that flavour.\n")
            continue  # Prompt the user again

        try:
            scoops = int(input("How many scoops would you like? "))

        except ValueError:
            print("Please enter a valid number.\n")
            continue

        # Scoop validation
        match scoops:
            case 1 | 2 | 3:
                pass  # Valid scoops, move forward

            case 0:
                print("We don't sell just a cone.\n")
                continue

            case _:
                print("That's too many scoops to fit in a cone.\n")
                continue

        # Flavour pricing
        match flavour:
            case "v":
                price_per_scoop = VANILLA_PRICE

            case "c":
                price_per_scoop = CHOCOLATE_PRICE

            case "s":
                price_per_scoop = STRAWBERRY_PRICE

        # Maths & Output
        total_pence = CONE_PRICE + (price_per_scoop * scoops)
        total_pounds = total_pence / 100.0
        print(f"That will be £{total_pounds:.2f} please.")
        break  # Exit loop after successful calculation

# Run the function
IceCream()

