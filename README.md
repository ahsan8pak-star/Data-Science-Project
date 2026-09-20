# Data Science Project

A personal project to advance my career in Data Science.

---

# Completed Tasks

- CLI Commands from **Powershell/CMD (mainly used)** and **Ubuntu/Linux (eventually will come later on in main projects)**
- Git Version Control from **GitHub & GitLab (both of them synchronized with VSC as a 'middle man')** and **Git Bash (rarely used)**

*The rest of the tasks are categorised into its own subheadings respectively below:*

---

# Python Fundamental Topics

All fundamental and applied topics learnt in their respective folder, known as `fundamental_topics`.

---

## Imperative Programming

| Topic Name | Descriptions |
| --- | --- |
| Environment & Execution | **(PyCharm / Visual Studio Code) IDE installation, interpreter mechanics, `print()`** |
| Variables & Core Types | **Data declarations, interactive `input()`, type casting via `int()` / `float()`** |
| String Manipulation | **F-strings, index parsing, multi-line strings, string methods** |
| Arithmetic & Maths Operations | **Operators, BIDMAS operatortions, maths module functions** |
| Conditions & Control Flow | **`if`, `elif`, `else`, logical `and` / `or` / `not`, comparison operators** |
| Loops & State Control | **`while` loops, `for` loops, nested loops, `break` statements** |
| Lists & Matrices | **Arrays, 2D Matrices, index modification, list methods like `.append()` and `.sort()`** |
| Tuples & Dictionaries | **Immutable sequences, tuple unpacking, key-value data structures** |
| Functions | **`def` blocks, positional/keyword arguments, parameter passing, `return` statements** |
| Exceptions | **`try`, `except` error handling structures** |
| Reusable Logic & Code Style | **Function refactoring, `#` syntax comments documentation** |
| Modules | **Importing, creating modules and descriptions of its various types** |
| Scope Resolution | **Range of variable scopes within functions i.e. (LEGB) Local -> Enclosed -> Global -> Built-in** |
| `__main__` | **Software Development Practical and Security Function using `def main():` and `if __name__ == __main__:`** |
| `datetime` | **Applied dates, times, timezones, formatting, and time-based comparisons via `datetime` module** |

---

## Object-Oriented Programming

| Topic Name | Descriptions |
| --- | --- |
| Classes | **Objects and classes through import created modules, and fundamental variable assignments** |
| Class Variables | **Outside of constructor's scope as a global variable** |
| Constructors | **`def __init__ (self)` -> `self.variable == variable` and printing the objects within the class itself** |
| Inheritance | **Combination of the classes, methods and constructors and derived the basic definitions to grasp its full use and applications** |
| Multiple & Multi-Level Inheritance | **Extension of inheritance with applied child and parent classes, its methods, attributes and functions all intertwined / interconnected to each other** |
| Abstract Classes | **Applied classes of non - instantitated rules to understand its own functions through parent and child classes** |
| `super()` | **Applied constructors of `def __init__(self,...)` -> `super().__init__(...)`** |
| Polymorphism | **Fundamental OOP concept. *Go to **Inheritence** as reference*** |
| Aggregation | **"Has-a" relationship -> refers 'independent' classes** |
| Composition | **"Owns-a" relationship. Uses 'components' (dependents) to represent a composite object (independent)** |
| Nested Classes | **Similar to `Nested Loops` in `Imperative Programming`. *Go towards `Inheritence` for more fundamental reasons*** |
| Static Methods | **Alternative to `Instance Methods`. *Go to `Nested Loops` for further context*** |
| Class Methods | **Alternative to `Static Methods`. *Go to `Nested Classes` and `Static Methods` for further context*** |
| Magic Methods | **Branch of `Class Methods` and `Constructors`. *Refer to `Nested Classes` for further context*** |
| Decorator | **Unique method used to make functions into attributes. *Go to `Abstract Methods` and `Class Methods` for more information*** |
| Property | **Combination of functions as attributes i.e. objects functioning as its own attributes. *Go to `Decorator` , `Magic Methods` and `Class Methods` for its full responses*** |
| Iterator | **`__iter__` and `__next__` as OOP alternatives to `while` loops and (index) increments respectively** |
| Generator | **`yeild` method as an alternative to `return` within `def` blocks i.e. an iterator function** |

---

## Functional Programming

| Topic Name | Descriptions |
| --- | --- |
| Any & All | **`any()` and `all()` short-circuit predicate checks over iterables, including their empty-iterable semantics** |
| Closures | **Nested functions capturing ("remembering") a value from their outer function even after it has finished running** |
| Comprehensions | **List, set, and dictionary comprehensions as compact, declarative loops with optional `if` filters** |
| Currying | **Turning a multi-argument function into a chain of single-argument functions, i.e. `add(a, b)` becomes `add(a)(b)`** |
| Filter | **`filter()` combined with lambda predicates to conditionally select items from a list - even and odd numbers, values both above and below a threshold, and non-empty strings** |
| First-Class Functions | **Functions treated as values - stored in variables, passed as arguments, and returned from other functions** |
| itertools Module | **`itertools` building blocks such as `chain`, `count`, `islice`, `cycle`, `repeat` and `product`** |
| Lambda | **Anonymous one-expression functions assigned to variables, applied across arithmetic, comparison, and conditional (ternary) use cases** |
| Map | **`map()` applying a lambda across single and multiple iterables - squaring/doubling values, type conversion, and pairwise combination of 2 lists** |
| Partial Application | **`functools.partial` pre-filling arguments to create specialised versions of a general function** |
| Pipelines | **Chaining functional steps (`filter` -> `map` -> `sorted` -> `reduce`) into immutable data flows** |
| Pure Functions | **Deterministic, side-effect-free functions contrasted with impure functions that read or change external state** |
| Reduce | **`functools.reduce` accumulating an iterable down to a single value - running sums, products, and largest items** |
| Sorted | **`sorted()` returning a NEW sorted list with lambda `key` functions and `reverse`, without mutating the original** |
| Zip | **`zip()`combining multiple iterables into paired tuples, with unpacking via for loop across matched indices** |

---

# Applied Foundation Projects

All python files have been made into their respective folders from each programming methods used throughout based on the applications from `fundamental_topics` folder as its reference.

---

## Imperative Programming

---

**Unit & Format Converters:**

| File Name | Topics Covered |
| --- | --- |
| Fahrenheit & Celcius | **Function fundamentals with basic conditional loops** |
| Phone Number Converter | **`match case` function & conditional loops** |
| Roman Numerals Converter | **Conditional loops, `input()` functions, `match cases` fundamentals & exception rules** |
| Time Coverter | **Fundamental `match cases`, including error catching within conditional loops** |
| Weight Converter | **Conditional logic integration** |

---

**Interactive Games:**

| File Name | Topics Covered |
| --- | --- |
| Dice Game | **Fundamental dictionary / sets, applied arrays / lists and applied conditional loops with creative TUI display** |
| Haiku - Madlibs | **F-strings with lists and `import random`** |
| Hangman Game | **Applied Dictionaries, for loops, tuples and conditional statements with `import random`** |
| Numerical Guessing Game | **`while` loop & `break` engine execution** |
| Quiz Game | **Fundamental lists and conditional `for` loops, including basic mathematical operations i.e. percentage score** |
| Rock Paper Scissors | **Applied `def` functions, conditional loops with ASCII Art and formatting** |
| Word Guessing Game | **Conditional loops, `input()` functions & list fundamentals** |

---

**Math & Science Calculators:**

| File Name | Topics Covered |
| --- | --- |
| Area & Volume Calculator | **Functions combining 2 basic files with advanced user `input()`** |
| Area | **Basic arithmetic functions with 2 values** |
| Area of Circle | **Mathematical functions, including user `input()`** |
| Area of Triangle | **Basic mathematical functions, with a fundamental user input function** |
| Annual Rate Calculator | **Exception functions & formatting within mathematical formulas** |
| Arithmetic Calculator | **Basic `match cases` with extensive conditional loops and f-strings with the inclusion of fundamental mathematical unit formatting** |
| Arithmetic Expressions | **Created `import math` module i.e. `Arithmetic Calculator`, f-strings and TUI displays based on `Arithmetic Calculator`** |
| Arithmetic Iteration | **Imported created modules, f-strings with the inclusion of fundamental mathematical formulas and TUI displays** |
| Card Validator Program | **Applied for loops and list indexing with fundamental variable assignments** |
| Circle Calculator | **Fundamental mathematical functions and imported created modules, with applied user error catching and TUI** |
| Circumference of Circle | **Mathematical functions, including user `input()`** |
| Compound Debt Calculator | **Mathematical formulas in relation to `Compound Interest Rate`, including fundamental conditional loops** |
| Compound Interest Rate | **Mathematical formulas, including fundamental conditional loops, `try-except` error catching and f-strings** |
| Cosine Rule | **Advanced Mathematical functions** |
| Euclidean Distance Calculator | **Applied mathematical functions thorugh user `input()` and an example case to check its functionality and durability** |
| Gradient Calculator | **Mathematical functions for calculating graphical slopes and gradients** |
| Perimeter of Triangle | **Basic mathematical functions with user `input()`** |
| Pythagoras Theorem | **Advanced Mathematical functions** |
| Simple Debt Calculator | **Mathematical formulas in relation to `Simple Interest Rate`, including fundamental conditional loops** |
| Simple Interest Rate | **Mathematical formulas, including fundamental conditional loops, `try-except` error catching and f-strings** |
| Sine Rule | **Advanced Mathematical functions** |
| Square Number Times Tables | **Mathematical iteration using a single loop, modules `import`, and formatted f-strings** |
| Times Tables | **Mathematical iteration using nested loops, advanced user `input()`, and formatted f-strings** |
| Triangle Calculator | **Functions combining 2 basic and 2 advanced files with advanced user `input()`** |
| Volume | **Basic arithmetic functions with 3 values** |

---

**Syntax Exercises:**

| File Name | Topics Covered |
| --- | --- |
| Activity Log.txt | *Go to `File Handling` for more* |
| Add | **`+` -> Addition** |
| AIM.txt | *Go to `File Writer` for more* |
| Alarm Clock | **`import datetime`, `import time` ,`import os` and `import pygame`, with the application of alarm clocks via personalised / customised sound files when time's up** |
| Banking Program | **Applied arithmetic formulas under fintech, error catching, `def` functions and `match case` with TUI displays** |
| Checkout System | **User `input()` and type conversions** |
| Count Up Timer | **Foundational default arguments and `import time`** |
| Distance Calculator | **`floats` and user `input()` demonstration.** |
| Divide | **`/` -> Division** |
| Drink Script Example | **Imports `favourite_food` from a created module and defines `favourite_drink`; runs standalone** |
| Email Slicer | **Index formatting fundamentals** |
| Even & Odd Loop Detector | **Fundamental conditional `for` loop and modulus operator (`%`)** |
| Factorials | **Iterative Sequence Multiplication** |
| File Handling | **Comprehensive file I/O operations and context managers** |
| File Reader | **Read functions and string parsing fundamentals** |
| File Writer | **File I/O fundamentals** |
| Food Menu | **Dictionaries and/or sets and applied conditional loops** |
| Food Script Example | **Exposes `favourite_food` for import and a content-named `show_food_script()` entry with a `__main__` guard** |
| Grade Boundary Calculator | **Integers with conditional `if-else` loops** |
| Hour Clock | **Fundamental `import time` and scaling it up to its real world resemblence through previous files made on such** |
| Input / Output CSVs | *Go to `File Handling` for more* |
| Input / Output JSONs | *Go to `File Handling` for more* |
| Input / Output / Test TXTs | *Go to `File Handling` for more* |
| LeapYear | **Basic Mathematical functions under conditional loops** |
| Math File | **Fundamental `import` modules and basic printing various cases** |
| Math Module | **Fundamental created `import` modules and basic mathematical functions** |
| Minute Time | **Fundamental `import time` and basic scaling from its previous file to test its functionality** |
| Multiply | **`*` -> Multiplication** |
| Number Matrix Display | **Nested loops with advanced formatted grid outputs** |
| Num Pad | **2D lists and nested conditional loops** |
| Prime Numbers | **Iterative sequence filtration and identification** |
| Random Cipher | **`import random` and `import string`, with applied `input()` functions, f-strings and conditional loops** |
| Random Colour Generator | **`from random import randint`, `match-case` statements, applied f-strings, nested for loops and `try-except` error catching.** |
| Reverse List Program | **Fundamental list manipulation via slicing and comprehensions, applied type validation using `all()` method, and conditional string formatting.** |
| Seconds Countdown | **Fundamental `import time` under its essential `def` function including f-string methods to present it accurately** |
| Shipping Label | **Foundational `xArgs` and `xKwargs`, applied dictionaries, and walrus operator (`:=`) under a specific for conditional loop as well as string methods being applied throughout.** |
| Shopping Cart | **Fundamental lists under a function within a `for` conditoinal loop, including `try-except` error catching and f-string methods.** |
| Square | **`pow(x, y)` == `**`** |
| Subtract | **`-` -> Subtraction** |
| Symbol Generator | **Fundamental nested loops with user `input()`s, `try-except` error catching and conditional loops.** |
| Username Status | **Fundamental conditional expressions with advanced string methods.** |

---

## Object-Oriented Programming

---

**Syntax Fundamentals:**

| File Name | Topics Covered |
| --- | --- |
| Bank Account | **Encapsulation, instance methods, custom string formatting (`__str__`), state mutation through deposits and withdrawals, and object-level data management** |
| Calculator | **Static methods, utility functions, and reusable class-level operations for arithmetic logic** |
| Car | **Fundamental classes, attributes, methods, constructors, and importing created modules** |
| Device | **Abstract classes, inheritance, method overriding, base/derived class design, and `super()` call mechanics** |
| Dice | **Applied import modules within OOP (e.g., `from dice_game import dice_art`), object-based simulation, and basic file interaction** |
| Employee Contract | **Multiple inheritance, combined class behaviour, and real-world worker role modelling** |
| Food | **Multi-level inheritance, layered class hierarchies, and specialised food categories such as snacks, desserts, and drinks** |
| Grocery Caloric List | **Class methods as alternative constructors, duck typing across differing grocery item types, and iterative aggregation for total caloric summation** |
| Item | **Magic methods, dunder methods, custom comparisons, item lookup, and built-in operator behaviour** |
| Order | **Class variables versus instance variables, constructors (`__init__`), object tracking, and aggregated calculations** |
| Payment | **Polymorphism, shared interfaces, and differing implementations for cash, card, and bank transfer payments** |
| Person | **Fundamental classes, methods, and importing created modules for object practice** |
| Point | **Fundamental classes, methods, constructors, and importing created modules** |
| Real Estate | **Property decorators, validation logic, getter/setter patterns, and real-world attribute checking** |
| Restaurant | **Aggregation and composition, managing nested objects such as menus, and dynamic state updating** |
| School | **Class relationships, has-a / owns-a modelling, collection management inside classes, and multi-class interaction** |
| Sports | **Nested classes, grouped related classes, and domain-specific object organisation** |
| User Access | **Decorator-based access control, login validation, permission checks, and wrapper logic** |
| Worker | **Inheritance hierarchies, subclass-specific behaviour, and switch-style matching through object type dispatch** |

---

## Functional Programming

---

**Syntax Fundamentals:**

| File Name | Topics Covered |
| --- | --- |
| Grade Summary | **Applied `filter()`, `reduce()` and `any()` / `all()` to summarise passing, failing and average student grades** |
| Number Pipeline | **A basic `filter` -> `map` -> `reduce` data flow computing the sum of squared even numbers** |
| Shopping Receipt | **Applied `map()`, `filter()` and `reduce()` to total a shopping basket and print a formatted receipt** |
| Word Frequency | **Applied `sorted()` with lambda keys and a set comprehension to tally repeated words** |

---

# University Courseworks

This is where university modules and its coursework goes under for the application of Python (*Read Above for more information about its topic usage*)

---

## CS1IP

---

**Coursework 1 -> 1st half of Semester 1 at Year 1**

| File Name | Topics Covered |
| --- | --- |
| Average Grades | **`Python Fundamental Topics` -> `Imperative Programming` -> `Lists & Matrices` , `Loops & State Control` , `Conditions & Control Flow` , `Functions` and `Main`** |
| Hello | **`Python Fundamental Topics` -> `Imperative Programming` -> `Environment & Execution`** |
| Ice Cream | **`Python Fundamental Topics` -> `Imperative Programming` -> `Conditions & Control Flow` , `Loops & State Control` and `Exceptions`** |
| Seven Segment | **`Python Fundamental Topics` -> `Imperative Programming` -> `Lists & Matrices` , `Loops & State Control` , `Conditions & Control Flow` , `Functions` and `Main`** |
| Volume | **`Python Fundamental Topics` -> `Imperative Programming` -> `Functions` , `Modules` and `Arithmetic & Maths Operations`** |

---

**Coursework 2 -> 2nd half of Semester 1 at Year 1**

| File Name | Topics Covered |
|---|---|
| Sort Comparison | **`Python Fundamental Topics` -> `Imperative Programming` -> `Lists & Matrices` , `Loops & State Control` , `Conditions & Control Flow` , `Functions` , `Modules` and `Main`** |

---

## Advanced Projects

This is for extensive and multi-level applications such as machine learning and specific topics dedicated for data science.

---

**Machine Learning**

| Folder Name | File Types |
| --- | --- |
| Music | **multiple `music_---.ipynb`, `music-recommender.dot`, `music-recommender.joblib` and `music.csv`** |
| Video Games | **multiple `vg_---.ipynb`, `vg-sales-recommender.dot`, `vg-recommender.joblib` and `vgsales.csv`** |
| Data Outliers | **`data_outlier.ipynb` and `data_outlier.py`** |

---

**Music Player**

| Folder Name | File Types |
| --- | --- |
| TUI | `mp3_` & `wav_` -> `tui_player.py` |
| GUI | `mp3_` & `wav_` -> `gui_player.py` |

---

**Transactions**

| File Name | File Usage / Purpose |
| --- | --- |
| transactions.py | **Python Excel Automation Script** |
| transactions.xlsx | **Raw / Original Excel Spreadsheet / Dataset** |
| transactionsv1.xlsx | **Modified Excel sheet with barcharts and references** |

---

## Timetable

*Summer 2026 block (Jun 1 – Sep 13, now historical; kept as a tickable record. Unticked items roll into Summer 2027 Block II.)*

### Phase 1: Environment & Pure Syntax (Jun 1 – Jun 28)

- [x] **Week 1 — CLI & environment** (Windows CMD, VS Code, Boot.dev): CLI navigation without the mouse (`cd`, `mkdir`, `dir`, `cls`); install Python 3 and VS Code via terminal prompts; 25–30 h/wk
  - [ ] Friday — TargetJobs: build undergraduate profile, set "Data Analyst Placements" filters (unverified)
- [x] **Week 2 — Git & GitHub** (CMD, Git, Boot.dev, GitHub, TargetConnect): `git init`, `git status`, staging and commits; daily push snapshots; 28–35 h/wk
  - [ ] Friday — TargetConnect: authenticate credentials, sector notifications, career-fair dates (unverified)
- [x] **Week 3 — Object properties & conditionals** (Coddy.tech, Códex, VS Code, GitHub, FutureLearn): typecasting logic, `if/elif/else` conditional trees evaluating console hardware configurations; 28–35 h/wk
  - [ ] Friday — FutureLearn: short business analytics course (unverified)
- [x] **Week 4 — Loops & state control** (Coddy.tech, W3Schools, VS Code, GitLab, TargetJobs): `for`/`while`, control breaks, range variations, index bounds, nested loop automation scripts; 28–35 h/wk
  - [ ] Friday — CV infrastructure: highlight active daily commits on resume (unverified)

---

### Phase 2: Data Structures & Algorithmic Logic (Jun 29 – Jul 26)

- [x] **Week 5 — Data collection models** (Coddy.tech, W3Schools, VS Code, GitHub, The Forage): lists, dictionaries, tuples, sets with multi-level key lookups; in-memory catalog of 85 sports/racing games; 28–35 h/wk
  - [ ] Friday — Forage: profile setup, Data Analytics virtual internships (unverified)
- [x] **Week 6 — Functional abstraction** (Coddy.tech, VS Code, GitLab, The Forage): `def` functions, arguments, returns, local/global scope; refactor loops into a reusable search utility; 28–35 h/wk
  - [ ] Friday — Forage: virtual simulation modules, spreadsheet cleaning and client summaries (unverified)
- [ ] **Week 7 — Algorithmic node charts** (GetCracked.io, Roadmap.sh, VS Code, GitHub, The Forage): Roadmap.sh (AI / Data Scientist) traversal workflows; GetCracked.io "Easy" Arrays & Sorting challenges on a 30-minute timer (unverified)
  - [ ] Friday — Forage: complete corporate tasks, extract verified certificate (unverified)
- [x] **Week 8 — Indexing & Big O** (GetCracked.io, W3Schools, VS Code, GitLab, Highered): quick-lookup hash architectures, manual loop-speed tracing, markdown documentation profiles; 28–35 h/wk
  - [ ] Friday — Highered: international student hub setup + target sector filters (unverified)

---

### Phase 3: OOP & Data Analytics (Jul 27 – Aug 23)

- [x] **Week 9 — OOP patterns** (Coddy.tech, VS Code, GitHub, TargetConnect): `__init__` constructors, object state attributes, class inheritance; base `Media` class with custom-flag subclasses; 28–35 h/wk
  - [ ] Friday — TargetConnect: submit resume layout to Careers team for critique (unverified)
- [x] **Week 10 — File I/O & NumPy** (W3Schools, Windows CMD, VS Code, GitHub, TargetJobs): `with open` filesystem interaction, `pip install numpy`, text logs into multi-dimensional matrix files; 28–36 h/wk
  - [ ] Friday — TargetJobs: document entry parameters and calendars of top 15 insight-track firms (unverified)
- [x] **Week 11 — Pandas DataFrames** (365 Data Science, VS Code, GitHub, Highered): Data Analyst Track; CSV game inventory ingest with `.loc`/`.iloc` slices; 28–35 h/wk
  - [ ] Friday — Highered: networking panels, virtual forums, remote events (unverified)
- [x] **Week 12 — Data cleaning & grouping** (365 Data Science, W3Schools, VS Code, GitLab): missing variables, `.groupby()` statistics; `feature-analytics` experiment branch merged back; 28–35 h/wk
  - [ ] Friday — Ecosystem alignment: finalise resume from feedback, anchor GitHub/GitLab links (unverified)

---

### Phase 4: Industrial Capstone (Aug 24 – Sep 13)

- [x] **Week 13 — Pipeline ingestion** (ProjectPro, Roadmap.sh, VS Code, Git, TargetJobs): enterprise file-tree layouts, ingestion layers trapping broken cells and dropping duplicate files; 28–35 h/wk
  - [ ] Friday — Live Application Wave 1: Spring Insight / Winter placement early-bird submissions (unverified)
- [x] **Week 14 — Transformation & ML/AI paths** (ProjectPro, Windows CMD, VS Code, GitHub): statistical matrix queries on cleaned dataframes, auto-export report sheets, Roadmap.sh ML / AI Paths; 28–35 h/wk
  - [ ] Friday — Live Application Wave 2: Summer 2027 Data Analyst internship applications (unverified)
- [x] **Week 15 — Production README & final sync** (365 Data Science, VS Code, GitHub, GitLab, Highered): API documentation and markup design; compose production-grade README; final GitHub/GitLab sync; 25–30 h/wk
  - [ ] Friday — Final profile sync: LinkedIn, Highered, TargetConnect audit (unverified)

---

## Project Architecture

```text
Data-Science-Project/
│
├── .vscode/                                # IDE local runtime environment configuration
│
├── Data/                                   # Storage layer for project datasets and tracking assets
│   └── Sandbox/                            # Storage folder containing raw pipeline source data (e.g., aim.csv)
│
├── HTMLCov/                                # Generated pytest HTML coverage report (gitignored build artefact)
│
├── PostgreSQL/                             # Analytical relational database management scripts
│   └── Sandbox/                            # Database workspace housing schemas, migrations, and query scripts (e.g., aim.sql)
│
├── Python/                                 # Main Python development and modelling architectures
│   ├── Advanced Projects/                  # Applied capstone builds combining core libraries with data and UI automation
│   │   ├── Machine Learning/               # Supervised learning experiments over curated public datasets
│   │   │   ├── Data Outliers/              # Outlier-capping (IQR) detection experiment with report notebooks
│   │   │   ├── Music/                      # Music recommendation model with accuracy, prediction, and visualisation workflows
│   │   │   └── Video Games/                # Video-game sales recommender with hypothesis, IQR, and per-region prediction analysis
│   │   │
│   │   ├── Music Player/                   # Standalone audio players exposing GUI and terminal (TUI) interfaces
│   │   │   ├── GUI/                        # Graphical MP3 and WAV playback interface variants
│   │   │   └── TUI/                        # Terminal MP3 and WAV playback interface variants
│   │   │
│   │   └── Transactions/                   # Excel workbook automation and bar-chart report generation
│   │
│   ├── Functional Programming/             # Pure functions, mathematical pipelines, and immutable data flows
│   │   ├── Fundamental Topics/             # Higher-order transforms: filter, lambda, map, and zip
│   │   └── Syntax Fundamentals/            # Data-pipeline demos: grade summary, number pipeline, shopping receipt, word frequency
│   │
│   ├── Imperative Programming/             # Procedural logic scripts focused on mutable state and step-by-step execution
│   │   ├── Unit & Format Converters/       # Unit and number-format conversion utility scripts
│   │   ├── Fundamental Topics/             # Implementation playgrounds for native collection types, modules, and error handling
│   │   ├── Interactive Games/              # Interactive terminal games testing state tracking and algorithmic logic loops
│   │   ├── Math & Science Calculators/     # Financial models, geometry calculators, and coordinate boundary systems
│   │   └── Syntax Exercises/               # Language syntax scratchpads exploring file I/O operations, string manipulation, and timers
│   │
│   ├── Object Oriented Programming/        # State-driven architectures using classes, encapsulation, and custom domain models
│   │   ├── Fundamental Topics/             # Implementation of abstraction, inheritance, polymorphism, and nested classes
│   │   └── Syntax Fundamentals/            # Domain models including Car, Person, Point, and Dice with custom TUI graphics
│   │
│   └── Sandbox/                            # Primary Python workspace housing unified ingestion and execution scripts (e.g., aim.py)
│
├── Roadmap/                                # Data Science and Python learning-path reference guides (PDF/TXT)
│
├── Scripts/                                # Interactive project-tree / per-folder benchmark runner (execution_time.py)
│
├── Tests/                                  # Pytest unit-testing framework validating mathematical logic and code stability
│   ├── Test Functional Programming/        # Test suites verifying deterministic, side-effect-free data transformations
│   ├── Test Imperative Programming/        # Test suites validating procedural state changes, conditional loops, and user I/O logic
│   ├── Test Object Oriented Programming/   # Verification of object lifecycles, attribute states, and mocked dependencies
│   ├── Test Advanced Projects/             # Coverage for sklearn IQR capping, openpyxl discount pipelines, and music players (mocked pygame/tkinter)
│   ├── Test Scripts/                       # Unit tests for the interactive project-tree benchmark in scripts/
│   └── Test University Courseworks/        # Headless unit tests for the transposed CS1IP Python coursework under University Courseworks/
│
├── University Courseworks/                 # Official university module briefings and transposed coursework
│   ├── Year 1/                             # CS1 briefings (AC, CA, DB, IP, MA, OP) plus translated CS1IP coursework
│   │   └── CS1IP/                          # Java coursework transposed into Python pairs
│   │       ├── Coursework 1/               # hello, ice_cream, volume, seven_segment, average_grades (Java ↔ Python)
│   │       └── Coursework 2/               # sort_comparison with partial and full sorted-dataset exports
│   │
│   ├── Year 2/                             # CS2 briefings (DA, AI, ON, PP, SD, SE) plus the CS2PP module roadmap
│   │
│   └── Year 3/                             # Year 3 briefing documents
│
├── .gitattributes                          # Repository-level line-ending (CRLF) and diff/merge attribute policies for consistent checkout handling
├── .gitignore                              # Multilayer safety network blocking binary artefacts, database dumps, and environment variables
├── .gitkeep                                # Version control placeholder file preserving empty directory architecture in Git
├── AGENTS.md                               # Local AI-agent operating rules: commit conventions, mirror workflow, and project rules for collaborators
├── DEPENDENCIES.md                         # Tiered dependency catalogue separating all-rounder libraries from Windows dev kits
├── LICENSE                                 # MIT legal framework outlining permissions, open-source compliance, and liability limits
├── NOTES.md                                # Comprehensive engineering journal tracking milestone phases, study tracks, and resources
├── pyproject.toml                          # Central project configuration for build tools, test runners, and strict linters (Ruff/Black)
├── README.md                               # Master structural roadmap, technical documentation, and portfolio overview
├── requirements-win_dev.in                 # Direct Windows Dev Kits source list (compiles to requirements-win_dev.txt)
├── requirements-win_dev.txt                # Frozen Windows Dev Kits dependency set (generated by requirements_sync.py)
├── requirements.in                         # Direct All-Rounder library source list (compiles to requirements.txt)
├── requirements.txt                        # Frozen All-Rounder dependency set (generated by requirements_sync.py)
└── requirements_sync.py                    # One-command offline sync + audit: regenerates both frozen files from the live venv
```

---

## References

- [1]: CLI Environment: Navigation and script execution via PowerShell/CMD and Linux/Ubuntu workflows.
- [2]: Version Control: Repository sync via GitHub, GitLab, and VS Code, supported by Git Bash CLI.
- [3]: IDE Setup (`.vscode/`): Debugger paths (`launch.json`), settings (`settings.json`), and build tasks (`tasks.json`).
- [4]: Build & Compliance: Tool setup in `pyproject.toml`, .`gitignore` data protection, and MIT LICENSE terms.
- [5]: Imperative Programming: Syntax, datatypes, control flow, functions, LEGB scope, error handling, and `main` entry guards.
- [6]: OOP Architecture (`fundamental_topics/`): Classes, abstraction, inheritance, polymorphism, encapsulation, nested classes, types of class methods and constructors.
- [7]: Functional Programming: Pure functions, mathematical data processing, and immutable data flow pipelines.
- [8]: Data Converters: Conversions for rates, temperatures, phone numbers, Roman numerals, time, and weights.
- [9]: CLI Games: Interactive terminal games including Dice (TUI), Hangman, Quiz, RPS, and Word Guessing.
- [10]: Maths & Fintech: Geometry, trigonometry, interest/debt calculators, and a TUI banking application.
- [11]: Syntax Utilities: Standalone scripts covering File I/O, timers, factorials, ciphers, and walrus operators.
- [12]: OOP Models (`syntax_fundamentals/`): Domain models including `car.py`, `person.py`, `point.py`, and `dice.py` with custom TUI graphics.
- [13]: University Courseworks: Translated CS1IP coursework including `Average Grades`, `Seven Segment`, and `Volume` logic.
- [14]: Machine Learning: Recommendation models for Music and Video Games using `.csv`, `.dot`, and `.joblib` assets.
- [15]: Excel Automation: Scripting (`transactions.py`) for processing Excel sheets and generating bar chart outputs.
- [16]: Multi-Language Layer: Raw CSV data pipelines and PostgreSQL database schemas.
- [17]: Pytest Framework: Unit tests under `tests/` mirroring imperative, OOP, and functional Python paradigms.
- [18]: Data Safety: The `[Dd]ata/` rule in `.gitignore` protects both uppercase and lowercase data tracks.
- [19]: Open Source: MIT legal framework chosen for repository distribution compliance.
- [20]: Legal Terms: Standard permissions, copyright notices, and liability limits under open-source licensing.
- [21]: Roadmap Guides: Data Science and Python learning-path references (`.pdf` / `.txt`) under `Roadmap/`, guiding the study phases.
- [22]: Advanced Projects: ML experiments (`Machine Learning/`), media-playback interfaces (`Music Player/`), and Excel automation (`Transactions/`).
- [23]: Courseworks Archive: Year 1–3 module briefings and the Java-to-Python CS1IP transposition pairs under `University Courseworks/`.
- [24]: Dependencies: Tiered environment catalogue (`DEPENDENCIES.md`) splitting cross-platform All-Rounder libraries (`requirements.in`/`requirements.txt`) from Windows Dev Kits (`requirements-win_dev.in`/`requirements-win_dev.txt`).

---


