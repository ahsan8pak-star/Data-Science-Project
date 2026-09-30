""" TXT File Example """

def greet(name):
    return f"{name}"

message = greet("A.I.M")
file_path = "aim.txt"  # Relative to cwd for pytest to run_script(cwd = tmp_path)

with open(file_path, "w", encoding = "utf-8") as file:
    file.write(message)


""" Another Example for Writing TXT Files """

txt = "T.X.T"
file_path = "output.txt"

try:
    with open(file_path, "x", encoding = "utf-8") as file:
        file.write(txt)
    print(f"\n.txt file ['{file_path}'] has been created successfully!")

except FileExistsError:
    print(f"\nFile '{file_path}' already exists!\nNo need to overwrite.")


""" TXT File Appending Activity Log Example """

from datetime import datetime

current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
log_entry = f"[{current_time}] System Check Completed by User: 'A.I.M'\n"
file_path = "activity_log.txt"

try:
    with open(file_path, "a", encoding = "utf-8") as file:
        file.write(log_entry)
    print(f"\nLog entry successfully appended to ['{file_path}'].")

except PermissionError:
    print(f"\nError: Insufficient permissions to write to '{file_path}'.")


""" JSON File Example """

import json

employee = {
    "name": "Ahsan",
    "age": 21,
    "job": "Tutor"
}

file_path = "output.json"

try:
    with open(file_path, "x", encoding = "utf-8") as file:
        json.dump(employee, file, indent = 4) # Indentation of 4 spaces for json formatting i.e. 2 <TAB> spaces
    print(f"\n.json file ['{file_path}'] has been created successfully!")

except FileExistsError:
    print(f"\nFile '{file_path}' already exists!\nNo need to overwrite.")


""" CSV File Example """

import csv

employees = [
    ["Name", "Age", "Job"],
    ["Ahsan", 21, "Tutor"],
    ["Hamza", 20, "Manager"],
    ["Yayha", 19, "Baker"]
]

file_path = "output.csv"

try:
    with open(file_path, "x", newline="", encoding = "utf-8") as file:
        writer = csv.writer(file)

        for row in employees:
            writer.writerow(row)
    print(f"\n.csv file ['{file_path}'] was created successfully!")

except FileExistsError:
    print(f"\nFile '{file_path}' already exists!\nNo need to overwrite.")

