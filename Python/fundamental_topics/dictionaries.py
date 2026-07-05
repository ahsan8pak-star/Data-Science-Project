coder = {
    "Name": "A.I.M",
    "Age": 21,
    "Is_Beginner": True
}

# Fiding exactly where in the dictionary is case- sensitive

# Example:
# print((coder["name"])) 

# Output:
# KeyError: name

print(coder["Name"]) # A.I.M
print(coder["Age"]) # 21
print((coder["Is_Beginner"])) # True

print(coder.get("Name")) # Outputs from what the dictionary specifies
print(coder.get("name")) # None - Prevents the program crashing

print(coder.get("Favourite_Team", "Arsenal")) # Add a new "word" / "definition" in the dictionary

coder["Age"] = 20 # replaces the age of 21 to now 20
print(coder["Age"]) # Now it outputs this rather than previous one being 21

