from times_tables import times_tables

def square_number():
    # Only ask for a single input to determine the range of square numbers
    limit = int(input("Enter the maximum number for your square times tables: "))
    
    print("\nSquare Times Tables:")
    
    # A single loop is all that is needed to multiply 'i' by itself
    for i in range(0, limit + 1):
        print(f"{i} x {i} = {i * i}")

if __name__ == "__main__":
    square_number()

