""" Set Methods """ 

fruits = {'apple', 'orange', 'banana', 'grapes', 'pineapple', 'plum'} 

# Unordered (NOT in Order), Immutable (can't be Changed) and no Duplications (no same items repeated) 

# Can Add and Remove items in sets 

print(fruits) # prints out a RANDOM ORDER of items under set name 'fruits'

print(dir(fruits)) # Show Different Functions and Attributes of Sets

print(help(fruits)) # Help Guide of all the Set Methods

print(len(fruits)) # Number of items under set 'fruits'

print('coconut' in fruits) # Result: False -> Reason: this word is not found within this set, letter by letter + Case - Sensitive as well

print('Apple' in fruits) # an example of case-sensitive statement -> Result: False

print(fruits.add('coconut')) # Adds 'coconut' to the set 

print(fruits.remove('plum')) # Removes 'plum' from the set

print(fruits.pop()) # Removes the first element -> Under a random list, it'll remove whatever comes first

print(fruits.clear()) # Clears all items under the set 'fruits' -> Result: set()