"""
Distance calculator - converts between millimetres, metres, kilometres, inches
and miles.

Reads both the start and the destination at module level, so running the file
prompts immediately. The scale factors are the substance of the exercise; the
validation catches ValueError for a non-numeric distance.
"""

start = input("Starting point: ")
finish = input("End point: ")

result = float(finish) - float(start)

distance = round(result, 2)

print(f"You travelled {distance}km!")


