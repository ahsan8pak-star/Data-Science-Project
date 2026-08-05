# 1 1 1 1 1
# 2 1 2 4 8
# 3 1 3 9 27
# 4 1 4 16 64
# 5 1 5 25 125

# 1st column: 1, 2, 3, 4, 5 -> n + 1
# 2nd column: 1, 1, 1, 1, 1 -> n
# 3rd column: 1, 2, 3, 4, 5 -> n + 1
# 4th column: 1, 4, 9, 16, 25 -> n^2
# 5th column: 1, 8, 27, 64, 125 -> n^3

def display_number_matrix(n):
    """Display the matrix pattern for a non-negative integer n."""
    for value in range(1, 6): # loop through values 1 to 5 for the rows
        first_value = value + n - 1 # calculate the first value in the row based on n
        col1 = first_value # n + 1
        col2 = n # n
        col3 = first_value # n + 1
        col4 = n * value ** 2 # n^2
        col5 = n * value ** 3 # n^3
        print(f"{col1} {col2} {col3} {col4} {col5}") # display the values in a single line for each row


if __name__ == "__main__":
    try:
        n = int(input("Enter a whole number for n: "))

        if n < 0:
            raise ValueError("Number must be a positive integer i.e. n >= 0")

    except ValueError as e:
        print(f"Invalid input: {e}")

    else:
        display_number_matrix(n)

