# zip() = Combines multiple iterables (lists, tuples, sets, dict) into a single iterator of tuples.
# Makes managing multiple indices easier.

names = ["Ahsan", "Hamza", "Yahya"]
ages = [21, 20, 19]
jobs = ["Tutor", "Manager", "Baker"]

data = zip(names, ages, jobs) # automatically converts any items arranged into Tuples unless specified in front
# e.g. list(zip(names, ages, jobs))

for name, age, job in data:
    print(f"{name} is a {age} year old {job}")

