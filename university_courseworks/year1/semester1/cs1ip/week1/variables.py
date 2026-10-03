def main() -> None:
    # Variables and dynamic typing
    uni: str = "Reading"
    total_days: int = 275
    target_days: int = 360
    
    # Division and modulus arithmetic
    weeks: int = (target_days - total_days) // 7  # Explicit integer division
    days: int = (target_days - total_days) % 7
    
    # Formatted console output using f-strings
    print(f"The University of {uni} was founded in {1892}.")
    print(f"There are {weeks} weeks and {days} days until Christmas.")

if __name__ == "__main__":
    main()

