"""
One-off converter: rewrite runs of three or more hash comments as blocks.

[AI-authored fix] House style caps a run of consecutive hash comments at two
lines and requires three or more to become a triple-quoted block, with the
opening and closing quotes alone on their own lines. This script applies that
conversion across the tracked tree so the rule is met everywhere rather than
only in newly written files.

It is deliberately conservative about four things, because each one can
silently change a file's meaning:

  - the comment text is copied verbatim, character for character, apart from
    losing the leading `# ` and its trailing space. No wording is 'improved',
    because these are A.I.M's own notes and rule 2 forbids rewriting them;
  - the block is indented to match the comment it replaces, so it stays
    syntactically valid wherever it appeared;
  - a run whose text contains a triple quote is skipped, since a block cannot
    contain its own delimiter;
  - the frozen OOP lane and the marked CS1IP coursework are never touched,
    because rule 1 and rule 8 protect them from edits of this kind.

The script refuses to run twice over the same file: re-running is a no-op
because the converted block is no longer a hash run.

[AI] Run it from the repo root, review the diff, then delete the script. It
exists to be auditable, not to become part of the project.
"""

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
QUOTE = '"' * 3

# Rule 1 freezes the OOP lane; rule 8 marks the CS1IP coursework as submitted
# work. Neither is ours to restyle, so both are skipped by name.
EXEMPT = {
    "python/object_oriented_programming/fundamental_topics/decorator.py",
    "python/object_oriented_programming/fundamental_topics/generator.py",
    "python/object_oriented_programming/fundamental_topics/multitasking.py",
    "python/object_oriented_programming/fundamental_topics/dice.py",
    "python/object_oriented_programming/fundamental_topics/classes.py",
    "python/object_oriented_programming/fundamental_topics/abstract_classes.py",
    "python/object_oriented_programming/fundamental_topics/nested_classes.py",
    "university_courseworks/year1/semester1/cs1ip/coursework2/python/sort_comparison.py",
}


def tracked_python_files():
    listed = subprocess.run(
        ["git", "ls-files", "*.py"],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout.split()
    return [rel for rel in listed if rel not in EXEMPT]


def find_runs(lines):
    """Yield (start, end) index pairs for hash-comment runs of 3+ lines."""
    run_start = None
    for index, line in enumerate(lines):
        if line.strip().startswith("#"):
            if run_start is None:
                run_start = index
        else:
            if run_start is not None and index - run_start > 2:
                yield run_start, index
            run_start = None
    if run_start is not None and len(lines) - run_start > 2:
        yield run_start, len(lines)


def convert(text):
    lines = text.split("\n")
    out = []
    cursor = 0
    converted = 0
    for start, end in find_runs(lines):
        out.extend(lines[cursor:start])
        block = lines[start:end]
        indent = block[0][:len(block[0]) - len(block[0].lstrip())]
        body = []
        for line in block:
            stripped = line.strip()
            text_part = stripped[1:]
            if text_part.startswith(" "):
                text_part = text_part[1:]
            body.append(text_part)
        # A block cannot contain its own delimiter, so skip rather than mangle.
        if any(QUOTE in entry for entry in body):
            out.extend(block)
        else:
            out.append(f"{indent}{QUOTE}")
            out.extend(f"{indent}{entry}" if entry else "" for entry in body)
            out.append(f"{indent}{QUOTE}")
            converted += 1
        cursor = end
    out.extend(lines[cursor:])
    return "\n".join(out), converted


def main():
    total_files = 0
    total_runs = 0
    for rel in tracked_python_files():
        path = REPO_ROOT / rel
        try:
            original = path.read_bytes().replace(b"\r\n", b"\n").decode("utf-8")
        except UnicodeDecodeError:
            print(f"  skipped (not utf-8): {rel}")
            continue
        if original.endswith("\n\n"):
            body, converted = convert(original.rstrip("\n"))
        else:
            body, converted = convert(original)
        if not converted:
            continue
        try:
            compile(body, str(path), "exec")
        except SyntaxError as error:
            print(f"  REFUSED (would not parse): {rel}: {error}")
            continue
        path.write_bytes(body.encode("utf-8"))
        total_files += 1
        total_runs += converted
    print(f"  converted {total_runs} runs across {total_files} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())

