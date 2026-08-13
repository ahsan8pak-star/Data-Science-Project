def times_tables():
    # Ask the user for the number of columns (how long each times table should be)
    columns = int(input("Enter the number of columns you want the times table to be extended: "))
    
    # Ask the user for the number of tables (up to which times table to print)
    tables = int(input("Enter how many times you want to do this i.e. from up to which times tables: "))
    
    # The outer loop controls which times table we are on (e.g., 0, 1, 2...)
    for i in range(0, tables + 1):
        print(f"\n{i} Times Table(s)")
        
        # The inner loop controls the multiplication up to the requested 'columns'
        for j in range(0, columns + 1):
            print(f"{i} x {j} = {i * j}") # 1 x 1 = 1 ... ->  ... 12 x 12 = 144

if __name__ == "__main__":
    times_tables()

