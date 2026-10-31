"""
network.py -- CS2PP Coursework 1, Task 1: Structuring and Analysing Network Data.

Task 1 map
----------
1.1  file_to_edge_list: reads the citation TSV and returns a list of (int, int) edges.
1.2  edge_to_neighbour_list_my: converts an edge list into a neighbour list dict.
1.3  calculate_degree_statistics: returns the maximum, minimum, average and most common degree.
1.4  calculate_clustering_coefficient: returns the clustering coefficient as a float for a node.

Note: candidate conversion functions live in candidates.py; subgraph returns the
node, its linked neighbours and the edges between them.
"""

import csv

# NetworkDataError: base exception raised when network data fails validation.
class NetworkDataError(Exception):
    """Raised when network data fails validation."""

# NodeNotFoundError: raised when a requested node is not in the network.
class NodeNotFoundError(NetworkDataError):
    """Raised when a requested node is not in the network."""

# file_to_edge_list: reads the citation TSV and returns a list of (int, int) edges.
def file_to_edge_list(*, file_path):
    """Return the citation file contents as a list of (int, int) edges."""

    if not isinstance(file_path, str) or not file_path.strip():
        raise NetworkDataError("'file_path' must be a non-empty string.")

    try:
        with open(file_path, 'r', encoding = 'utf-8') as tsvfile:
            reader = csv.reader(tsvfile, delimiter = '\t')
            edges = []

            for row in reader:
                if not row:
                    continue

                if len(row) != 2:
                    raise NetworkDataError(f"Expected 2 columns.\nGot {len(row)}: {row}")

                try:
                    edges.append((int(row[0]), int(row[1]))) # two rows only

                except ValueError as e:
                    raise NetworkDataError(f"Non-integer node id in row: {row}") from e
            return edges

    except FileNotFoundError as e:
        raise FileNotFoundError(f"Citation file not found: {file_path}") from e

    except PermissionError as e:
        raise PermissionError(f"Unable to read citation file: {file_path}") from e


# edge_to_neighbour_list_my: converts an edge list into a neighbour list dict.
def edge_to_neighbour_list_my(edges, /):
    """Return {node: [distinct sorted neighbours]} from an edge list."""

    neighbours = {}

    for left, right in edges:
        neighbours.setdefault(left, set()).add(right)
        neighbours.setdefault(right, set()).add(left)
    return {node: sorted(neighbour) for node, neighbour in neighbours.items()}


# inspect_node: returns the edges of a node from an edge list, or linked nodes from a neighbour list.
def inspect_node(*, network, node):
    """Return edges containing node (edge list) or its neighbours (neighbour list)."""

    if not isinstance(node, int):
        raise TypeError("node must be an integer.")

    if isinstance(network, dict):
        if node not in network:
            raise NodeNotFoundError(f"Node {node} not found in network.")
        return list(network.get(node, []))
    return [edge for edge in network if node in edge]


# calculate_degree_statistics: returns the maximum, minimum, average and most common degree.
def calculate_degree_statistics(network):
    """Return (maximum, minimum, average, most_common) degree values."""

    if not isinstance(network, dict) or not network:
        raise NetworkDataError("network must be a non-empty neighbour dict.")

    degrees = [len(neighbour) + (1 if node in neighbour else 0) for node, neighbour in network.items()]
    maximum = max(degrees)
    minimum = min(degrees)
    average = (lambda values: float(sum(values)) / len(values))(degrees)
    most_common = max(set(degrees), key = lambda d: degrees.count(d))

    return maximum, minimum, average, most_common


# calculate_clustering_coefficient: returns the clustering coefficient as a float for a node.
def calculate_clustering_coefficient(*, network, node):
    """Return the clustering coefficient of node as a single float."""

    if not isinstance(network, dict):
        raise TypeError("network must be a neighbour-list dict.")

    if not isinstance(node, int):
        raise TypeError("node must be an integer.")

    if node not in network:
        raise NodeNotFoundError(f"Node {node} not found in network.")

    neighbours = [n for n in network.get(node, []) if n != node]
    k = len(neighbours)

    if k < 2:
        return 0.0

    edges_among = sum(
        1
        for i in range(len(neighbours))
        for j in range(i + 1, len(neighbours))
        if neighbours[j] in network.get(neighbours[i], ())
    )

    try:
        return (2 * edges_among) / (k * (k - 1))

    except ZeroDivisionError:
        return 0.0


# subgraph: returns the node, its linked neighbours and the edges between them.
def subgraph(*, network, node):
    """Return the node, its linked neighbours, and the edges between them."""

    if not isinstance(network, dict) :
        raise TypeError("network must be a neighbour-list dict.")

    if not isinstance(node, int) :
        raise TypeError("node must be an integer.")

    if node not in network :
        raise NodeNotFoundError(f"Node {node} not found in network.")

    neighbours = sorted({n for n in network[node] if n != node})
    nodes = [node] + neighbours

    edges = []

    for neighbour in nodes:
        for linked in nodes:
            if neighbour < linked and linked in network.get(neighbour, ()):
                edges.append((neighbour, linked))

    return nodes, edges

