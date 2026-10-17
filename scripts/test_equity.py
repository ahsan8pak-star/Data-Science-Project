"""
Measure test-equity across the python/ portfolio.

A module is not "well tested" because it has N tests; it is well tested when
the tests it has are in proportion to what the module actually does.  Equal
counts per file are the wrong target, because a 200-line calculator and a
5-line helper do not deserve the same effort.  The right target is a
consistent ratio of tests (and the guards inside them) to the module's
behavioural surface, plus coverage of the full input/output range.

Nothing here writes a score and nothing is pinned.  It measures what is on
disk today - the surface of every tracked module and the cases/guards that
reference it - and reports the distribution so a human can see which modules
are over- or under-proportioned.  The companion guard
(tests/test_scripts/test_test_equity.py) turns the equity and full-range
checks into failures.

Surface (the denominator) is a composite of four things the user named:
  * methods     - functions + class methods
  * attributes  - attributes used, class attributes, module globals
  * commands    - distinct command categories the module invokes (io_in,
                  io_out, file, sleep, random, math, subprocess, network,
                  lib, other)
  * io          - input points + output points

Tests (the numerator) are pytest cases plus the guard assertions inside
them (assert / pytest.raises / pytest.warns), attributed to a module by
resolving the FILE/FOLDER constants and path literals a test class or
function actually uses.
"""

import ast
import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PYTHON_ROOT = REPO_ROOT / "python"
TESTS_ROOT = REPO_ROOT / "tests"

THIRD_PARTY = {
    "numpy", "pandas", "sklearn", "matplotlib", "seaborn", "pygame",
    "openpyxl", "joblib", "PIL", "tkinter", "sqlite3", "requests",
    "scipy", "plotly", "xgboost", "torch", "tensorflow", "pydub", "bs4",
}


def _tracked_modules():
    out = subprocess.run(
        ["git", "ls-files", "python"], cwd=REPO_ROOT,
        capture_output=True, text=True, check=True,
    ).stdout.split()
    return [m for m in out if m.endswith(".py") and not m.endswith("__init__.py")]


def _module_stem(rel):
    return Path(rel).stem


def _command_category(call):
    func = call.func
    if isinstance(func, ast.Name):
        name = func.id
        if name == "input":
            return "io_in"
        if name == "print":
            return "io_out"
        if name == "open":
            return "file"
        return None
    if isinstance(func, ast.Attribute):
        attr = func.attr
        obj = func.value
        obj_name = obj.id if isinstance(obj, ast.Name) else None
        if attr in {"read", "readlines", "read_text", "read_bytes", "readline",
                    "write", "writelines", "write_text", "write_bytes"}:
            return "file"
        if attr == "sleep":
            return "sleep"
        if obj_name == "random" or attr in {"choice", "randint", "random", "shuffle"}:
            return "random"
        if obj_name == "math" or attr in {"sqrt", "pow", "sin", "cos", "tan", "log"}:
            return "math"
        if obj_name in {"subprocess", "os"} and attr in {"system", "run", "popen", "call"}:
            return "subprocess"
        if obj_name in {"requests", "urllib"}:
            return "network"
        if obj_name in THIRD_PARTY:
            return "lib"
        return "other"
    return None


def module_surface(path):
    try:
        source = path.read_bytes().replace(b"\r\n", b"\n").decode("utf-8")
    except (UnicodeDecodeError, OSError):
        return None
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return None

    functions = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    classes = [n for n in tree.body if isinstance(n, ast.ClassDef)]
    methods = []
    for cls in classes:
        methods.extend(n for n in cls.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)))

    attrs_used = {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)}
    class_attrs = 0
    for cls in classes:
        for node in cls.body:
            if isinstance(node, ast.Assign):
                class_attrs += sum(1 for t in node.targets if isinstance(t, ast.Name))
    module_globals = 0
    for node in tree.body:
        if isinstance(node, ast.Assign):
            module_globals += sum(1 for t in node.targets if isinstance(t, ast.Name))

    cats = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            c = _command_category(node)
            if c:
                cats.add(c)
    libs_used = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                libs_used.add(a.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            libs_used.add(node.module.split(".")[0])
    libs_used = libs_used & THIRD_PARTY
    if libs_used:
        cats.add("lib")

    input_calls = sum(
        1 for n in ast.walk(tree)
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "input"
    )
    output_calls = sum(
        1 for n in ast.walk(tree)
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "print"
    )
    file_writes = sum(
        1 for n in ast.walk(tree)
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "open"
    )
    outputs = output_calls + file_writes

    methods_n = len(functions) + len(methods)
    attributes_n = len(attrs_used) + class_attrs + module_globals
    commands_n = len(cats) if cats else 1
    io_n = input_calls + outputs

    surface = methods_n + attributes_n + commands_n + io_n
    if surface < 1:
        surface = 1

    return {
        "methods": methods_n,
        "attributes": attributes_n,
        "command_types": commands_n,
        "command_categories": sorted(cats),
        "third_party_libs": sorted(libs_used),
        "inputs": input_calls,
        "outputs": outputs,
        "io_pairs": io_n,
        "surface": surface,
    }


def _test_files():
    out = []
    for p in TESTS_ROOT.rglob("test_*.py"):
        out.append(p)
    for p in (REPO_ROOT / "university_courseworks").rglob("test_*.py"):
        out.append(p)
    return sorted(set(out))


def _source_stems():
    return {_module_stem(m): m for m in _tracked_modules()}


def _resolve_constants(tree, parent_scope=None):
    """Resolve simple module/class-level constants into a dict."""
    scope = dict(parent_scope or {})
    # iterate to fixpoint
    changed = True
    # collect assignments
    assigns = []
    for node in tree.body if hasattr(tree, "body") else []:
        if isinstance(node, ast.Assign):
            assigns.append(node)
    # repeat passes
    remaining = list(assigns)
    progress = True
    while progress and remaining:
        progress = False
        still = []
        for node in remaining:
            if len(node.targets) != 1 or not isinstance(node.targets[0], ast.Name):
                still.append(node)
                continue
            name = node.targets[0].id
            # try to eval
            try:
                code = compile(ast.Expression(node.value), "<const>", "eval")
                val = eval(code, {"__builtins__": {}}, scope)
                scope[name] = val
                progress = True
            except Exception:
                still.append(node)
        remaining = still
    return scope


def _resolve_file_path(cls_node, module_scope):
    """Resolve a class's FILE constant (possibly f-string referencing FOLDER)."""
    class_scope = dict(module_scope)
    _resolve_constants(cls_node, class_scope)
    # FILE may be built from FOLDER
    if "FILE" in class_scope and isinstance(class_scope["FILE"], str):
        return class_scope["FILE"]
    # try common patterns
    for attr in ("FILE", "file", "PATH", "path"):
        if attr in class_scope and isinstance(class_scope[attr], str):
            return class_scope[attr]
    return None


def _count_asserts(func_node):
    n = 0
    for node in ast.walk(func_node):
        if isinstance(node, ast.Assert):
            n += 1
        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if isinstance(ctx, ast.Call):
                    f = ctx.func
                    name = f.attr if isinstance(f, ast.Attribute) else (f.id if isinstance(f, ast.Name) else None)
                    if name in {"raises", "warns", "deprecated_call", "raises_strict"}:
                        n += 1
    return n


def _load_conftest_scope(test_file_path):
    """Resolve string constants from conftest.py files up the directory tree."""
    scope = {}
    cur = test_file_path.parent
    roots = []
    while True:
        roots.append(cur)
        if cur == TESTS_ROOT or cur == REPO_ROOT or cur.parent == cur:
            break
        cur = cur.parent
    for d in reversed(roots):
        cf = d / "conftest.py"
        if cf.is_file():
            try:
                ctree = ast.parse(cf.read_bytes().replace(b"\r\n", b"\n").decode("utf-8"))
            except SyntaxError:
                continue
            new = _resolve_constants(ctree, scope)
            scope.update(new)
    return scope


def _test_functions_in_file(path, stem_to_rel):
    try:
        source = path.read_bytes().replace(b"\r\n", b"\n").decode("utf-8")
    except (UnicodeDecodeError, OSError):
        return []
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []
    module_scope = _load_conftest_scope(path)
    module_scope = _resolve_constants(tree, module_scope)

    # direct imports: from x.y.z import ... -> module
    imported_modules = set()
    file_refs = _refs_from_segment(source, stem_to_rel)
    for node in tree.body:
        if isinstance(node, ast.ImportFrom) and node.module:
            parts = node.module.split(".")
            # find which tracked module stem matches last part
            for stem, rel in stem_to_rel.items():
                if parts and parts[-1] == stem:
                    imported_modules.add(rel)
        elif isinstance(node, ast.Import):
            for a in node.names:
                parts = a.name.split(".")
                for stem, rel in stem_to_rel.items():
                    if parts and parts[-1] == stem:
                        imported_modules.add(rel)

    results = []  # list of (func_name, referenced_rel_set, asserts)
    # module-level test functions
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test_"):
            seg = ast.get_source_segment(source, node) or ""
            refs = _resolve_refs_from_function(node, seg, module_scope, stem_to_rel, imported_modules)
            if not refs and file_refs:
                refs = set(file_refs)
            results.append((node.name, refs, _count_asserts(node)))

    # classes
    for cls in tree.body:
        if not isinstance(cls, ast.ClassDef):
            continue
        class_scope = _resolve_constants(cls, module_scope)
        file_path = class_scope.get("FILE") or class_scope.get("file") or class_scope.get("PATH") or class_scope.get("path")
        cls_refs = set()
        if isinstance(file_path, str):
            cand = file_path.replace("\\", "/")
            for stem, rel in stem_to_rel.items():
                if Path(rel).name == Path(cand).name or Path(rel).stem == Path(cand).stem:
                    cls_refs.add(rel)
        # scan class body text for path literals / stems
        cls_seg = ast.get_source_segment(source, cls) or ""
        cls_refs |= _refs_from_segment(cls_seg, stem_to_rel)

        for node in cls.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test_"):
                seg = ast.get_source_segment(source, node) or ""
                if cls_refs:
                    refs = set(cls_refs)
                else:
                    refs = _resolve_refs_from_function(node, seg, class_scope, stem_to_rel, imported_modules)
                if not refs and imported_modules and len(imported_modules) == 1:
                    refs = set(imported_modules)
                if not refs and file_refs:
                    refs = set(file_refs)
                results.append((node.name, refs, _count_asserts(node)))
    return results, source, imported_modules


def _refs_from_segment(seg, stem_to_rel):
    refs = set()
    # path literals
    for m in re.finditer(r"[\"']([A-Za-z0-9_./\\-]+\.py)[\"']", seg):
        cand = m.group(1).replace("\\", "/")
        base = Path(cand).name
        for stem, rel in stem_to_rel.items():
            if Path(rel).name == base:
                refs.add(rel)
    # direct module path literals like "folder/file.py" already handled by basename
    # stem tokens
    for stem, rel in stem_to_rel.items():
        if len(stem) < 5:
            continue
        if stem in {"main", "area", "volume", "point", "food", "order", "person",
                    "school", "sports", "worker", "device", "dice", "payment", "item",
                    "car", "calculator"}:
            continue
        if re.search(r"\b" + re.escape(stem) + r"\b", seg):
            refs.add(rel)
    return refs


def _value_matches_module(val, stem_to_rel):
    """If val is a str naming a tracked module, return that rel path."""
    if not isinstance(val, str):
        return None
    cand = val.replace("\\", "/")
    base = Path(cand).name
    for stem, rel in stem_to_rel.items():
        if Path(rel).name == base or Path(rel).stem == Path(cand).stem:
            return rel
    # stem substring
    for stem, rel in stem_to_rel.items():
        if len(stem) >= 5 and stem in cand:
            return rel
    return None


def _resolve_refs_from_function(func_node, seg, scope, stem_to_rel, imported_modules):
    refs = set()
    # 1. path literals / stem tokens in the function source
    refs |= _refs_from_segment(seg, stem_to_rel)
    # 2. constants referenced by name in the function body
    for node in ast.walk(func_node):
        if isinstance(node, ast.Name) and node.id in scope:
            rel = _value_matches_module(scope[node.id], stem_to_rel)
            if rel:
                refs.add(rel)
    # 3. single-import fallback
    if not refs and imported_modules and len(imported_modules) == 1:
        refs = set(imported_modules)
    return refs


def _refs_from_segment_and_scope(seg, cls_scope, module_scope, stem_to_rel, imported_modules):
    refs = _refs_from_segment(seg, stem_to_rel)
    if not refs and imported_modules and len(imported_modules) == 1:
        refs = set(imported_modules)
    return refs


def measure():
    modules = _tracked_modules()
    stem_to_rel = _source_stems()

    surfaces = {}
    for rel in modules:
        s = module_surface(REPO_ROOT / rel)
        if s is not None:
            surfaces[rel] = s

    stats = defaultdict(lambda: {"cases": 0, "guards": 0, "test_files": set(), "categories_seen": set()})
    unattributed_cases = 0
    unattributed_guards = 0

    for tf in _test_files():
        funcs, source, imported = _test_functions_in_file(tf, stem_to_rel)
        if not funcs:
            continue
        for name, refs, asserts in funcs:
            if not refs:
                unattributed_cases += 1
                unattributed_guards += asserts
                continue
            for rel in refs:
                stats[rel]["cases"] += 1
                stats[rel]["guards"] += asserts
                stats[rel]["test_files"].add(str(tf.relative_to(REPO_ROOT)))
                # categories seen: scan segment not available here; re-scan source for the func name? skip for now
                # We'll fill categories_seen from the module's own categories as a proxy (full range checked separately)

    # fill categories_seen by re-scanning test file source for command-category keywords per module (best-effort):
    # For full-range, check that each module's command categories appear as substrings in at least one referencing test file.
    module_test_text = defaultdict(str)
    for tf in _test_files():
        try:
            txt = tf.read_bytes().replace(b"\r\n", b"\n").decode("utf-8")
        except Exception:
            continue
        # attribute file text to modules it references
        file_refs = _refs_from_segment(txt, stem_to_rel)
        for rel in file_refs:
            module_test_text[rel] += "\n" + txt

    # Second pass: credit test files whose classes resolve a FILE constant to a
    # module, even when no stem token appears in the file text.
    for tf in _test_files():
        try:
            txt = tf.read_bytes().replace(b"\r\n", b"\n").decode("utf-8")
            tree = ast.parse(txt)
        except Exception:
            continue
        module_scope = _resolve_constants(tree, {})
        for cls in tree.body:
            if not isinstance(cls, ast.ClassDef):
                continue
            cscope = _resolve_constants(cls, module_scope)
            fp = cscope.get("FILE") or cscope.get("file")
            if not isinstance(fp, str):
                continue
            for stem, rel in stem_to_rel.items():
                if Path(rel).name == Path(fp).name:
                    module_test_text[rel] += "\n" + txt

    report = {}
    densities = []
    for rel in modules:
        s = surfaces.get(rel)
        if s is None:
            continue
        st = stats.get(rel, {"cases": 0, "guards": 0, "test_files": set(), "categories_seen": set()})
        cases = st["cases"]
        guards = st["guards"]
        total_tests = cases + guards
        density = total_tests / s["surface"] if s["surface"] else 0.0
        # full range: module's command categories must appear in referencing tests' text
        ttext = module_test_text.get(rel, "").lower()
        missing_cats = [c for c in s["command_categories"] if c not in ttext]
        full_range_ok = cases > 0
        if s["inputs"] > 0:
            full_range_ok = full_range_ok and ("input" in ttext)
        if s["outputs"] > 0:
            full_range_ok = full_range_ok and (guards > 0)
        if cases > 0 and guards == 0:
            full_range_ok = False
        report[rel] = {
            "surface": s,
            "tests": {"cases": cases, "guards": guards, "total": total_tests},
            "density": round(density, 4),
            "test_files": sorted(st["test_files"]),
            "missing_command_categories_in_tests": missing_cats,
            "full_range_ok": full_range_ok,
        }
        if cases > 0:
            densities.append(density)

    import statistics
    if densities:
        mean = statistics.mean(densities)
        stdev = statistics.pstdev(densities) if len(densities) > 1 else 0.0
        cv = (stdev / mean) if mean else 0.0
        mn = min(densities)
        mx = max(densities)
        ratio = (mx / mn) if mn > 0 else float("inf")
    else:
        mean = stdev = cv = mn = mx = ratio = 0.0

    zero_test_modules = [r for r in report if report[r]["tests"]["cases"] == 0]

    summary = {
        "modules_measured": len(report),
        "modules_with_tests": sum(1 for r in report if report[r]["tests"]["cases"] > 0),
        "modules_with_zero_tests": len(zero_test_modules),
        "unattributed_cases": unattributed_cases,
        "unattributed_guards": unattributed_guards,
        "density_mean": round(mean, 4),
        "density_stdev": round(stdev, 4),
        "density_cv": round(cv, 4),
        "density_min": round(mn, 4),
        "density_max": round(mx, 4),
        "density_min_max_ratio": round(ratio, 4) if ratio != float("inf") else None,
        "full_range_failures": sum(1 for r in report if not report[r]["full_range_ok"]),
    }

    out_path = Path("/tmp/opencode/test_equity.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps({"summary": summary, "modules": report}, indent=1), encoding="utf-8")

    print(f"measured {len(report)} modules")
    print(f"  with tests: {summary['modules_with_tests']}  zero-test: {summary['modules_with_zero_tests']}")
    print(f"  unattributed cases: {unattributed_cases}  guards: {unattributed_guards}")
    print(f"  density mean={mean:.4f} stdev={stdev:.4f} cv={cv:.4f} min={mn:.4f} max={mx:.4f} ratio={ratio:.2f}")
    print(f"  full-range failures: {summary['full_range_failures']}")
    ranked = sorted(
        (r for r in report if report[r]["tests"]["cases"] > 0),
        key=lambda r: report[r]["density"],
    )
    print("  lowest density (most under-tested relative to surface):")
    for r in ranked[:8]:
        print(f"    {report[r]['density']:6.3f}  {r}")
    print("  highest density (most over-tested relative to surface):")
    for r in ranked[-5:]:
        print(f"    {report[r]['density']:6.3f}  {r}")
    if zero_test_modules:
        print("  zero-test modules:")
        for r in zero_test_modules[:15]:
            print(f"    {r}")
    print(f"  report -> {out_path}")
    return summary, report


def main():
    summary, report = measure()
    out_path = Path("/tmp/opencode/test_equity.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps({"summary": summary, "modules": report}, indent=1), encoding="utf-8")
    # console summary
    print(f"measured {len(report)} modules")
    print(f"  with tests: {summary['modules_with_tests']}  zero-test: {summary['modules_with_zero_tests']}")
    print(f"  unattributed cases: {summary['unattributed_cases']}  guards: {summary['unattributed_guards']}")
    print(f"  density mean={summary['density_mean']:.4f} stdev={summary['density_stdev']:.4f} cv={summary['density_cv']:.4f} min={summary['density_min']:.4f} max={summary['density_max']:.4f} ratio={summary['density_min_max_ratio']}")
    print(f"  full-range failures: {summary['full_range_failures']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

