"""
tournament.py -- CS2PP Coursework 1, Task 2: Python Classes and Optimisation
Algorithms.

Task 2 map
----------
2.1  Tournament class (and nested Team class) built from a config JSON.
2.2  Compare two Tournament instances via the >= operator on champions.
2.3  Tournament_optimised child class using dynamic programming.

Requirements (from CS2PP_CW1.ipynb)
-----------------------------------
- Constructed from ./data/configTEST.json: path, name, nteams,
  default_low, default_high, default_incr, prize.
- Protective validation on every config value (range, increment, team
  count, file existence, required CSV columns).
- Sponsors and funding allocations assigned randomly, without duplication.
- Teams are their own Team class.
- Inventory acquired with the greedy knapsack: many cars of the sponsor's
  Make, no duplicate car within one transaction.
- Pairwise bracket rounds; only the winner advances.
- Round winner receives prize, added to budget, then buys more inventory.
- New transactions may duplicate existing inventory but not within the
  transaction.
- Score = sum of MPG-H over inventory; __ge__ compares champions' scores.
- show_win_record prints the bracket in the format shown in the brief.

Invariants to preserve
----------------------
- No duplicate sponsor; no duplicate budget; no duplicate car within a
  transaction (duplicates across rounds are allowed).
- configCOMPARE.json keeps the same data source but differing parameters.
- The greedy-vs-DP comparison in 2.3 must be fair: same sponsors, teams
  and data, only the algorithm differs.

Note: no local CS2PP material teaches dynamic programming (Week 5 folder
is empty); the knapsack descriptions are the Blackboard supplement. Implement
against that material, not from memory.
"""

