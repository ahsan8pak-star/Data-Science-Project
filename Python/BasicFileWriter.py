def greet(name): 
    return f"{name}"


message = greet("A.I.M")
file = open("AIM.txt", "w") # Opens a file in write mode.
file.write(message) # Writes the greeting message to the file.
file.close() # Closes the file.