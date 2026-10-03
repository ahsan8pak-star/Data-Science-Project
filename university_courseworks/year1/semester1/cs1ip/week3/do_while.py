i = 0

# Create an infinite loop to simulate the 'do' block
while True:
    # This block executes at least once
    print(i)
    i += 1
    
    # Evaluate the condition at the end; break if it is no longer met
    if not (i < 5):
        break

