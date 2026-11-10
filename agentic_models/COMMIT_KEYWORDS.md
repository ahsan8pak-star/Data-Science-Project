# Git Commit Keywords & Phrases — Reference

Source basis: [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/),
[commitlint](https://commitlint.js.org/) (conventional-changelog/commitlint),
[Angular commit guidelines](https://github.com/angular/angular/blob/main/CONTRIBUTING.md#commit),
and [Semantic Release](https://semantic-release.gitbook.io/). This table is the
single source of truth for which keyword/phrase maps to which task so every
agentic model (and human contributor) picks the right one.

## Commit message structure

```
<type>(<scope>): <subject>

<body>

<footer(s)>
```

- `<type>` — **mandatory**. One of the prefixes below.
- `(<scope>)` — **mandatory in this repo** (rule 12): names the file or folder touched.
- `<subject>` — imperative, lowercase, no trailing period.
- `<body>` — optional, explains *why*.
- `<footer(s)>` — optional, separated from body by a blank line (breaking changes, issue refs, co-authors).

## Type prefixes (what task each keyword covers)

| Keyword | Task it covers | When to use | Example |
| --- | --- | --- | --- |
| `feat` | New feature / new source file / new script | Adding functionality or a new file that delivers value | `feat(generator.py): add QR-code generation entry point` |
| `fix` | Bug fix / runtime error resolution | Correcting defective behaviour | `fix(clock.py): resolve timing drift in loop` |
| `docs` | Documentation only | README, docstrings, notes, comments, markdown | `docs(README.md): update setup commands` |
| `style` | Formatting only, no logic change | Whitespace, imports, lint fixes | `style(imports): sort and group imports` |
| `refactor` | Restructure / move without behaviour change | Relocation, rename, extract | `refactor(alarm_clock.py): move to syntax_exercises` |
| `perf` | Performance improvement | Speed/memory optimisation | `perf(search.py): cache repeated lookups` |
| `test` | Add or modify automated tests | pytest additions/edits | `test(test_ranking_docs.py): guard heading drift` |
| `build` | Build system / dependencies | requirements, pyproject, build config | `build(requirements.txt): pin coverage 7.17.0` |
| `ci` | CI / pipeline workflow | GitHub Actions, workflows | `ci(workflow): add automated pytest run` |
| `chore` | Maintenance / housekeeping | `.gitignore`, tooling, cleanup, moves of assets | `chore(.gitignore): ignore .env` |
| `revert` | Revert a previous commit | Undoing a commit | `revert: revert "feat: add X"` |

## Scope (mandatory in this repo)

`(<scope>)` names the **principal file or folder** touched. Use the folder/area when many files change.

| Form | Meaning | Example |
| --- | --- | --- |
| `file.ext` | Single file | `fix(generator.py): resolve import error` |
| `folder/` | Whole folder | `docs(university_courseworks/year2/): add holiday tables` |
| `area` | Cross-cutting area | `chore(deps): bump numpy` |

A commit with **no scope** is wrong even when the prefix is right.

## Breaking-change markers

| Keyword / marker | Meaning | Effect |
| --- | --- | --- |
| `!` after type/scope | Breaking change (short form) | `feat(api)!: drop v1 endpoints` — major bump |
| `BREAKING CHANGE:` footer | Breaking change (long form) | Describes the break in the body/footer |
| `BREAKING-CHANGE:` | Alias of above | Same as `BREAKING CHANGE:` |

## Footer keywords / phrases (task relevance)

| Keyword / phrase | Task it covers | Example |
| --- | --- | --- |
| `Closes #N` / `Fixes #N` / `Resolves #N` | Closes a linked issue/PR | `fix(clock.py): off-by-one\n\nCloses #42` |
| `Refs #N` | References an issue without closing | `docs: update\n\nRefs #7` |
| `Co-authored-by: Name <email>` | Multi-author attribution | `feat: X\n\nCo-authored-by: A <a@x>` |
| `Reviewed-by: Name <email>` | Reviewer attribution | `fix: Y\n\nReviewed-by: B <b@x>` |
| `Signed-off-by: Name <email>` | DCO sign-off | `chore: Z\n\nSigned-off-by: C <c@x>` |
| `Revert "<subject>"` | Revert header (auto-generated) | `revert: revert "feat: add X"` |
| `See also:` / `Related:` | Cross-reference | `docs: note\n\nSee also: #9` |

## Rules of thumb (task → keyword)

| Task | Keyword | Notes |
| --- | --- | --- |
| Creating a new file | `feat` (or `test`/`docs`/`chore` for tests/docs/config) | `feat: create <file_name>` |
| Patching a bug | `fix` | |
| Documentation only | `docs` | |
| Formatting only | `style` | No logic change |
| Moving / relocating a file | `refactor` | Use `git mv` |
| Renaming without behaviour change | `refactor` | |
| Adding / editing tests | `test` | |
| Dependency / build config change | `build` | |
| CI workflow change | `ci` | |
| Performance improvement | `perf` | |
| Maintenance / cleanup / `.gitignore` | `chore` | |
| Undoing a commit | `revert` | |
| Breaking API change | `feat!` / `fix!` + `BREAKING CHANGE:` | Major version bump |

## Non-standard prefixes (do NOT use)

| Bad prefix | Why it breaks things | Use instead |
| --- | --- | --- |
| `file(...)` | Breaks commitlint, changelogs, Semantic Release | The correct type (`feat`, `fix`, …) with a scope |

## Source references

- Conventional Commits 1.0.0 — <https://www.conventionalcommits.org/en/v1.0.0/>
- commitlint rules — <https://commitlint.js.org/>
- Angular contributing guide — <https://github.com/angular/angular/blob/main/CONTRIBUTING.md>
- Semantic Release — <https://semantic-release.gitbook.io/>
- Git trailers (Co-authored-by etc.) — <https://git-scm.com/docs/git-interpret-trailers>
