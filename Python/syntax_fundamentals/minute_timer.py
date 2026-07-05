import time

def countdown(total_seconds):

    # 'timer' decreases by 1 on every iteration
    for timer in range(total_seconds, 0, -1): 
    
        # Calculates both minutes and remaining seconds using the changing loop variable
        minutes = timer // 60 
        seconds = timer % 60
        print(f"{minutes:02}:{seconds:02}") # Pad the zeros (0s) within two (2) digits
        time.sleep(1) # main function -> every execution made for every second passed
    print("TIMES UP!") # for loop ends / completes

try:
    # Takes input as a string first to safely validate it
    minutes_input = input("Enter time in minute(s): ")
    seconds_input = input("Enter time in second(s): ")

    # Makes sure it contains only digits before proceeding
    if minutes_input.isdigit() and seconds_input.isdigit():
        minutes = int(minutes_input)
        seconds = int(seconds_input)
    
        if seconds >= 60:
            print("Can't be at least 60 seconds")
            print("Anything more than that will go to minutes.")
        else:
            combined_seconds = (minutes * 60) + seconds
            countdown(combined_seconds)
    else:
        print("Please enter a valid input.")
except ValueError:
    print("Minutes and Seconds is in the form of integers.")