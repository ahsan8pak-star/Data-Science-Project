# 2D list of lists
num_pad = [[1, 2, 3],
           [4, 5, 6],
           [7, 8, 9],
           ["*", 0, "#"]]

# 2D list of tuples
num_pad = [(1, 2, 3),
           (4, 5, 6),
           (7, 8, 9),
           ("*", 0, "#")]

# 2D list of sets
num_pad = [{1, 2, 3},
           {4, 5, 6},
           {7, 8, 9},
           {"*", 0, "#"}]

# 2D tuple of lists
num_pad = ([1, 2, 3],
           [4, 5, 6],
           [7, 8, 9],
           ["*", 0, "#"])

# 2D tuple of tuples
num_pad = ((1, 2, 3),
           (4, 5, 6),
           (7, 8, 9),
           ("*", 0, "#"))

# 2D tuple of sets
num_pad = ({1, 2, 3},
           {4, 5, 6},
           {7, 8, 9},
           {"*", 0, "#"})

# 2D set of lists (NOT VALID) -> Reason: Lists are mutable, resulting its "identity" (hash) to be changed, breaking the logic of a set.
num_pad = {[1, 2, 3],
           [4, 5, 6],
           [7, 8, 9],
           ["*", 0, "#"]}

# 2D set of tuples
num_pad = {(1, 2, 3),
           (4, 5, 6),
           (7, 8, 9),
           ("*", 0, "#")}

# 2D set of sets (NOT VALID) -> Reason: Sets are also mutable, i.e. not hashable. You cannot place a standard set inside another set.
# Use forzensets() instead to make a set immutable / hashable
num_pad = {{1, 2, 3},
           {4, 5, 6},
           {7, 8, 9},
           {"*", 0, "#"}}

# an example of this VALID format
num_pad = {frozenset({1, 2, 3}),
           frozenset({4, 5, 6}),
           frozenset({7, 8, 9})}

# This for loop below will only take ONE TYPE of 'num_pad' being used
for row in num_pad:
    for num in row:
        print(num, end=" ") # Under EACH LIST being interated, ALL of its item will display on a single line i.e. goes to the next one after completion.
        # when n list is completed, n + 1 list is next to be iterated, etc.
    print() # This allows each new line to be printed after each iteration completed by each list

# Expected Result:
"""
1 2 3
4 5 6
7 8 9
* 0 #
"""

# Actual Result:
"""
1 2 3
4 5 6
7 8 9
* 0 #
"""

# Reason: for row in num_pad -> prints the list entirely in one row HORIZONTALLY
# for num in row -> prints the columns (VERTICAL LISTS)
# print(num, end=" ") -> Under EACH LIST being interated, ALL of its item will display on a single line i.e. goes to the next one after completion.
# end=" " -> this allows EACH ITEM to have a whitespace to the next item i.e. have a spare empty space next to one another
# print() -> This allows each new line to be printed after each iteration completed by each list ( \n funtion )