# Dependencies & Environment Catalogue

Every library installed in the project virtual environment (`.venv`, Python 3.14), split into **three tiers** so that the cross-platform code libraries stay separate from the Windows-specific development tooling.

## Classification Rule

| Tier | File(s) | What it means |
| --- | --- | --- |
| **A — Fundamental / All-Rounder** | `requirements.in` → `requirements.txt` | Libraries **imported by project code** (scripts, notebooks, tests). Ship cross-platform wheels, usable on any OS and in any kind of software. |
| **B — Windows Dev Kits** | `requirements-win_dev.in` → `requirements-win_dev.txt` | Tooling that turns this machine into a **development workstation**: notebook/kernel stacks, REPL, type-checker, Windows terminal bridges. |
| **C — Packaging & Build Toolchain** | *(unpinned — managed by pip itself)* | The tools that install, compile, and update Tiers A and B. |

> The compiled `.txt` files are the **complete frozen inventory** (dependency closures, exact pins).
> `DEPENDENCIES.md` documents the *meaningful* (declared) packages per tier; the full transitive
> set for each tier lives in its compiled file (regenerate both with `requirements_sync.py` —
> see **Keeping Requirements Current** below).

---

## Tier A — Fundamental / All-Rounder Libraries

Declared in `requirements.in` (15 packages):

| Library | Pinned | Purpose |
| --- | --- | --- |
| `numpy` | 2.5.2 | Numerical array/matrix core beneath the whole data-science stack |
| `pandas` | 3.0.5 | Tabular `DataFrame`/`Series` analytics |
| `scipy` | 1.18.1 | Scientific computing (stats, linear algebra, optimisation) |
| `scikit-learn` | 1.9.0 | Machine learning (recommenders, `OutlierCapper` transformer, pipelines) |
| `matplotlib` | 3.11.1 | Plotting and figure generation |
| `seaborn` | 0.13.2 | Statistical visualisation on top of matplotlib/pandas |
| `joblib` | 1.6.0 | Model persistence (`.joblib`) and parallel caching |
| `openpyxl` | 3.1.5 | Excel automation (`transactions.py` pipeline) |
| `psycopg2` | 2.9.12 | PostgreSQL driver for the SQL/analytics workflows |
| `requests` | 2.34.2 | HTTP client for scraping and API work |
| `pygame-ce` | 2.5.8 | Community-edition PyGame: alarm clock, TUI/GUI media players |
| `qrcode` | 8.2 | QR-code generation (NOTES.md project list) |
| `pytest` | 9.1.1 | Test runner |
| `pytest-cov` | 7.1.0 | Coverage plugin for pytest |
| `coverage` | 7.16.0 | `coverage[toml]` measurement engine |

**Transitive closure** frozen in `requirements.txt`: `certifi`, `charset-normalizer`, `cloudpickle`, `colorama`, `contourpy`, `cycler`, `et-xmlfile`, `fonttools`, `idna`, `iniconfig`, `kiwisolver`, `narwhals`, `packaging`, `pillow`, `pluggy`, `pygments`, `pyparsing`, `python-dateutil`, `six`, `threadpoolctl`, `tzdata`, `urllib3`.

---

## Tier B — Windows Dev Kits

Declared in `requirements-win_dev.in` (6 packages):

| Library | Pinned | Purpose |
| --- | --- | --- |
| `jupyter` | 1.1.1 | Metapackage: JupyterLab + Notebook + Console + Widgets |
| `ipykernel` | 7.3.0 | Python kernel that executes `.ipynb` notebooks |
| `ipython` | 9.17.1 | Rich interactive REPL |
| `pywinpty` | 3.0.5 | **Windows-only** pseudo-terminal bridge (used by `terminado`/Jupyter) |
| `colorama` | 0.4.6 | ANSI colour codes on the Windows console (IPython + qrcode) |
| `mypy` | 2.3.1 | Static type checker for editor/LSP workflows |

**Transitive closure** frozen in `requirements-win_dev.txt`: Jupyter servers/clients (`jupyterlab`, `notebook`, `jupyter-server`, `nbconvert`, `nbclient`, `nbformat`, `jupyter-core`, `jupyter-client`, `tornado`, `pyzmq`, `terminado` ...), REPL internals (`jedi`, `parso`, `prompt-toolkit`, `stack-data`, `asttokens`, `executing`, `pure-eval`, `matplotlib-inline`), web transport (`httpx`, `httpcore`, `anyio`, `h11`), JSON-schema utilities (`jsonschema`, `referencing`, `rpds-py`, `arrow`, `fqdn`, URI/RFC validators), notebook converters (`nbconvert` stack: `bleach`, `soupsieve`, `jinja2`, `mistune`, `pandocfilters`, `beautifulsoup4`, `tinycss2`, `webencodings`, `defusedxml`), security (`argon2-cffi`, `argon2-cffi-bindings`, `cffi`, `pycparser`), mypy support (`mypy-extensions`, `ast-serialize`, `librt`, `pathspec`, `typing-extensions`), and kernel/widget support (`comm`, `debugpy`, `ipywidgets`, `widgetsnbextension`, `jupyterlab-widgets`, `nest-asyncio2`, `traitlets`, `psutil`).

---

## Tier C — Packaging & Build Toolchain

Installed but intentionally **not pinned** in the requirements files (pip itself manages them):

| Library | Version | Purpose |
| --- | --- | --- |
| `pip` | 26.2.1 | Package installer |
| `setuptools` | 84.0.0 | `pyproject.toml` build backend |
| `wheel` | 0.48.0 | Wheel archive builder |
| `pip-tools` | 7.6.1 | pip-compile/pip-sync — legacy curators of the frozen files (now superseded by `requirements_sync.py`) |
| `pip-review` | 1.3.0 | Check for and apply package upgrades |
| `build` | 1.6.0 | PEP 517 sdist/wheel builder |
| `pyproject_hooks` | 1.2.0 | Invokes PEP 517 build backends |
| `click` | 8.5.0 | CLI framework used by pip-tools/build |

---

## Shared Bottom Layer

The following packages are pinned in **both** compiled files because both tiers depend on them;
`requirements-win_dev.txt` repeats them under the `-c requirements.txt` constraint so the two tiers
can never diverge on versions:

`certifi`, `charset-normalizer`, `colorama`, `idna`, `packaging`, `pygments`, `python-dateutil`, `requests`, `six`, `tzdata`, `urllib3`

---

## Keeping Requirements Current

One command keeps the whole requirement set in sync with the live environment:

`requirements_sync.py` walks the dependency graph of the **installed** packages and rewrites
**both** compiled files (`requirements.txt` + `requirements-win_dev.txt`) to exactly match the
as-installed versions, then audits the result. It is fully offline and deterministic — the
audit is always CLEAN after a run, because a compile can never invent a version that is not
actually installed.

```powershell
# 1. Regenerate BOTH compiled files and re-audit        (offline, safe)
.venv\Scripts\python.exe requirements_sync.py

# ... or from VS Code:  Terminal > Run Task > "Sync: Update Requirements"

# 2. Check for + apply package upgrades (needs network), then re-run step 1
pip-review --auto

# 3. Optional second view: snapshot the live environment
.venv\Scripts\python.exe -m pip freeze
```

**The constant-update loop** (repeat whenever the environment changes):

1. `pip install <library>` into the venv.
2. Declare the *direct* dependency in the right source file:
   - `requirements.in` — libraries imported by project code (Tier A)
   - `requirements-win_dev.in` — development tooling (Tier B)
3. Run `requirements_sync.py` — it pins the new package + its whole closure at today's
   versions in both compiled files and prints a drift report (which tier, which version).
4. Periodically run `pip-review --auto` to pull upgrades, then re-run `requirements_sync.py`
   so the compiled files track the upgraded environment.

**Installing from the frozen files (fresh machine):**

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m pip install -r requirements-win_dev.txt
```

> The classic `pip-compile --no-index ...` commands from older versions of this catalogue are
> **not** a reliable regeneration path: `--no-index` gives pip nothing to resolve from unless a
> `--find-links` source is provided, so `pip-compile` cannot act as the offline source of truth.
> `requirements_sync.py` is the maintained replacement for that workflow.

## Viewing the Environment

```powershell
# List every installed library in this venv, one per line with its version (piped table):
.venv\Scripts\python.exe -m pip list

# The same, but only packages that have an update available:
.venv\Scripts\python.exe -m pip list --outdated

# Details + dependencies of one library (e.g. qrcode):
.venv\Scripts\python.exe -m pip show qrcode

# Verify no installed package has a broken/unsatisfied dependency:
.venv\Scripts\python.exe -m pip check

# Confirm the environment is healthy and packages import cleanly:
.venv\Scripts\python.exe -c "import numpy, pandas, sklearn, matplotlib, seaborn, scipy, openpyxl, psycopg2, requests, pygame, qrcode, pytest; print('all-rounder import OK')"
.venv\Scripts\python.exe -c "import jupyterlab, ipykernel, IPython, mypy; print('windows dev-kit import OK')"
```

> `pip list` (without the `python.exe -m` prefix) works too when the venv is activated; the
> `.venv\Scripts\python.exe -m pip ...` form always targets the correct environment regardless
> of which Python is on the PATH.

