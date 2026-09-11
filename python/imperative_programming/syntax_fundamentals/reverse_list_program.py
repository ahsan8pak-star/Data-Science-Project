def reverse_list(arr):
    # Takes an array as a parameter and returns the reverse of the array.
    return arr[::-1]


if __name__ == "__main__":
    user_input = input("Enter your list: ")
    
    # Parse the input into a list, stripping any extra spaces
    items = [item.strip() for item in user_input.split(",")]
    
    # Validate that all items are of the same data type
    is_alpha = all(item.isalpha() for item in items)
    is_numeric = all(item.isnumeric() for item in items)
    
    if not (is_alpha or is_numeric):
        print("Error: All items must be the same data type / variable")

    else:
        if is_alpha:
            order_choice = input("Do you want this list to be ordered alphabetically? (y/n): ").strip().lower()

            if order_choice.lower().startswith("y"):
                items.sort()

        elif is_numeric:
            order_choice = input("Do you want this list to be ordered numerically? (y/n): ").strip().lower()

            # Convert string numbers to integers for accurate numerical manipulation
            items = [int(item) for item in items]
            
            if order_choice.lower().startswith("y"):
                items.sort()
        
        # Reverse the list using the requested function
        reversed_items = reverse_list(items)
        
        # Format the output to match the requested comma-separated string
        formatted_output = ", ".join(str(item) for item in reversed_items)
        print(f"Reverse List: {formatted_output}")

