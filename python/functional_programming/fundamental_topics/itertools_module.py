# itertools = A module of efficient building blocks for working with iterators.
# Provides infinite counters, chained iterables, repeated values, and combinatorics.


import itertools

# chain() joins multiple iterables together
combined = list(itertools.chain([1, 2], [3, 4], [5, 6]))

# count() counts forever (take a slice with islice())
natural = list(itertools.islice(itertools.count(1), 5))

# cycle() repeats an iterable over and over
colours = list(itertools.islice(itertools.cycle(["red", "green", "blue"]), 6))

# repeat() repeats a single value a fixed number of times
repeated = list(itertools.repeat("A", 4))

# product() pairs every item with every item
outcomes = list(itertools.product([1, 2], ["head", "tail"]))

print("chain:", combined)
print("count first 5:", natural)
print("cycle sample:", colours)
print("repeat:", repeated)
print("product:", outcomes)