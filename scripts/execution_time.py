import sys
import time
import subprocess
from pathlib import Path

# Ensure UTF-8 console output so tree glyphs (├ └ │) render on Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

PROJECT_ROOT = Path(r"C:\Users\A.I.M\C.S\Data-Science-Project")

# Generated / vendored folders and files skipped in the tree display (and never benchmarked)
TREE_SKIP = {".git", ".venv", ".pytest_cache", "__pycache__", ".coverage", "htmlcov"}


def execute_project_scripts(target_directory):
    base_path = Path(target_directory)

    # Recursively find all python files in the directory
    py_files = list(base_path.rglob("*.py"))

    results = []
    start_time_total = time.perf_counter()

    for file_path in py_files:
        # Extract relative path (e.g. python\imperative_programming\...) for clean display
        try:
            rel_path = file_path.relative_to(base_path.parent)

        except ValueError:
            rel_path = file_path.name

        start_time_file = time.perf_counter()

        try:
            # Execute the file.
            # timeout = 2 is crucial to prevent scripts with input() loops from freezing the execution.
            process = subprocess.run(
                ["python", str(file_path)],
                capture_output=True,
                text=True,
                timeout=2
            )

            status = "PASS" if process.returncode == 0 else "FAIL"

        except subprocess.TimeoutExpired:
            status = "TIMEOUT"  # Flags interactive files requiring user input

        except Exception:
            status = "ERROR"  # Flags unexpected errors during execution

        end_time_file = time.perf_counter()
        exec_time = end_time_file - start_time_file

        results.append((str(rel_path), status, exec_time))

    end_time_total = time.perf_counter()
    total_time = end_time_total - start_time_total

    # Generate Pytest-style ASCII Table
    print("\n" + "=" * 60 + " execution report " + "=" * 60)
    print(f"{'Name':<105} {'Status':<15} {'Time'}")
    print("-" * 138)

    for name, status, t in results:
        print(f"{name:<105} {status:<15} {t:>6.3f}s")

    print("-" * 138)
    print(f"TOTAL FILES: {len(results):<93} TOTAL TIME: {total_time:.2f}s")
    print("=" * 138 + "\n")


def print_directory_tree(base, prefix=""):
    """
    mirror of `tree /f`: directories end with a backslash, files are shown
    plainly, and generated/vendored paths in TREE_SKIP are omitted.
    """
    try:
        entries = sorted(
            (e for e in base.iterdir() if e.name not in TREE_SKIP),
            key=lambda e: (e.is_file(), e.name.lower()),
        )
    except OSError:
        return

    for index, entry in enumerate(entries):
        is_last = index == len(entries) - 1
        connector = "└── " if is_last else "├── "
        suffix = "\\" if entry.is_dir() else ""

        print(prefix + connector + entry.name + suffix)

        if entry.is_dir():
            extension = "    " if is_last else "│   "
            print_directory_tree(entry, prefix + extension)


def resolve_folder(choice):
    target = Path(choice.strip().strip("\\"))

    if not target.is_absolute():
        target = PROJECT_ROOT / target

    if target.is_dir():
        return target

    # Fallback: allow typing just a folder name shown in the tree
    matches = sorted(
        p for p in PROJECT_ROOT.rglob("*")
        if p.is_dir() and p.name.lower() == target.name.lower()
    )
    if len(matches) == 1:
        return matches[0]

    if len(matches) > 1:
        print(f"[!] '{target.name}' matches multiple folders:")
        for match in matches:
            print(f"    - {match}")
        print("Type the full path for the folder you want.")

    return None


def main():
    if "--all" not in sys.argv:
        print(f"\nFolder tree of '{PROJECT_ROOT}':\n")
        print(PROJECT_ROOT)
        print_directory_tree(PROJECT_ROOT)

    while True:
        if "--all" in sys.argv:
            target = PROJECT_ROOT / "python"
        else:
            choice = input(
                "\nFolder to run (e.g. python\\imperative_programming\\syntax_exercises, "
                "or press Enter to run the whole python/ folder, or 'quit'): "
            ).strip()

            if choice.lower() in {"quit", "exit", "q"}:
                print("\nExiting.")
                break

            target = PROJECT_ROOT / "python" if not choice else resolve_folder(choice)

            if target is None:
                continue

        print(f"\n>>> The folder '{target}' is currently running...")
        execute_project_scripts(target)

        if "--all" in sys.argv:
            break


if __name__ == "__main__":
    main()

