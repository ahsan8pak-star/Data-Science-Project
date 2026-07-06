# Dictionary =  a collection of {key:value} pairs
# Ordered and Changeable, but No Duplicates
"""
Dictionary = {

    key: value

}
"""

coder = {
    "Name": "A.I.M",
    "Age": 21,
    "Is_Beginner": True
}

print(dir(coder)) # Shows all the methods available for the dictionary under a single line
print(help(coder)) # Shows all the methods available as a help guide

# Fiding exactly where in the dictionary is case - sensitive

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

coder["Age"] = 20 # replaces the age of 21 to now 20 -> coder.update({"Age": 20})
print(coder["Age"]) # Now it outputs this rather than previous one being 21

print(coder.pop("Is_Beginner")) # Removes the key and value from the dictionary
print(coder) # Outputs the dictionary without the key and value of Is_Beginner

print(coder.popitem()) # Removes the last item in the dictionary

print(coder.clear()) # Clears the entire dictionary

print(coder.keys()) # Outputs all the keys in the dictionary (first column)
# Output: (['Name', 'Age', 'Is_Beginner'])

print(coder.values()) # Outputs all the values in the dictionary (second column)
# Output: (['A.I.M', 20, True])

print(coder.items()) # Shows all the items in the dictionary as a list -> [ {}, {}, {}... ]

""" Another Dictionary Example """

capitals = {"USA": "Washington D.C.",
            "India": "New Delhi",
            "China": "Beijing",
            "Russia": "Moscow"}

print(dir(capitals))
print(help(capitals))
print(capitals.get("Japan"))

if capitals.get("Russia"):
    print("Captial Exists!")
else:
    print("Non-Existant Capital!")

capitals.update({"Germany": "Berlin"}) 
# {"USA": "Washington D.C.", "India": "New Delhi", "China": "Beijing", "Russia": "Moscow", "Germany": "Berlin"}

capitals.update({"USA": "Detroit"}) 
# {"USA": "Detroit", "India": "New Delhi", "China": "Beijing", "Russia": "Moscow", "Germany": "Berlin"}

capitals.pop("China") 
# {"USA": "Detroit", "India": "New Delhi", "Russia": "Moscow", "Germany": "Berlin"}

capitals.popitem() 
# {"USA": "Detroit", "India": "New Delhi", "Russia": "Moscow"}

capitals.clear() 
# {}

keys = capitals.keys()
for key in capitals.keys():
    print(key)

# Output: 
"""
USA
India
China
Russia
"""

values = capitals.values()
for value in capitals.values():
    print(value)

# Output:  
"""
Washington D.C.
New Delhi
Beijing
Moscow
"""


items = capitals.items()
for key, value in capitals.items():
    print(f"{key}: {value}")

# Output:
"""
USA: Washington D.C.
India: New Delhi
China: Beijing
Russia: Moscow
"""