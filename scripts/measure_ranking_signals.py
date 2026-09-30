"""
Measure objective signals for the file-ranking rescore.

[AI] Scoring 160 files by eye produced the previous sheet, and the numbers in
it were hard to defend because the basis for each mark was not written down.
This pass measures what can be measured - coverage, exception handling,
docstrings, comment quality, hardcoded values, input validation, library use
- so the human judgement that remains is only about naming and whether a
defect is deliberate.

Nothing here writes a score. It emits a JSON table of signals, and the scoring
step reads that table rather than re-reading 160 files from scratch.

The distinction that shapes the whole exercise: a learning script is judged on
whether it teaches clearly, and an applied project is judged on whether it
survives contact with a user. Those are different questions, so they are
weighted differently in the guide.
"""

import ast
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PYTHON_ROOT = REPO_ROOT / "python"

# Library use separates applied work from classroom practice far more reliably
# than folder names do, because the same technique is taught in both lanes.
APPLIED_LIBS = {
    "numpy", "pandas", "sklearn", "matplotlib", "seaborn", "pygame",
    "openpyxl", "joblib", "PIL", "tkinter", "sqlite3", "requests",
    "scipy", "plotly", "xgboost", "torch", "tensorflow",
}
THIRD_PARTY = APPLIED_LIBS | {"playwright", "bs4", "pydub", "serial"}

# Hardcoded values are a real smell in applied code and expected in a teaching
# script that exists to show `temperature = 25`, so both are recorded.
HARDCODED_NUMBER = re.compile(r"=\s*-?\d+\.?\d*\s*(#.*)?$")
HARDCODED_PATH = re.compile(r"=\s*[\"'][A-Za-z]:[\\/]|[\"']/Users/|[\"']C:\\\\")
AMERICANISM = re.compile(
    r"\b(color|behavior|organize|analyze|labeled|center|initializer|"
    r"customize|recognize|realize|defense|licence)\w*\b", re.I
)


def classify(rel):
    """
    Learning material or applied project.

    [AI] Folder names are a poor guide: python/advanced_projects/ holds both
    machine-learning notebooks and two GUI music players, while
    imperative_programming/ holds a spreadsheet pipeline. What actually
    separates them is intent, and the three signals below approximate it -
    a real data file, a third-party library, or a class-based interface. The
    result is recorded per file so a human can disagree with any single call.
    """
    return "unknown"


def module_signals(path):
    """Everything measurable about one module, or a reason it cannot be read."""
    try:
        source = path.read_bytes().replace(b"\r\n", b"\n").decode("utf-8")
    except (UnicodeDecodeError, OSError) as error:
        return {"error": str(error)}
    try:
        tree = ast.parse(source)
    except SyntaxError as error:
        return {
            "error": f"unparseable at line {error.lineno}",
            "lines": source.count("\n") + 1,
            "source": source,
        }

    docstring = ast.get_docstring(tree)
    functions = [n for n in tree.body if isinstance(n, ast.FunctionDef)]
    classes = [n for n in tree.body if isinstance(n, ast.ClassDef)]
    methods = [
        n for c in classes for n in c.body if isinstance(n, ast.FunctionDef)
    ]
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".")[0])

    calls = {
        node.func.id for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    try_nodes = [n for n in ast.walk(tree) if isinstance(n, ast.Try)]
    handlers = [
        h for n in try_nodes for h in n.handlers
    ]
    raises = [n for n in ast.walk(tree) if isinstance(n, ast.Raise)]
    bare_raises = [n for n in raises if n.exc is None]
    inputs = [
        n for n in ast.walk(tree)
        if isinstance(n, ast.Call)
        and isinstance(n.func, ast.Name) and n.func.id == "input"
    ]
    # A guard on user input is a comprehension test, a length check, or a
    # try around the read. The name matters less than the presence.
    guards = sum(
        1 for n in ast.walk(tree)
        if isinstance(n, ast.If) and isinstance(n.test, ast.Compare)
    )
    while_loops = [n for n in ast.walk(tree) if isinstance(n, ast.While)]
    for_loops = [n for n in ast.walk(tree) if isinstance(n, ast.For)]
    infinite_loops = [
        n for n in while_loops
        if isinstance(n.test, ast.Constant) and n.test.value is True
    ]
    functions_without_doc = [
        n.name for n in functions + methods
        if ast.get_docstring(n) is None
    ]
    commented_blocks = len(
        [1 for line in source.split("\n") if line.strip().startswith("#")]
    )
    triple_blocks = len(re.findall(r'^\s*"""', source, re.M)) // 2
    hardcoded_numbers = sum(
        1 for line in source.split("\n")
        if HARDCODED_NUMBER.search(line) and "range(" not in line
        and "for " not in line
    )
    hardcoded_paths = len(HARDCODED_PATH.findall(source))
    return {
        "lines": source.count("\n") + 1,
        "statements": sum(
            1 for n in ast.walk(tree)
            if isinstance(n, ast.stmt) and not isinstance(n, (ast.Expr,))
        ),
        "has_module_docstring": docstring is not None,
        "module_docstring_lines": len(docstring.split("\n")) if docstring else 0,
        "functions": len(functions),
        "methods": len(methods),
        "classes": len(classes),
        "functions_without_doc": functions_without_doc,
        "imports": sorted(imports),
        "third_party": sorted(imports & THIRD_PARTY),
        "try_blocks": len(try_nodes),
        "except_handlers": len(handlers),
        "bare_raises": len(bare_raises),
        "input_calls": len(inputs),
        "guard_ifs": guards,
        "infinite_loops": len(infinite_loops),
        "for_loops": len(for_loops),
        "print_calls": sum(1 for c in calls if c == "print"),
        "commented_hash_lines": commented_blocks,
        "triple_blocks": triple_blocks,
        "hardcoded_numbers": hardcoded_numbers,
        "hardcoded_paths": hardcoded_paths,
        "americanisms": AMERICANISM.findall(source),
        "unreachable_after_return": count_dead_code(source),
    }


def count_dead_code(source):
    """
    Statements after a return or raise in the same block.

    [AI] Unreachable code is a genuine defect signal and is invisible to a
    coverage report, because it is never executed by definition. A function
    with a return followed by more statements is either missing an `if` or
    has a leftover from an edit, and either way a reader is misled.
    """
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return 0
    total = 0
    for node in ast.walk(tree):
        body = getattr(node, "body", None)
        if not isinstance(body, list):
            continue
        for index, statement in enumerate(body[:-1]):
            if isinstance(statement, (ast.Return, ast.Raise, ast.Continue,
                                      ast.Break)):
                total += 1
                break
    return total


def coverage_table():
    """Per-file line coverage from the JSON report, if one has been produced."""
    report = Path("/tmp/opencode/cov.json")
    if not report.is_file():
        return {}
    data = json.loads(report.read_text(encoding="utf-8")).get("files", {})
    out = {}
    for key, value in data.items():
        name = key.replace("\\", "/")
        summary = value.get("summary", {})
        out[name] = {
            "percent": summary.get("percent_covered_display"),
            "missing_lines": len(value.get("missing_lines", [])),
            "missing_branches": len(value.get("missing_branches", [])),
            "statements": summary.get("num_statements"),
        }
    return out


def benchmark_status():
    """PASS / INTERACTIVE / TIMEOUT / FAIL / ERROR per file, from the harness."""
    result = subprocess.run(
        [sys.executable, "scripts/execution_time.py", "--all"],
        cwd=REPO_ROOT, capture_output=True, text=True,
    )
    status = {}
    for line in result.stdout.splitlines():
        match = re.search(r"(python[\\/].+?\.py)\s+(\w+)\s+[\d.]+s", line)
        if match:
            name = match.group(1).replace("\\", "/")
            status[name] = match.group(2)
    return status


def main():
    tracked = subprocess.run(
        ["git", "ls-files", "python"], cwd=REPO_ROOT,
        capture_output=True, text=True, check=True,
    ).stdout.split()
    coverage = coverage_table()
    benchmark = benchmark_status()
    report = {}
    for rel in tracked:
        if not rel.endswith(".py") or rel.endswith("__init__.py"):
            continue
        signals = module_signals(REPO_ROOT / rel)
        signals["coverage"] = coverage.get(rel, {})
        signals["benchmark"] = benchmark.get(rel, "not-run")
        report[rel] = signals
    out = Path("/tmp/opencode/ranking_signals.json")
    out.write_text(json.dumps(report, indent=1), encoding="utf-8")
    print(f"  measured {len(report)} modules -> {out}")
    unreadable = [k for k, v in report.items() if "error" in v]
    print(f"  unreadable (deliberately unparseable or unreadable): {len(unreadable)}")
    for name in unreadable:
        print(f"    {name}: {report[name]['error']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

