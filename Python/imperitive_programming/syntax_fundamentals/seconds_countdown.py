import time

def countdown(total_seconds):

    # 'second' decreases by 1 on every iteration
    for second in range(total_seconds, 0, -1): 
    
        # Calculate remaining seconds using the changing loop variable
        seconds = second % 60
        print(f"{seconds:02}") # Pad the zeros (0s) within two (2) digits
        time.sleep(1) # main function -> every execution made for every second passed
    print("TIMES UP!") # for loop ends / completes

try:
    # Takes input as a string first to safely validate it
    user_input = input("Enter time in second(s): ")

    # Makes sure it contains only digits before proceeding
    if user_input.isdigit():
        seconds = int(user_input)
    
        if seconds >= 60:
            print("Can't be at least 60 seconds")
            print("This is not suitable for minutes.")
        else:
            countdown(seconds)
    else:
        print("Please enter a valid input.")
except ValueError:
    print("Seconds is in the form of integers.")

