try:
    rows = int(input("Enter # of rows: "))
    columns = int(input("Enter # of columns: "))
    symbol = input("Enter a symbol: ")

    if symbol.isalpha() or symbol.isdigit():
        print("Can't be a letter nor a number. Try again")
    
    else:
        for row in range(rows):
            for column in range(columns):
                print(symbol, end="")
            print()
except ValueError:
    print("Invalid Input. Try Again.")

