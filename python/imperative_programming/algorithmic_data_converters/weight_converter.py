weight = input("Weight: ")
if len(weight) == 0 or weight == "0":
    print("You must weigh something")
else:
    try:
        w = float(weight)
    except ValueError:
        print("Invalid weight")
    else:
        unit = input("Lb(s) or Kg(s): ")
        if unit and unit.lower()[0] == "l":
            new = w * 0.45
            print(f"You weigh {new} kilograms.")
        elif unit and unit.lower()[0] == "k":
            new = w / 0.45
            print(f"You weigh {new} pounds.")
        else:
            print("Only pounds and kilos.")

