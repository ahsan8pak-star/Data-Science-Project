def greet(name): 
    return f"{name}"


message = greet("A.I.M")

file = open("AIM.txt", "w") # Opens a file in write mode.
file.write(message) # Writes the greeting message to the file.
file.close() # Closes the file.


""" Another Example for Writing TXT Files """

txt = "T.X.T"

file_dir = "C:/Users/A.I.M/C.S/Data-Science-Project/python/imperative_programming/syntax_fundamentals/"
file_name = "output.txt"
file_path = file_dir + file_name

try:
    with open(file_path, "x") as file: # Uses "x" (exclusive creation) so FileExistsError works correctly
        file.write(txt)
    print(f"\n.txt file ['{file_path}'] has been created successfully!")

except FileExistsError:
    print(f"\nFile '{file_name}' already exists!\nNo need to overwrite.")


""" JSON File Example """

import json

employee = {
    "name": "Ahsan",
    "age": 21,
    "job": "Tutor"
}

file_dir = "C:/Users/A.I.M/C.S/Data-Science-Project/python/imperative_programming/syntax_fundamentals/"
file_name = "output.json"
file_path = file_dir + file_name

try:
    with open(file_path, "x") as file:
        json.dump(employee, file, indent=4)
    print(f"\n.json file ['{file_path}'] has been created successfully!")

except FileExistsError:
    print(f"\nFile '{file_name}' already exists!\nNo need to overwrite.")


""" CSV File Example """

import csv

employees = [["Name", "Age", "Job"],
             ["Ahsan", 21, "Tutor"],
             ["Hamza", 20, "Manager"],
             ["Yayha", 19, "Baker"]]

file_dir = "C:/Users/A.I.M/C.S/Data-Science-Project/python/imperative_programming/syntax_fundamentals/"
file_name = "output.csv"
file_path = file_dir + file_name

try:
    with open(file_path, "x", newline="") as file:
        writer = csv.writer(file)

        for row in employees:
            writer.writerow(row)
    print(f"\n.csv file ['{file_path}'] was created successfully!")

except FileExistsError:
    print(f"\nFile '{file_name}' already exists!\nNo need to overwrite.")

