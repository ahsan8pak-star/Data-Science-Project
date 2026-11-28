"""
Generate the personalised road-network adjacency matrices for CS2DA coursework.

Replicates the logic of ``java/GenerateNetwork.java``, 
so the coursework can be reproduced without a Java toolchain.
"""

import heapq
import math

STUDENT_ID = 34001219
LOCATIONS = "A, B, C, D, E, F"

SPEED_LOW = 5.0    # miles per hour: pairwise distance below 5 miles
SPEED_MID = 20.0   # miles per hour: pairwise distance between 5 and 10 miles
SPEED_HIGH = 30.0  # miles per hour: pairwise distance above 10 miles


class _Random:
    """
    Python twin of ``java.util.Random`` for the network data generation.

    The state is the 48-bit linear congruential generator Knuth described in
    the Art of Computer Programming, section 3.2.1, seeded by scrambling the
    student number the same way the Java constructor does.
    """

    def __init__(self, seed: int):
        self.state = (seed ^ 0x5DEECE66D) & 0xFFFFFFFFFFFF
        self.cached_gaussian = 0.0
        self.have_cached_gaussian = False

    def next(self, bits: int) -> int:
        self.state = (self.state * 0x5DEECE66D + 0xB) & 0xFFFFFFFFFFFF
        return self.state >> (48 - bits)

    def next_double(self) -> float:
        return ((self.next(26) << 27) + self.next(27)) * (2.0 ** -53)

    def next_gaussian(self) -> float:
        if self.have_cached_gaussian:
            self.have_cached_gaussian = False
            return self.cached_gaussian
        while True:
            v1 = 2 * self.next_double() - 1
            v2 = 2 * self.next_double() - 1
            s = v1 * v1 + v2 * v2
            if 0 < s < 1:
                break
        multiplier = math.sqrt(-2 * math.log(s) / s)
        self.cached_gaussian = v2 * multiplier
        self.have_cached_gaussian = True
        return v1 * multiplier

    def next_int(self, bound: int) -> int:
        if bound <= 0:
            raise ValueError("bound must be positive")
        u = self.next(31)
        r = u % bound
        m = bound - 1
        while u - r + m < 0:
            u = self.next(31)
            r = u % bound
        return r


def generate(student_id: int, n: int = 6):
    """
    Return the n x n adjacency matrix of direct distances (miles) for the
    student number, with NaN marking a missing road.
    """
    random = _Random(student_id)
    offset = (student_id % 5) / 5.0

    distances = [[float("nan")] * n for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            distance = math.floor(30 * abs(offset - random.next_gaussian()))
            distances[i][j] = float(distance)
            distances[j][i] = float(distance)

    # Mark two distinct, randomly chosen entries in each row as missing.
    # These omissions are independent by row, so the displayed matrix need not remain symmetric.
    for i in range(n):
        first = random.next_int(n)
        second = random.next_int(n - 1)
        if second >= first:
            second += 1
        distances[i][first] = float("nan")
        distances[i][second] = float("nan")

    # The diagonal represents the distance from each location to itself.
    for i in range(n):
        distances[i][i] = 0.0

    return distances


def travel_time(distance: float):
    """
    Return the travel time in hours from a direct distance in miles, using
    the coursework speed rule: 5 mph below 5 miles, 20 mph from 5 up to and
    including 10 miles, and 30 mph above 10 miles.
    """
    if math.isnan(distance):
        return float("nan")
    
    if distance < 5:
        speed = SPEED_LOW
    
    elif distance <= 10:
        speed = SPEED_MID
    
    else:
        speed = SPEED_HIGH
    
    return distance / speed


def to_travel_times(distances):
    """
    Convert the adjacency matrix of direct distances into one of travel times.
    """
    return [[travel_time(distance) for distance in row] for row in distances]


def dijkstra(graph, start: int = 0):
    """
    Return the shortest-path costs from `start` over the adjacency matrix
    `graph` (miles for the distances matrix, hours for the travel-time matrix;
    NaN marks a missing road).

    Dijkstra's algorithm extracts the minimum-cost node from a priority queue,
    relaxes its edges, and repeats. The standard-library priority queue has no
    decrease-key operation, so the decrease-key step is implemented here as lazy
    deletion: a new queue entry is pushed whenever a shorter path is found, and
    stale entries are skipped when they are extracted.

    Returns a list of shortest-path costs from `start` to each location, with
    NaN for locations that cannot be reached from `start`.
    """
    n = len(graph)
    dist = [math.inf] * n
    dist[start] = 0
    heap = [(0, start)]
    
    while heap:
        cost, u = heapq.heappop(heap)
    
        if cost > dist[u]:
            continue  # stale entry: the decrease-key was applied when it was pushed
    
        for v in range(n):
            if u == v:
                continue
    
            weight = graph[u][v]
    
            if math.isnan(weight):
                continue
    
            candidate = cost + weight
    
            if candidate < dist[v]:
                dist[v] = candidate
                heapq.heappush(heap, (candidate, v))
    
    return [float("nan") if math.isinf(value) else value for value in dist]


def _format_cell(value: float) -> str:
    if math.isnan(value):
        return "NaN".rjust(8)
    return str(int(value)).rjust(8)


def _format_time_cell(value: float) -> str:
    if math.isnan(value):
        return "NaN".rjust(8)
    return f"{value:>8.2f}"


def print_matrix(distances, times=None):
    """
    Print the adjacency matrix of direct distances, and the converted matrix
    of travel times when one is supplied.
    """
    print("The adjacency matrix showing direct distances (miles)")
    print("amongst " + LOCATIONS + " is given by:")
    print()
    
    for row in distances:
        print("".join(_format_cell(value) for value in row))

    if times is not None:
        print()
        print("The adjacency matrix showing direct travel times (hours)")
        print("amongst " + LOCATIONS + " is given by:")
        print()
    
        for row in times:
            print("".join(_format_time_cell(value) for value in row))


def main():
    student_id = STUDENT_ID
    sid = str(student_id)

    if sid[:2] != "34" or len(sid) != 8:
        print("WARNING: YOU NEED TO PUT YOUR STUDENT ID IN THE PROGRAM SOURCE CODE.")

    print("Student ID: " + str(student_id))
    
    distances = generate(student_id)
    times = to_travel_times(distances)
    
    print_matrix(distances, times)

    shortest_distances = dijkstra(distances, 0)
    shortest_times = dijkstra(times, 0)

    print()
    
    print("The shortest distances (miles) from " + LOCATIONS.split(", ")[0] + " are:")
    
    for i, location in enumerate(LOCATIONS.split(", ")):
        value = shortest_distances[i]
        value_str = "NaN" if math.isnan(value) else f"{value:.0f}"
        print(f"Shortest distance from {location}: {value_str}")

    print()
    
    print("The shortest travel times (hours) from " + LOCATIONS.split(", ")[0] + " are:")
    
    for i, location in enumerate(LOCATIONS.split(", ")):
        value = shortest_times[i]
        value_str = "NaN" if math.isnan(value) else f"{value:.2f}"
        print(f"Shortest travel time from {location}: {value_str}")


if __name__ == "__main__":
    main()

