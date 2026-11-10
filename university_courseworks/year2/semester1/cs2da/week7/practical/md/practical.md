---
geometry: margin=1in
title: 'CS2DA: Data Structures & Algorithms --- Practical 3'
colorlinks: true
fontsize: 12pt
...

This practical guides you through use of graph search algorithms (depth-first search, breadth-first search and iterative deepening search) on the game graphs of noughts and crosses and chess.

# Setup

As for the previous practicals, you will need a text editor and a JDK installation. On lab PCs in G56, the text editor Notepad++ is available from AppsAnywhere and the JDK is installed. Visual Studio Code is also available from AppsAnywhere.

Download the files `NoughtsAndCrosses.java` and `Chess.java` from Blackboard and save them in a suitable directory.

These files are AI-generated implementations of the well-known board games noughts and crosses (also known as tic-tac-toe) and chess. Both of these files implement the same API. An instance of either class represents the state of the game board, which will be a node in the graph. The public constructor creates a new object that represents the starting state of the game. The method `nextStates()` returns a list of states accessible from the current state by making a single move; that is, it returns the neighbours of a node. The method `outcome()` returns an `enum` that indicates whether the game is finished and, if so, whether it was drawn or won. The classes implement `toString()`, `equals()` and `hashCode()` sensibly.

For the sake of simplicity, the chess implementation omits rules that rely on knowing anything more than the current state of the board, namely castling, capturing en-passant and draws by repetition or lack of progress. If you do not know what any of that means, do not worry, as it is not important for this practical.

There is no `main()` method in either class. The simplest way to proceed is to add one to each class and write your code there. However, if you prefer, you can create a new class and put your code in there.

# Task 1: Recursive Depth-First Search

To familiarise yourself with the API provided by `NoughtsAndCrosses.java`,
write a **recursive** depth-first search that finds any winning game of noughts and crosses
and prints out the play (sequence of moves) that leads to the win.

# Task 2: Non-Recursive Depth-First Search

Noughts and crosses has a very small state space. The whole game graph can easily be enumerated and fit in memory, even on very old computers.
Combined with its simple rules, this makes it popular for illustrating algorithms for playing games from classical AI.
It is well-known that, with perfect play by both players, noughts and crosses will always end in a draw.
Indeed, the experience of adult human players is that almost all games end in a draw.

Using a **non-recursive** depth-first search, count and print out the number of distinct completed games that end in a draw and the number that end in a win.

Take "distinct" to mean that the final board states are different, regardless of how they were reached. That is, you are trying to count the number of leaf nodes in the game graph with each outcome. Do not bother trying to check for symmetries.

# Task 3: Breadth-First Search

Chess has a very large state space, although not as large as that of Go. This makes it infeasible to construct or explore the whole game graph. Realistic algorithms for playing chess use heuristics to prune the graph in order to focus on the most likely lines of play. However, we can still use basic graph search algorithms to search up to a limited depth.

Using **breadth-first** search, find the shortest possible play that ends in a win for either player. You will need to think about how to record the sequence of moves that leads to the winning state during the search.

# Task 4: Iterative Deepening Search

In lectures, it was claimed that iterative deepening is useful on very large or infinite graphs, as (compared with breadth-first search at the same depth) it uses far less memory and only a constant factor more time.

How far can your breadth-first search go with 1 GB of memory? Modify your program from the previous task to count the number of nodes found (added to the queue) and periodically print out the node count, time taken and memory used by the program. You are not looking for any particular nodes in the graph this time, just seeing how many you can explore. You should also remove tracking of whether a node has previously been seen; this increases the branching factor of the search, but decreases the memory usage.

Now implement iterative deepening search, printing out the same information. (Note that the node current count resets every time you increment the target depth.) How do the two compare?

# Conclusion

The basic graph search algorithms are fairly simple to implement.
However, it can be fiddly to track extra details,
such as the path taken through the graph.

In spite of its apparent wastefulness,
the low memory usage of
iterative deepening search makes it a practical alternative to breadth-first search
on very large or infinite graphs that are represented implicitly.

