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

if __name__ == "__main__":
    try:     
        # Example usage
        point_a = (2, 3)
        point_b = (10, 8)
        distance = euclidean_distance(point_a, point_b)
        print(f"The Euclidean distance between {point_a} and {point_b} is {distance:.2f}")

        # TUI Display
        print("\n --- Euclidean Distance Calculator ---")

        # Custom input from the user
        user_input1 = input("Enter the coordinates of the first point (comma-separated): ")
        user_input2 = input("Enter the coordinates of the second point (comma-separated): ")

        point1 = tuple(map(float, user_input1.split(',')))
        point2 = tuple(map(float, user_input2.split(',')))

        distance = euclidean_distance(point1, point2)
        print(f"The Euclidean distance between {point1} and {point2} is {distance:.2f}")

    except ValueError as e:
        print(f"Error: {e}")

