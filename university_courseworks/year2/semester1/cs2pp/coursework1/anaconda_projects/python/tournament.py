"""
tournament.py - CS2PP Coursework 1, Task 2: Python Classes and Optimisation Algorithms.

Task 2:

2.1) Tournament class (and nested Team class) built from a config JSON.

2.2) Compare two Tournament instances via the >= operator on champions.

2.3) Tournament_optimised child class using dynamic programming.

Requirements (from CS2PP_CW1.ipynb):

- Constructed from ./data/configTEST.json: 
  path, name, nteams, default_low, default_high, default_incr, prize.

- Protective validation on every config value 
  (range, increment, team count, file existence, required CSV columns).

- Sponsors and funding allocations assigned randomly, without duplication.

- Teams are their own Team class.

- Inventory acquired with the greedy knapsack: 
  many cars of the sponsor's Make, no duplicates in transaction.

- Pairwise bracket rounds; only the winner advances.

- Round winner receives prize, added to budget, then buys more inventory.

- New transactions may duplicate existing inventory but not within the transaction.

- Score = sum of MPG-H over inventory; __ge__ compares champions' scores.

Invariants to preserve:

- No duplicate sponsor; no duplicate budget; no duplicate car within a transaction
  (duplicates across rounds are allowed).

- configCOMPARE.json keeps the same data source but differing parameters.

- The greedy-vs-DP comparison in 2.3 must be fair: 
  same sponsors, teams and data, only the algorithm differs.

Note: the third-party modules explored in Week 5 may be used for Task 2 (optional).
"""

import csv
import json
import random


# TournamentDataError: base exception raised when tournament data or configuration fails validation.
class TournamentDataError(Exception):
    """Raised when tournament data or configuration fails validation."""


# Team: a sponsored team that collects an inventory of fuel efficient cars.
class Team:
    def __init__(self, sponsor, budget, algorithm = "greedy"):
        """Initialise the team with its sponsor, its budget and its acquisition algorithm."""

        self.sponsor = sponsor
        self.budget = budget
        self.inventory = []
        self.algorithm = algorithm

    def __str__(self):
        """Return the team's summary: sponsor, available budget, inventory size and score."""

        return f"Team sponsored by {self.sponsor} with ${self.budget} available and {len(self.inventory)} cars and a score of {self.score()}"

    def acquire(self, cars, budget):
        """Acquire inventory within budget, returning the acquired cars."""

        acquired = self._knapsack(cars, budget)

        self.inventory.extend(acquired)

        total_spent = 0

        for car in acquired:
            total_spent += car["Price"]

        self.budget = budget - total_spent

        return acquired

    def score(self):
        """Return the team's score: the sum of MPG-H ratings over its inventory."""

        total_score = 0

        for car in self.inventory:
            total_score += car["MPG-H"]

        return total_score

    def _knapsack(self, cars, budget):
        """Return the acquired cars using the team's configured algorithm."""

        if self.algorithm == "dp":
            return self._dp_knapsack(cars, budget)

        return self._greedy_knapsack(cars, budget)

    def _greedy_knapsack(self, cars, budget):
        """Return the greedy acquisition: efficient cars first, within budget, without duplicates."""

        acquired = []
        spent = 0
        seen = set()

        for car in sorted(cars, key = lambda car: car["MPG-H"], reverse = True):
            if car["Make"] != self.sponsor:
                continue

            key = (car["Make"], car["Model"], car["Year"], car["Price"])

            if key in seen:
                continue

            if car["Price"] <= budget - spent:
                acquired.append(car)
                spent += car["Price"]
                seen.add(key)

        return acquired

    def _dp_knapsack(self, cars, budget):
        """Return the optimal acquisition: 0/1 dynamic programming within the budget."""

        items = {}

        for car in cars:
            if car["Make"] != self.sponsor:
                continue

            key = (car["Make"], car["Model"], car["Year"], car["Price"])

            if key not in items:
                items[key] = car

        candidates = sorted(items.values(), key = lambda car: (-car["MPG-H"], car["Price"]))
        affordable = []

        for car in candidates:
            if car["Price"] <= budget:
                affordable.append(car)

        pruned = []
        cheapest = None

        for car in affordable:
            if cheapest is None or car["Price"] < cheapest:
                pruned.append(car)
                cheapest = car["Price"]

        total_pruned_cost = 0

        for car in pruned:
            total_pruned_cost += car["Price"]

        capacity = min(budget, total_pruned_cost)
        count = len(pruned)

        table = []

        for _ in range(count + 1):
            row = [0] * (capacity + 1)
            table.append(row)

        for index in range(1, count + 1):
            car = pruned[index - 1]
            price = car["Price"]
            value = car["MPG-H"]

            row = table[index]
            previous = table[index - 1]

            for weight in range(capacity + 1):
                row[weight] = previous[weight]

                if price <= weight and previous[weight - price] + value > row[weight]:
                    row[weight] = previous[weight - price] + value

        acquired = []
        weight = capacity

        for index in range(count, 0, -1):
            if table[index][weight] != table[index - 1][weight]:
                car = pruned[index - 1]
                acquired.append(car)
                weight -= car["Price"]

        acquired.reverse()

        return acquired


# Tournament: a competition between sponsored teams of car efficiency enthusiasts.
class Tournament:
    def __init__(self, config_path, *, seed = None):
        """Initialise the tournament from a JSON configuration file."""

        if not isinstance(config_path, str) or not config_path.strip():
            raise TournamentDataError("'config_path' must be a non-empty string.")

        try:
            with open(config_path, 'r', encoding = 'utf-8') as config_file:
                config = json.load(config_file)

        except FileNotFoundError as e:
            raise FileNotFoundError(f"Tournament config file not found: {config_path}") from e

        except json.JSONDecodeError as e:
            raise TournamentDataError(f"Tournament config is not valid JSON: {config_path}") from e

        required_keys = ("path", "name", "nteams", "default_low", "default_high", "default_incr", "prize")

        for key in required_keys:
            if key not in config:
                raise TournamentDataError(f"Tournament config missing required key: {key}")

        if not isinstance(config.get("name"), str) or not config.get("name").strip():
            raise TournamentDataError("'name' must be a non-empty string.")

        nteams = config.get("nteams")

        if isinstance(nteams, bool) or not isinstance(nteams, int) or nteams < 2:
            raise TournamentDataError("'nteams' must be an integer of at least 2.")

        default_low = config.get("default_low")
        default_high = config.get("default_high")
        default_incr = config.get("default_incr")
        prize = config.get("prize")

        for value in (default_low, default_high, prize):
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise TournamentDataError("Funding values and prize must be non-negative integers.")

        if default_high < default_low:
            raise TournamentDataError("'default_high' must be greater than or equal to 'default_low'.")

        if isinstance(default_incr, bool) or not isinstance(default_incr, int) or default_incr < 1:
            raise TournamentDataError("'default_incr' must be a positive integer.")

        if not isinstance(config.get("path"), str) or not config.get("path").strip():
            raise TournamentDataError("'path' must be a non-empty string.")

        self.path = config.get("path")
        self.name = config.get("name")
        self.nteams = nteams
        self.default_low = default_low
        self.default_high = default_high
        self.default_incr = default_incr
        self.prize = prize

        self._rng = random.Random(seed)
        self.teams = []
        self.cars = []
        self._champion = None
        self.bracket = []
        self.algorithm = "greedy"

    @property
    def champion(self):
        """Return the Team that won the tournament."""

        return self._champion

    def _read_cars(self):
        """Return the validated car inventory rows from the configured data path."""

        required_columns = ("Make", "Model", "Year", "Price", "MPG-H")

        with open(self.path, 'r', encoding = 'utf-8', newline = '') as csvfile:
            reader = csv.DictReader(csvfile)
            fieldnames = reader.fieldnames or []

            for column in required_columns:
                if column not in fieldnames:
                    raise TournamentDataError(f"Car data missing required column: {column}")

            cars = []

            for row in reader:
                if not row.get("Make"):
                    continue

                try:
                    cars.append({
                        "Make": row["Make"],
                        "Model": row["Model"],
                        "Year": int(row["Year"]),
                        "Price": int(row["Price"]),
                        "MPG-H": int(row["MPG-H"]),
                    })

                except (TypeError, ValueError) as e:
                    raise TournamentDataError(f"Invalid car data row: {row}") from e

        return cars

    def generate_sponsors_and_teams_with_inventory(self):
        """Assign distinct sponsors and budgets, then acquire inventory for each team."""

        cars = self._read_cars()
        self.cars = cars

        makes = []

        for car in cars:
            if car["Make"] not in makes:
                makes.append(car["Make"])

        if len(makes) < self.nteams:
            raise TournamentDataError(f"Tournament requires {self.nteams} sponsors; only {len(makes)} available.")

        sponsors = self._rng.sample(makes, self.nteams)
        budgets = self._rng.sample(list(range(self.default_low, self.default_high + 1, self.default_incr)), self.nteams)

        self.teams = []

        for sponsor, budget in zip(sponsors, budgets):
            team = Team(sponsor, budget, algorithm = self.algorithm)
            team.acquire(cars, budget)
            self.teams.append(team)

        return self.teams

    def hold_event(self):
        """Run the pairwise bracket tournament until a single champion prevails."""

        current = list(self.teams)
        rounds = []

        while len(current) > 1:
            matches = []
            winners = []

            for index in range(0, len(current) - 1, 2):
                left = current[index]
                right = current[index + 1]
                winner = left if left.score() >= right.score() else right

                winner.budget += self.prize
                winner.acquire(self.cars, winner.budget)

                matches.append((left, right, winner))

            if len(current) % 2 == 1 and len(current) > 1:
                winners.append(current[-1])

            for match in matches:
                winners.append(match[2])

            rounds.append(matches)
            current = winners

        self.bracket = rounds
        self._champion = current[0]

        return self._champion

    def show_win_record(self):
        """Print the tournament bracket, round by round, and the final result."""

        print(f"The {self.name} Tournament bracket:")

        for round_number, matches in enumerate(self.bracket, start = 1):
            header = "Final" if round_number == len(self.bracket) else f"Round {round_number}"

            print()
            print(header)
            print("-" * len(header))

            for index, (left, right, winner) in enumerate(matches, start = 1):
                print(f"Match {index}: {left} vs {right} -> {winner} wins.")

        print()
        print(f"The champion of the {self.name} Tournament is the {self._champion}.")

    def __ge__(self, other):
        """Return True if this tournament's champion scored higher than or equal to the other's champion."""

        if not isinstance(other, Tournament):
            raise TypeError("Can only compare Tournament instances.")

        return self._champion.score() >= other._champion.score()


# Tournament_optimised: Task 2.3 tournament that acquires inventory with dynamic programming.
class Tournament_optimised(Tournament):
    """Tournament that computes inventory acquisitions with dynamic programming instead of the greedy method."""

    def __init__(self, config_path, *, seed = None):
        """Initialise the optimised tournament, inheriting the configuration before switching strategy."""

        super().__init__(config_path, seed = seed)
        self.algorithm = "dp"

