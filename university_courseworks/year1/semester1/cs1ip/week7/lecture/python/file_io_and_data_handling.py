# Writing formatted records using context managers
with open("clients.txt", "w") as output:
    output.write(f"{100} {'Bob'} {'Blue'} {24.98:.2f}\n")
    output.write(f"{200} {'Steve'} {'Green'} {-345.67:.2f}\n")

# Reading sequential tokens
with open("clients.txt", "r") as input_file:

    for line in input_file:
        parts = line.split()

        if parts:
            account = int(parts[0])
            first_name = parts[1]
            last_name = parts[2]
            balance = float(parts[3])

            print(f"account {account} from {first_name} {last_name} has balance {balance:.2f}")

