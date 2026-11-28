# CS2DA Technical Report

**Module Code:** CS2DA

**Assignment Title:** Finite State Automata & Dijkstra's Algorithm

**Student Number:** 34001219

**Actual hours spent:** 16

**Other learning aids used (please list):** CS2DA lecture slides and practical materials (Weeks 7 - 9)

**AI tools used:** OpenCode (Model: Flint 40B Free)

---

## 1. Drawing a DFA with GraphViz

The first two tasks of the assignment centre on drawing a deterministic finite state automaton with the GraphViz suite.

**Implementation note.** The assignment brief permits either Java or Python.

As my expertise is in Python and the coursework was to continue in advance, the Java files supplied for Tasks 1 and 2 were translated into the Python implementations used for the submission: the supplied `GenerateDFA.java` became the Python transition table generator and GraphViz drawer (`coursework/python/generate_dfa.py`), and the network program `GenerateNetwork.java` became the Python network utilities (`coursework/python/generate_network.py`).

The supplied `GenerateDFA.java` produced the personalised transition function and accepting states:

- Initial state: `q0`
- Accepting state: `q2`
- Transition function (states `q0`, `q1`, `q2`; alphabet `a`, `b`, `c`):

```Java
int delta[][] = {
    {1, -1, -1},
    {2, 1, 0},
    {-1, 0, 0},
};

boolean accepting[] = {
    false, false, true
};
```

The generated diagram was produced with the GraphViz `dot` executable from the `.dot` source written by the Python drawer (`generate_dfa.py` / `draw_dfa.py`, source at `coursework/dot/dfa.dot`), using a top-down layout (`rankdir = TB`), a point for the start state, and a double circle for the accepting state.

In the report we include:

- a listing of the `.dot` file used to create the diagram;
- an image of the diagram itself;
- evidence that the correct states and transitions were used;
- the visual style of the diagram (top-down rank, start marker, accepting-state double circle, labelled edges).

The exact positional layout of the nodes is left to GraphViz, as the briefing permits.

## 2. Algorithm for drawing a DFA with GraphViz

**Input:** a transition function for a deterministic finite state automaton, represented as an array, and an array of whether each state is accepting.

**Output:** a GraphViz `.dot` file, from which a diagram of the automaton can be generated.

The implemented algorithm (`generate_dot` in  `coursework/pseudocode/draw_dfa.txt`) emits the boilerplate, the start-state marker, the accepting-state decorations and one labelled edge per defined transition, skipping undefined transitions (`delta[q][a] = -1`).

The time complexity in terms of the number of states `Q` and the size of the alphabet `S` is `O(Q * S)`: the accepting-state pass is `O(Q)`, the boilerplate is `O(1)`, and the transition loop inspects each of the `Q * S` state/symbol pairs once, doing `O(1)` work per pair.

## 3. Adjacency matrix of travel time

The road network links six locations, denoted `A, B, C, D, E, F`. `GenerateNetwork.java` (mirrored by `coursework/python/generate_network.py`) produced the adjacency matrix of
direct distances (miles), where `NaN` marks a missing road:

```
       0      15     NaN       9      42      10
      15       0      46      37     NaN     NaN
      26     NaN       0      24     NaN      32
       9      37     NaN       0      38      84
      42     NaN      28      38       0     NaN
      10     NaN     NaN      84      26       0
```

Because some roads are one-way, the matrix need not be symmetric.

In rush hour, the travel time between adjacent locations uses the coursework speed rule: 5 mph if the pairwise distance is below 5 miles; 20 mph if the distance is between 5 and 10 miles; and 30 mph when the distance is above 10 miles. The conversion from the adjacency matrix of distances to the adjacency matrix of travel times is `to_travel_times` in `coursework/python/generate_network.py`.

In the report we include:

- an image of the network graph of distances (drawn by
  `coursework/python/draw_network.py` from the personalised matrix, source at `coursework/dot/network.dot`, image at `coursework/images/network.svg`);
- a Python listing of the program that converts the adjacency matrix of distances to one of travel times.

## 4. Implementing and using Dijkstra's Algorithm

The task was to implement Dijkstra's algorithm and use it to find, from location `A`, the shortest distance and the shortest travel time to each of `B, C, D, E, F`.

`dijkstra` was added to `coursework/python/generate_network.py` (heap-based, with the coursework's lazy decrease-key) and mirrored in `coursework/java/GenerateNetwork.java` (Java `PriorityQueue` with the same lazy decrease-key). Both read the adjacency matrix of distances (miles) or of travel times (hours) and return the shortest-path cost from the start node.

Running the algorithm from `A` on the personalised network gives:

- shortest distances from `A` (miles): `A = 0`, `B = 15`, `C = 61`, `D = 9`, `E = 36`, `F = 10`;
- shortest travel times from `A` (hours): `A = 0`, `B = 0.5`, `C = 2.03`, `D = 0.45`, `E = 1.37`, `F = 0.5`.

In the report we include:

- a Python listing of the program;
- the shortest distances from `A` as found by the program;
- the shortest travel times from `A` as found by the program.

## 5. Discussion and illustration of Dijkstra's Algorithm

The standard-library priority queues in Java (`PriorityQueue`) and Python (`heapq`) do not provide the ability to decrease the priority of an element already in the queue. This is an important part of Dijkstra's algorithm: when a shorter path to a node is discovered after an entry was queued, the queue entry for that node must be improved.

We worked around this by lazy deletion: whenever a shorter candidate path is found, a new queue entry is pushed with the improved cost, and entries that are no longer current are skipped when they are extracted. Both the Python twin (pushing onto `heapq`) and the Java twin (pushing onto a `PriorityQueue` whose entries implement `Comparable`) use this workaround.

**Q: Did it affect the time complexity?**

A: With a true decrease-key the heap-based implementation runs in `O((V + E) log V)`; with lazy deletion the worst case is `O(E log E)`. For this small road network (six locations) the practical impact is negligible, and the algorithm remains correct, provided the graph has non-negative weights - which holds here, since all distances and travel times are non-negative.

Illustration from `A` (shortest distance, personalised network), step by step:

1. Initialise `dist[A] = 0` and all other nodes at infinity; queue = `[(0, A)]`.
2. Extract `A` (cost 0); relax edges: `B = 15`, `D = 9`, `E = 42`, `F = 10. Queue: `[(9, D), (10, F), (15, B), (42, E)]`.
3. Extract `D` (cost 9); relax: no improvement (B via D = 46 > 15, E via D = 47 > 42, F via D = 93 > 10).
4. Extract `F` (cost 10); relax: `E = 36` (via F) improves `E` from 42; others unchanged.
5. Extract `B` (cost 15); relax: `C = 61` (via B); others unchanged.
6. Extract `E` (cost 36); relax: `C` via E = 64 does not improve `C` (61).
7. Extract `C` (cost 61); relax: no improvements.

Final shortest distances from `A`: `B = 15`, `C = 61`, `D = 9`, `E = 36`, `F = 10`.

---

## 6. Presentation

Ten marks will be for the presentation of the report. Headings are included for each section and formatting is consistent throughout; the front page carries the module code, assignment title, student number, hours and learning aids as the submission requirements specify.
