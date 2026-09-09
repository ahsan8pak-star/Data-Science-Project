"""
Generator = Function that behaves like an iterator (it can be used in a for loop)

Pauses a function, returns a value, then resumes
Uses yield instead of return

Iterate without loading everything into memory (e.g. reading large files)

return -> Pouring bucket = Always empties the function and returns a value
yield -> Drip faucet = Can be paused and resumed
"""

# -----------------
# --- EXAMPLE 1 ---
# ----------------- 

import time

def count_to(n):
    count = 1
    start_time = time.time()  # Track start time when generator execution begins

    while count <= n:
        yield count  # Pause here and return the current value
        count += 1
        time.sleep(1)  # Simulate a delay (e.g., waiting for a resource) for a realistic example

    # Calculate execution time after loop completes
    execution_time = time.time() - start_time

    print("\nFinished counting to", n)

    if execution_time < 1:
        print("Execution time is negligible (less than a second).")

    elif execution_time < 60:
        print(f"Took {execution_time:.2f} seconds to count to {n}")

    elif execution_time >= 60:
        minutes = int(execution_time // 60)
        seconds = execution_time % 60
        print(f"Took {execution_time:.2f} seconds, which is {minutes} minutes and {seconds:.2f} seconds to count to {n}")

    elif execution_time >= 3600:
        hours = int(execution_time // 3600)
        minutes = int((execution_time % 3600) // 60)
        seconds = execution_time % 60
        print(f"Took {execution_time:.2f} seconds, which is {minutes} minutes and {seconds:.2f} seconds, which is also {hours} hours, {minutes} minutes and {seconds:.2f} seconds to count to {n}")


if __name__ == "__main__":
    try:
        number = int(input("Enter a number to count up to: "))
        for n in count_to(number):
            print(n)

    except KeyboardInterrupt:
        print("\nGenerator process interrupted by user.")

# -----------------
# --- EXAMPLE 2 ---
# ----------------- 

def read_file(file_path):
    with open(file_path, "r", encoding = "utf-8") as file:
        for line in file:
            yield line.strip()


file_path = r"C:\Users\A.I.M\C.S\Data-Science-Project\python\imperative_programming\syntax_fundamentals\\"
file_name = "activity_log.txt"
file_directory = file_path + file_name

for line in read_file(file_directory):
    print(line)

# Note: Ensure activity_log.txt exists at path before iterating


"""
Generator Expression = Similar to a list comprehension but uses () instead of []

Creates a generator (iterator) that yields values one at a time
No need to define a function or use yield
Less flexible than a gen func and not reusable

gen object = (expression for value in iterable if condition)
"""

# -----------------
# --- EXAMPLE 1 ---
# ----------------- 

number = int(input("Enter a number to count up to: "))

counter = (count for count in range(1, number + 1))

for n in counter:
   print(n)
   time.sleep(1) # Check Comment on Line 20

# -----------------
# --- EXAMPLE 2 ---
# ----------------- 

file_path = r"C:\Users\A.I.M\C.S\Data-Science-Project\python\imperative_programming\syntax_fundamentals\\"
file_name = "aim.txt"
file_directory = file_path + file_name

with open(file_directory) as file:
   lines = (line.strip() for line in file)

   for line in lines:
       print(line)

# -----------------
# --- EXAMPLE 3 ---
# ----------------- 

number = int(input("Enter a number to square up to: "))

even_squares = (x ** 2 for x in range(1, number + 1) if x % 2 == 0)

for square in even_squares:
   print(square)

