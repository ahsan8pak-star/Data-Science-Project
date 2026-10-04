import random


def generate_strings(num_doors=20):
    door_numbers = list(range(1, num_doors + 1))
    random.shuffle(door_numbers)
    start = "S"
    end = "E"
    result = []
    current_value = start
    for i in range(num_doors):
        next_value = door_numbers[i] if i < num_doors - 1 else end
        random_letter = random.choice(["M", "T", "E"])
        result.append(f"{current_value} {random_letter} {next_value}")
        current_value = door_numbers[i]

    return result


strings = generate_strings(10)
for s in strings:
    print(s)

