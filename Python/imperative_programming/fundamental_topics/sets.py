""" Set Methods """ 

fruits = {'apple', 'orange', 'banana', 'grapes', 'pineapple', 'plum'} 
vegetables = ('tomato', 'potato', 'cabbage', 'onion', 'carrot')

# Unordered (NOT in Order), Immutable (can't be Changed) and no Duplications (no same items repeated) 

# Can Add and Remove items in sets 

print(fruits) # prints out a RANDOM ORDER of items under set name 'fruits'

print(dir(fruits)) # Show Different Functions and Attributes of Sets

print(help(fruits)) # Help Guide of all the Set Methods

print(len(fruits)) # Number of items under set 'fruits'

print('coconut' in fruits) # Result: False -> Reason: word not found within this set

print('Apple' in fruits) # Case-sensitive check -> Result: False

fruits.add('coconut') # Adds 'coconut' to the set (item into a list)

fruits.remove('plum') # Removes 'plum' from the set

print(fruits.pop()) # Removes an arbitrary element

fruits.update(vegetables) # Updates (Similar to Add but uses an entire list instead) the list 'vegetables' 

fruits.clear() # Clears all items under the set 'fruits' -> Result: set()

del vegetables # Deletes the list 'vegetables' i.e. removes completely of all the structure not only the items


""" Set <-> List """

vegetables = set(vegetables)
print(vegetables)

fruits= list(fruits)
print(fruits)


""" Joining Sets via Unions """

set1 = {'item1', 'item2', 'item3', 'item4'}
set2 = {'item5', 'item6', 'item7', 'item8'}
set3 = set1.union(set2) # Alternative: set3 = set1 | set2


""" Updating Sets """

st1 = {'item1', 'item2', 'item3', 'item4'}
st2 = {'item5', 'item6', 'item7', 'item8'}
st1.update(st2) # st2 contents are added to st1


""" Finding Intersections """

square_numbers = {1, 4, 9, 16, 25, 36, 49, 64, 81, 100}
cube_numbers = {1, 8, 27, 64, 125, 216, 343, 512, 729, 1000}

common_numbers = square_numbers.intersection(cube_numbers) # {1, 64}
print(common_numbers)
# Alternative: common_numbers = square_numbers & cube_numbers


""" Confirming Subset and Super Set """

whole_numbers = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
even_numbers = {0, 2, 4, 6, 8, 10}

print(even_numbers.issubset(whole_numbers)) # True
print(whole_numbers.issuperset(even_numbers)) # True
print(whole_numbers.issubset(even_numbers)) # False


""" Difference between 2 Sets """

python = {'p', 'y', 't', 'h', 'o', 'n'}
dragon = {'d', 'r', 'a', 'g', 'o', 'n'}

# Returns items in python but not in dragon
print(python.difference(dragon)) # {'p', 'y', 't', 'h'}
print(python - dragon) # Alternative syntax

# Returns items in dragon but not in python
print(dragon.difference(python)) # {'d', 'r', 'a', 'g'}


""" Finding Symmetric Difference """

# Returns items in either set, but NOT in both
print(python.symmetric_difference(dragon)) # {'p', 'y', 't', 'h', 'd', 'r', 'a', 'g'}
print(python ^ dragon) # Alternative syntax


""" Checking Disjoint Sets """

odd_numbers = {1, 3, 5, 7, 9}
even_numbers = {0, 2, 4, 6, 8}

# Returns True if two sets share no common elements
print(even_numbers.isdisjoint(odd_numbers)) # True
print(python.isdisjoint(dragon)) # False (shares 'o' and 'n')

