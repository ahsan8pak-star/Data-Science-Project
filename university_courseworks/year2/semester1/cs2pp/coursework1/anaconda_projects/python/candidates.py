from dataclasses import dataclass


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

