from euclidean_distance_calculator import get_dimensions, get_point_coordinates


def gradient(point1, point2):
    """Return the gradient m = (y2 - y1) / (x2 - x1)."""
    if len(point1) < 2 or len(point2) < 2:
        raise ValueError("Gradient requires at least two coordinates: x and y.")

    if len(point1) != len(point2):
        raise ValueError("Points must have the same number of dimensions.")

    x1, y1 = point1[0], point1[1]
    x2, y2 = point2[0], point2[1]

    if x2 == x1:
        raise ZeroDivisionError("Gradient is undefined for a vertical line (x2 - x1 = 0).")

    return (y2 - y1) / (x2 - x1)


def calculate(dimensions=None):
    if dimensions is None:
        dimensions = get_dimensions()

    if dimensions < 2:
        print("Gradient calculation requires at least 2 dimensions.")
        return

    point_a = get_point_coordinates(dimensions, "point a")
    if point_a is None:
        return

    point_b = get_point_coordinates(dimensions, "point b")
    if point_b is None:
        return

    direction = input("Is the line going from point a to point b? (y/n): ").strip().lower()

    if direction in ("", "y", "yes"):
        start_point, end_point = point_a, point_b
        start_name, end_name = "point a", "point b"
    else:
        start_point, end_point = point_b, point_a
        start_name, end_name = "point b", "point a"

    try:
        result = gradient(start_point, end_point)
    except ZeroDivisionError as exc:
        print(f"Error: {exc}")
        return
    except ValueError as exc:
        print(f"Error: {exc}")
        return

    print(f"Gradient from {start_name} to {end_name}: {result:.2f}")


if __name__ == "__main__":
    calculate()

