"""
itertools - efficient building blocks for working with iterators.

Provides infinite counters, chained iterables, repeated values, and
combinatorics. Everything here is lazy and iterator-based, so it composes into
pipelines without building intermediate lists.
"""

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

# accumulate() yields a running total after each element
running = list(itertools.accumulate([1, 2, 3, 4]))

# batched() groups a stream into fixed-size tuples
batches = list(itertools.batched([1, 2, 3, 4, 5, 6], 2))

# combinations() picks ordered tuples without repetition
combos = list(itertools.combinations(["A", "B", "C"], 2))

# combinations_with_replacement() allows the SAME value twice
combos_rep = list(itertools.combinations_with_replacement(["A", "B", "C"], 2))

# compress() keeps only the items whose selector value is True
selected = list(itertools.compress("ABCD", [1, 0, 1, 1]))

# dropwhile() drops the leading items while the condition holds
after_drop = list(itertools.dropwhile(lambda x: x < 3, [1, 2, 3, 4, 1]))

# filterfalse() keeps the items for which the predicate is False
rejected = list(itertools.filterfalse(lambda x: x % 2 == 0, [1, 2, 3, 4]))

# groupby() groups consecutive equal values into (key, group) pairs
grouped = {k: list(g) for k, g in itertools.groupby("AABBCCDD")}

# pairwise() yields each overlapping pair of consecutive items
pairs = list(itertools.pairwise([1, 2, 3, 4]))

# permutations() yields every ordered arrangement of length r
perms = list(itertools.permutations(["A", "B", "C"], 2))

# starmap() unpacks each tuple onto the function's arguments
summed = list(itertools.starmap(lambda a, b: a + b, [(1, 2), (3, 4)]))

# takewhile() takes items only while the condition holds
until_stop = list(itertools.takewhile(lambda x: x < 3, [1, 2, 3, 4, 1]))

# tee() duplicates one iterator into several independent ones
clone_a, clone_b = itertools.tee([1, 2, 3], 2)

# zip_longest() zips the shorter list by padding with fillvalue
zipped_padded = list(itertools.zip_longest([1, 2], ["a", "b", "c"], fillvalue="?"))

print("chain:", combined)
print("count first 5:", natural)
print("cycle sample:", colours)
print("repeat:", repeated)
print("product:", outcomes)
print("accumulate:", running)
print("batched:", batches)
print("combinations:", combos)
print("combinations_with_replacement:", combos_rep)
print("compress:", selected)
print("dropwhile:", after_drop)
print("filterfalse:", rejected)
print("groupby:", grouped)
print("pairwise:", pairs)
print("permutations:", perms)
print("starmap:", summed)
print("takewhile:", until_stop)
print("tee clone_a:", list(clone_a))
print("tee clone_b:", list(clone_b))
print("zip_longest:", zipped_padded)


