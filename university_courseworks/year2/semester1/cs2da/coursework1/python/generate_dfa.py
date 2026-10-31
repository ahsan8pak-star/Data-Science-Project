"""
Generate the personalised DFA transition table for CS2DA coursework 1.

Replicates the logic of ``java/GenerateDFA.java`` for student number
34001219, so the coursework can be reproduced without a Java toolchain.
"""

MASK = (1 << 64) - 1


def generate(student_id: int):
    """Return (delta, accepting, initial) for the given student number."""
    id_value = student_id
    hash_value = 5381

    while id_value > 0:
        hash_value = (((hash_value << 5) + hash_value) + (id_value & 255)) & MASK
        id_value = id_value >> 8

    delta = [[-1, -1, -1] for _ in range(3)]
    for q in range(3):
        for a in range(3):
            delta[q][a] = (hash_value & 3) - 1
            hash_value = (hash_value >> 2) & MASK

    # Force connectivity, exactly as in GenerateDFA.java.
    if delta[0][0] != 1 and delta[0][1] != 1 and delta[0][2] != 1:
        delta[0][0] = 1

    if delta[1][0] != 2 and delta[1][1] != 2 and delta[1][2] != 2:
        delta[1][1] = 2

    accepting = [False, False, True]
    initial = 0
    return delta, accepting, initial


def print_table(delta, accepting):
    print("  q |  a |  b |  c")
    print("-------------------")

    for q in range(len(delta)):
        print(f" q{q}", end="")

        for a in range(len(delta[0])):
            if delta[q][a] == -1:
                print(" | --", end="")

            else:
                print(f" | q{delta[q][a]}", end="")
        print()

    print("Accepting states: " + "".join(f" q{q}" for q in range(len(accepting)) if accepting[q]))


def main():
    student_id = 34001219
    sid = str(student_id)

    if sid[:2] != "34" or len(sid) != 8:
        print("WARNING: YOU NEED TO PUT YOUR STUDENT ID IN THE PROGRAM SOURCE CODE.")

    print(f"Student ID: {student_id}")

    print()

    delta, accepting, _ = generate(student_id)
    print_table(delta, accepting)


if __name__ == "__main__":
    main()

