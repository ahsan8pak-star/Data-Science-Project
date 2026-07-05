import time

def countdown(total_seconds):
    # 'timer' decreases by 1 on every iteration starting from the entire seconds pool
    for timer in range(total_seconds, 0, -1): 

        hours = timer // 3600 # 1 hour = 60 minutes = 3600 seconds

        minutes = (timer % 3600) // 60 # 1 minute = 60 seconds
        
        seconds = timer % 60 # remaining seconds
        
        # Print the full digital clock display zero-padding to two digits each
        print(f"{hours:02}:{minutes:02}:{seconds:02}") 
        time.sleep(1) 
        
    print("TIMES UP!") 

try:
    # Takes all three components as strings for safe verification
    hours_input = input("Enter time in hour(s): ")
    minutes_input = input("Enter time in minute(s): ")
    seconds_input = input("Enter time in second(s): ")

    # Ensure every single input contains only digits before converting
    if hours_input.isdigit() and minutes_input.isdigit() and seconds_input.isdigit():
        hours = int(hours_input)
        minutes = int(minutes_input)
        seconds = int(seconds_input)
    
        # Bound checks to keep minutes and seconds within real clock limits
        if minutes >= 60 or seconds >= 60:
            print("Minutes and seconds must be less than 60.")
            print("Values of 60 or more should carry over to the next unit up.")
       
        elif hours == 0 and minutes == 0 and seconds == 0:
            print("Enter a valid time.")
       
        else:
            # Calculate the sum of combined seconds
            combined_seconds = (hours * 3600) + (minutes * 60) + seconds
            countdown(combined_seconds)
    else:
        print("Please enter a valid input.")

except ValueError:
    print("All inputs must be in the form of whole integers.")