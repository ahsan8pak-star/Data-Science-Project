"""
candidates.py -- CS2PP Coursework 1, Task 1: Preformulated candidate conversion functions.

Task 1 map
----------
- edge_to_neighbour_list_a ... edge_to_neighbour_list_h: preformulated candidates under test in Task 1.5.
- _ValidatedEdge / _UndirectedAdjacencyBuilder / edge_to_neighbour_list_i: helper candidates.

Note: the custom converter under test is edge_to_neighbour_list_my in network.py.
"""

from dataclasses import dataclass


# edge_to_neighbour_list_a: candidate - converts an edge list into neighbour lists (append style)
def edge_to_neighbour_list_a(edges, /):
    """Candidate A."""
    neighbours = {}

    for edge in edges:
        neighbours.setdefault(edge[0], []).append(edge[1])
        neighbours.setdefault(edge[1], []).append(edge[0])
    return neighbours


# edge_to_neighbour_list_b: candidate - converts an edge list into neighbour lists (one-way style)
def edge_to_neighbour_list_b(edges, /):
    """Candidate B."""
    neighbours = {}

    for left, right in edges:
        neighbours.setdefault(left, []).append(right)
        neighbours.setdefault(right, [])
    return neighbours


# edge_to_neighbour_list_c: candidate - converts an edge list into neighbour sets (set style)
def edge_to_neighbour_list_c(edges, /):
    """Candidate C."""
    nodes = {node for edge in edges for node in edge}

    return {
        node: [right if left == node else left
               for left, right in edges
               if node in (left, right)]
        for node in nodes
    }


# edge_to_neighbour_list_d: candidate - converts an edge list into neighbour lists (preallocation style)
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


# edge_to_neighbour_list_e: candidate - converts an edge list into neighbour lists (node-set style)
def edge_to_neighbour_list_e(edges, /):
    """Candidate E."""

    nodes = {node for edge in edges for node in edge}
    neighbours = dict.fromkeys(nodes, [])

    for left, right in edges:
        neighbours[left].append(right)
        neighbours[right].append(left)
    return neighbours


# edge_to_neighbour_list_f: candidate - converts an edge list into neighbour lists (concatenation style)
def edge_to_neighbour_list_f(edges, /):
    """Candidate F."""
    neighbours = {}

    for left, right in edges:
        neighbours[left] = neighbours.get(left, []) + [right]
        neighbours[right] = neighbours.get(right, []) + [left]
    return neighbours


# edge_to_neighbour_list_g: candidate - converts an edge list into neighbour sets (reset-then-fill style)
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


# edge_to_neighbour_list_h: candidate - converts an edge list into neighbour sets (isinstance style)
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


# _ValidatedEdge: validated (left, right) pair that rejects bad types and self-loops
@dataclass(frozen=True, slots=True)
class _ValidatedEdge:
    left: int
    right: int

    def __post_init__(self):
        # raise TypeError when node identifiers are not integers
        if type(self.left) is not int or type(self.right) is not int:
            raise TypeError("Node identifiers must be integers")

        # raise ValueError when a self-loop edge is supplied
        if self.left == self.right:
            raise ValueError("Self-loops are not permitted")


# _UndirectedAdjacencyBuilder: internal helper that accumulates undirected edges
class _UndirectedAdjacencyBuilder:
    # _adjacency: maps each node to the set of its linked neighbours
    def __init__(self):
        self._adjacency = {}

    # ingest: adds a validated edge to the adjacency sets
    def ingest(self, edge):
        self._adjacency.setdefault(edge.left, set()).add(edge.right)
        self._adjacency.setdefault(edge.right, set()).add(edge.left)

    # export: returns the sorted neighbour list dict from the adjacency sets
    def export(self):
        return {
            node: sorted(connected_nodes)
            for node, connected_nodes in self._adjacency.items()
        }


# edge_to_neighbour_list_i: candidate - validates each edge then ingests it into the builder
def edge_to_neighbour_list_i(edges, /):
    """Candidate I."""
    builder = _UndirectedAdjacencyBuilder()

    for pair in edges:
        builder.ingest(_ValidatedEdge(*pair))
    return builder.export()

