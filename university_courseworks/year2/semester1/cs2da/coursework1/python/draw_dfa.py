"""
Generate a GraphViz .dot file from a DFA transition function (Task 2).
"""

DEFAULT_SYMBOLS = "abcdefghijklmnopqrstuvwxyz"


def generate_dot(delta, accepting, symbols=None):
    """
    Return the .dot source for the DFA described by delta/accepting.

    delta: list of Q rows, each a list of S ints (-1 means undefined).
    accepting: list of Q bools.
    symbols: optional string of length S; defaults to first S letters.
    """
    q_count = len(delta)
    s_count = len(delta[0]) if q_count else 0
    
    if symbols is None:
        symbols = DEFAULT_SYMBOLS[:s_count]
    
    if len(symbols) != s_count:
        raise ValueError("symbols length must match alphabet size")

    lines = []
    lines.append("digraph DFA {")
    lines.append("    rankdir=LR;")
    lines.append("    node [shape=circle, fontname=\"Helvetica\"];")
    lines.append("    edge [fontname=\"Helvetica\"];")
    lines.append("")
    lines.append("    start [shape=point];")
    lines.append("    start -> q0;")
    lines.append("")
    
    for q in range(q_count):
        if accepting[q]:
            lines.append(f"    q{q} [shape=doublecircle];")
    
    if any(accepting):
        lines.append("")
    
    for q in range(q_count):
        for a in range(s_count):
            target = delta[q][a]
    
            if target != -1:
                lines.append(f'    q{q} -> q{target} [label="{symbols[a]}"];')
    
    lines.append("}")
    return "\n".join(lines) + "\n"

def main():
    # Personalised DFA for student number 34001219.
    delta = [
        [1, -1, -1],
        [2, 1, 0],
        [-1, 0, 0],
    ]
    accepting = [False, False, True]
    print(generate_dot(delta, accepting), end="")

if __name__ == "__main__":
    main()

