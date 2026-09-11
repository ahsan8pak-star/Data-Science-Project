""" .txt file """

file_dir = "C:/Users/A.I.M/C.S/Data-Science-Project/python/imperative_programming/syntax_fundamentals/"
file_name = "input.txt"
file_path = file_dir + file_name

try:
    with open(file_path, "r") as file:
        content = file.read()
        print(content)

except FileNotFoundError:
    print("\nError: File Not Found.\nCheck Directory Path.")

except PermissionError:
    print("\nAdministrative / Authroised Users Only!")


""" .json file """

import json

file_dir = "C:/Users/A.I.M/C.S/Data-Science-Project/python/imperative_programming/syntax_fundamentals/"
file_name = "input.json"
file_path = file_dir + file_name

try:
    with open(file_path, "r") as file:
        content = json.load(file)
        print(content) # this line can access each key (e.g. print(content["gamertag"]))

except FileNotFoundError:
    print("\nError: File Not Found.\nCheck Directory Path.")

except PermissionError:
    print("\nAdministrative / Authroised Users Only!")


""" .csv file """

import csv
from datetime import datetime

file_dir = "C:/Users/A.I.M/C.S/Data-Science-Project/python/imperative_programming/syntax_fundamentals/"
file_name = "input.csv"
file_path = file_dir + file_name

try:
    with open(file_path, "r") as file:
        content = csv.reader(file)
        
        # Skip the header row
        header = next(content)

        for line in content:
            # Strip whitespace added by spaces after commas in the CSV
            row = [cell.strip() for cell in line]

            # Convert each column to its intended target type
            gamertag = str(row[0])
            gamerscore = int(row[1])
            is_online = row[2].lower() == "true"
            account_made = datetime.strptime(row[3], "%d/%m/%Y").date()

            print(f"\nTag: {gamertag} ({type(gamertag).__name__}) | "
                  f"Score: {gamerscore} ({type(gamerscore).__name__}) | "
                  f"Online: {is_online} ({type(is_online).__name__}) | "
                  f"Created: {account_made} ({type(account_made).__name__})\n")

except FileNotFoundError:
    print("\nError: File Not Found.\nCheck Directory Path.")

except PermissionError:
    print("\nAdministrative / Authorised Users Only!")

