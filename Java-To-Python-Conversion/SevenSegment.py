def ssd(d, n):
    """Returns the specific string segment for digit 'd' on line number 'n'."""

    match (d * 10) + n:
        case 1 | 5 | 21 | 23 | 25 | 31 | 33 | 35 | 43 | 51 | 53 | 55 | 61 | 63 | 65 | 71 | 81 | 83 | 85 | 91 | 93 | 95:
            return " -- "
        
        case 24 | 52 | 62:
            return "|   "
            
        case 12 | 14 | 22 | 32 | 34 | 44 | 54 | 72 | 74 | 94:
            return "   |"
            
        case 2 | 4 | 42 | 64 | 82 | 84 | 92:
            return "|  |"
            
        case _:
            return "    "

def display(n): # Essential for 'def ssd(d, n)' to be outputted after 'n' input passes through

    """Iterates through 5 lines, building the ASCII art for the number."""
    if n == 0:
        for line in range(1, 6):
            print(ssd(0, line))
        return

    # Pythonic shortcut: convert the number to a string to easily loop through its digits
    str_n = str(n)
    
    # Loop through the 5 lines of the 7-segment display in a nested format
    for line in range(1, 6): # 6 is exclusive
        row_parts = [] # empty list -> initialiser

        for char in str_n:
            digit = int(char)
            row_parts.append(ssd(digit, line))
            
        # Join the segments for this line with a space and print
        print(" ".join(row_parts))

if __name__ == "__main__":

    try:
        num = int(input("Enter a number to display: "))

        if num < 0:
            num = 0

        display(num)

    except ValueError:
        print("Integers Only.")

