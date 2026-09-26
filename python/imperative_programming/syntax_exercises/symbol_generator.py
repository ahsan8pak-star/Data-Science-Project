"""
Symbol generator - random strings for use as passwords or ids.

Chooses from a character pool and joins the picks, wrapping the input handling
in try/except so a non-numeric length is reported rather than raised. The
length is validated before any character is drawn.
"""

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


