import math


def euclidean_distance(point1, point2):
    """
    Calculate the Euclidean distance between two points in n-dimensional space.

    Parameters:
    point1 (tuple or list): Coordinates of the first point.
    point2 (tuple or list): Coordinates of the second point.

    Returns:
    float: The Euclidean distance between the two points.
    """
    if len(point1) != len(point2):
        raise ValueError("Points must have the same number of dimensions / axes.")

    squared_diff_sum = sum((a - b) ** 2 for a, b in zip(point1, point2))
    return squared_diff_sum ** 0.5


def get_float_input(prompt):
    user_input = input(prompt)

    if user_input.strip() == "":
        return None

    try:
        return float(user_input)

    except ValueError:
        print("Invalid Input. Numbers Only.")
        return None


def get_point_coordinates(dimensions, point_name):
    coordinates = []

    for index in range(1, dimensions + 1):
        value = get_float_input(f"Enter coordinate {index} for {point_name}: ")

        if value is None:
            return None

        coordinates.append(value)

    return tuple(coordinates)


def get_dimensions():
    while True:
        raw_choice = input("How many dimensions? Press Enter for 2D default: ").strip()

        if raw_choice == "":
            return 2

        try:
            dimensions = int(raw_choice)

        except ValueError:
            print("Invalid input. Please enter a whole number.")
            continue

        if dimensions <= 0:
            print("Error: Please enter a positive number of dimensions.")
            continue

        return dimensions


def calculate(dimensions=None):
    if dimensions is None:
        dimensions = get_dimensions()

    point1 = get_point_coordinates(dimensions, "point 1")
    if point1 is None:
        return

    point2 = get_point_coordinates(dimensions, "point 2")
    if point2 is None:
        return

    if len(point1) != len(point2):
        print("Error: Both points must have the same number of dimensions.")
        return

    distance = euclidean_distance(point1, point2)
    print(f"Euclidean Distance: {distance:.2f}")


if __name__ == "__main__":
    calculate()

