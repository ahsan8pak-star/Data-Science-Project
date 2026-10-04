# Declaration (Python uses type hints for optional static annotations)
var_name: list[int]  # or simple initialization: var_name = []

# Initialise Fixed-Size Array (with default values, e.g., zeros)
size = 5
var_name = [0] * size  # e.g., arr = [0] * 5

# Increment each element sequentially
def increment_array(numbers: list[int]) -> list[int]:
    # Pythonic approach (list comprehension)
    return [x + 1 for x in numbers]

    """
    Standard index loop equivalent:
    incremented_array = [0] * len(numbers)
    for i in range(len(numbers)):
        incremented_array[i] = numbers[i] + 1
    return incremented_array
    """

# Initialise Example
numbers = [1, 2, 3, 4, 5]
words = ["Imperative", "Programming", "is", "nice", "!"]

# Index-Based Loop Iteration
arr = [1, 2, 3, 4, 5]
for i in range(len(arr)):
    print(arr[i])

# For-Each (Direct Element) Loop Iteration
for element in arr:
    print(element)

