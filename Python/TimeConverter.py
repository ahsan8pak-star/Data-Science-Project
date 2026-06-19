def get_unit_info(time_choice):
    
    # Returns both the seconds multiplier and the text name of the unit.

    match time_choice: 
        case 1: # Base
            return 1, "Seconds" 
        
        case 2: # seconds to minutes
            return 60, "Minutes"
        
        case 3: # minutes to hours
            return 3600, "Hours" 
        
        case 4: # hours to days
            return 86400, "Days"
        
        case 5: # days to weeks
            return 604800, "Weeks" 
        
        case 6: # weeks to months
            return 2629746, "Months" 
        
        case 7: # months to years 
            return 31557600, "Years" 
        
        case 8: # years to decades
            return 315576000, "Decades" 
        
        case 9: # decades to centuries
            return 3155760000, "Centuries" 
        
        case 10: # centuries to milleniums
            return 31557600000, "Millenniums" 
        
        case _: # any incorrect value used and if it's outside of range 
            return None, "Invalid"

def display_menu(): # shows what each value in function get unit info stands for

    print("The Time Converter:")
    print("1. Seconds |   6. Months")
    print("2. Minutes |   7. Years")
    print("3. Hours   |   8. Decades")
    print("4. Days    |   9. Centuries")
    print("5. Weeks   |   10. Millenniums")


try:

    display_menu()
    
    # 1. Ask the user for their starting unit and target unit
    current_choice = input("Select your starting unit (1-10): ")
    next_choice = input("Select your target unit (1-10): ")
    
    # Unpack the multiplier and the name for both choices
    current_multiplier, current_name = get_unit_info(int(current_choice))
    next_multiplier, next_name = get_unit_info(int(next_choice))
    
    if current_multiplier is None or next_multiplier is None:
        print("Outside of Range.")

    else:

        # 2. Get the user's custom input amount
        amount = float(input(f"\nHow many {current_name} do you want to convert?: "))
        
        # 3. The Math (works going up or down the timeline)
        total_seconds = amount * current_multiplier
        final_answer = total_seconds / next_multiplier
        
        # 4. Print the final conversational sentence
        print(f"There are {final_answer} {next_name} in {amount} {current_name}.")

except ValueError:
    print("Numbers only.")

except KeyboardInterrupt:
    print("Program Stopped.")

