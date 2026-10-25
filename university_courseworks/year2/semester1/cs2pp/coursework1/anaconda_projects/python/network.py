"""
network.py -- CS2PP Coursework 1, Task 1: Structuring and Analysing Network Data.

Supports the Task 1 prompts in CS2PP_CW1.ipynb. All components use only
the Python standard library.
"""

import csv
from dataclasses import dataclass


class NetworkDataError(Exception):
    """Raised when network data fails validation."""


class NodeNotFoundError(NetworkDataError):
    """Raised when a requested node is not in the network."""


def file_to_edge_list(*, file_path):
    """Return the citation file contents as a list of (int, int) edges."""
    if not isinstance(file_path, str) or not file_path.strip():
        raise NetworkDataError("file_path must be a non-empty string.")
    try:
        with open(file_path, 'r') as tsvfile:
            reader = csv.reader(tsvfile, delimiter='\t')
            edges = []
            for row in reader:
                if not row:
                    continue
                if len(row) != 2:
                    raise NetworkDataError(
                        f"Expected 2 columns, got {len(row)}: {row}"
                    )
                try:
                    edges.append((int(row[0]), int(row[1])))
                except ValueError as exc:
                    raise NetworkDataError(
                        f"Non-integer node id in row: {row}"
                    ) from exc
            return edges
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            f"Citation file not found: {file_path}"
        ) from exc
    except PermissionError as exc:
        raise PermissionError(
            f"Cannot read citation file: {file_path}"
        ) from exc


def edge_to_neighbour_list_my(edges, /):
    """Return {node: [distinct sorted neighbours]} from an edge list."""
    neighbours = {}
    for left, right in edges:
        neighbours.setdefault(left, set()).add(right)
        neighbours.setdefault(right, set()).add(left)
    return {node: sorted(nbrs) for node, nbrs in neighbours.items()}


def inspect_node(*, network, node):
    """Return edges containing node (edge list) or its neighbours (neighbour list)."""
    if not isinstance(node, int):
        raise TypeError("node must be an integer.")
    if isinstance(network, dict):
        if node not in network:
            raise NodeNotFoundError(f"Node {node} not found in network.")
        return list(network.get(node, []))
    return [edge for edge in network if node in edge]


def calculate_degree_statistics(network):
    """Return (maximum, minimum, average, most_common) degree values."""
    if not isinstance(network, dict) or not network:
        raise NetworkDataError("network must be a non-empty neighbour dict.")
    degrees = [len(nbrs) for nbrs in network.values()]
    maximum = max(degrees)
    minimum = min(degrees)
    average = sum(degrees) / len(degrees)
    most_common = max(set(degrees), key=lambda d: degrees.count(d))
    return maximum, minimum, average, most_common


def calculate_clustering_coefficient(*, network, node):
    """Return the clustering coefficient of node as a single float."""
    if not isinstance(network, dict):
        raise TypeError("network must be a neighbour-list dict.")
    if not isinstance(node, int):
        raise TypeError("node must be an integer.")
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


def edge_to_neighbour_list_a(edges, /):
    """Candidate A."""
    neighbours = {}
    for edge in edges:
        neighbours.setdefault(edge[0], []).append(edge[1])
        neighbours.setdefault(edge[1], []).append(edge[0])
    return neighbours


def edge_to_neighbour_list_b(edges, /):
    """Candidate B."""
    neighbours = {}
    for left, right in edges:
        neighbours.setdefault(left, []).append(right)
        neighbours.setdefault(right, [])
    return neighbours


def edge_to_neighbour_list_c(edges, /):
    """Candidate C."""
    nodes = {node for edge in edges for node in edge}
    return {
        node: [right if left == node else left
               for left, right in edges
               if node in (left, right)]
        for node in nodes
    }


def edge_to_neighbour_list_d(edges, /):
    """Candidate D."""
    if not edges:
        return {}

    largest_node = max(max(edge) for edge in edges)
    neighbours = {node: [] for node in range(largest_node + 1)}
    for left, right in edges:
        neighbours[left].append(right)
        neighbours[right].append(left)
    return neighbours


def edge_to_neighbour_list_e(edges, /):
    """Candidate E."""
    nodes = {node for edge in edges for node in edge}
    neighbours = dict.fromkeys(nodes, [])
    for left, right in edges:
        neighbours[left].append(right)
        neighbours[right].append(left)
    return neighbours


def edge_to_neighbour_list_f(edges, /):
    """Candidate F."""
    neighbours = {}
    for left, right in edges:
        neighbours[left] = neighbours.get(left, []) + [right]
        neighbours[right] = neighbours.get(right, []) + [left]
    return neighbours


def edge_to_neighbour_list_g(edges, /):
    """Candidate G."""
    neighbours = {}
    for val in edges:
        neighbours[val[0]] = set()
        neighbours[val[1]] = set()

    for val in edges:
        neighbours[val[0]].add(val[1])
        neighbours[val[1]].add(val[0])
    return neighbours


def edge_to_neighbour_list_h(edges, /):
    """Candidate H."""
    neighbours = {}
    for x, y in edges:
        if isinstance(neighbours.get(x), set):
            neighbours[x].add(y)
        else:
            neighbours[x] = {y}

        if isinstance(neighbours.get(y), set):
            neighbours[y].add(x)
        else:
            neighbours[y] = {x}
    return neighbours


@dataclass(frozen=True, slots=True)
class _ValidatedEdge:
    left: int
    right: int

    def __post_init__(self):
        if type(self.left) is not int or type(self.right) is not int:
            raise TypeError("Node identifiers must be integers")
        if self.left == self.right:
            raise ValueError("Self-loops are not permitted")


class _UndirectedAdjacencyBuilder:
    def __init__(self):
        self._adjacency = {}

    def ingest(self, edge):
        self._adjacency.setdefault(edge.left, set()).add(edge.right)
        self._adjacency.setdefault(edge.right, set()).add(edge.left)

    def export(self):
        return {
            node: sorted(connected_nodes)
            for node, connected_nodes in self._adjacency.items()
        }


def edge_to_neighbour_list_i(edges, /):
    """Candidate I."""
    builder = _UndirectedAdjacencyBuilder()
    for pair in edges:
        builder.ingest(_ValidatedEdge(*pair))
    return builder.export()

