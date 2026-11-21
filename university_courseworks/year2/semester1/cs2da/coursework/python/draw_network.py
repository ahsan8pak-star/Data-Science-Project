"""
Generate a GraphViz .dot file from a road-network adjacency matrix of distances (Task 3).
"""

import math

LOCATIONS = "ABCDEF"


def generate_dot(distances):
    """
    Return the .dot source for the network graph expressed by the adjacency matrix of distances.

    distances: list of n rows, each a list of n floats (NaN marks a missing road).
    """
    n = len(distances)
    lines = []
    lines.append("digraph Network {")
    lines.append("    rankdir = TB;")
    lines.append("    node [shape = circle, fontname = \"Helvetica\"];")
    lines.append("    edge [fontname = \"Helvetica\"];")
    lines.append("")
    for i in range(n):
        lines.append(f"    {LOCATIONS[i]} [label = \"{LOCATIONS[i]}\"];")
    lines.append("")
    for i in range(n):
        for j in range(n):
            if i == j or math.isnan(distances[i][j]):
                continue
            lines.append(f'    {LOCATIONS[i]} -> {LOCATIONS[j]} [label = "{int(distances[i][j])}"];')
    lines.append("}")

    return "\n".join(lines) + "\n"


def main():
    # Personalised network for student number 34001219.
    distances = [
        [0.0, 15.0, float("nan"), 9.0, 42.0, 10.0],
        [15.0, 0.0, 46.0, 37.0, float("nan"), float("nan")],
        [26.0, float("nan"), 0.0, 24.0, float("nan"), 32.0],
        [9.0, 37.0, float("nan"), 0.0, 38.0, 84.0],
        [42.0, float("nan"), 28.0, 38.0, 0.0, float("nan")],
        [10.0, float("nan"), float("nan"), 84.0, 26.0, 0.0],
    ]
    print(generate_dot(distances), end="")


if __name__ == "__main__":
    main()

