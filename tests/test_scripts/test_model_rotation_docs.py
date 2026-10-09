"""
The free-model rotation tables in AGENTS.md and PROGRESSION.md carry hard
numbers: route context, route output, privacy behaviour and usage volume.
None of them can be recomputed from the repo, so nothing would catch them
drifting - which is exactly how the five unsupported claims recorded in the
1 October 2026 session survived a first draft.

The guard that is possible offline is the structural one: every model named in
the pick-a-model table must also carry a pros/cons row, a main purpose and
three ranked hand-off recommendations. A model added to the rotation without
its downside documented would fail here, which is the moment to fix it rather
than after a model is picked for work it cannot do.
"""

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
AGENTS_MD = REPO_ROOT / "AGENTS.md"
PROGRESSION_MD = REPO_ROOT / "PROGRESSION.md"
ALLOWANCE_MD = REPO_ROOT / "model_rotation" / "MODEL_ALLOWANCE.md"

MODELS = [
    "Big Pickle Free",
    "Space Bunny Free",
    "Nemotron 3.5 Lightning Free",
    "Nemotron 3 Ultra Free",
    "Ling 3.0 Flash Fin Free",
    "Ling 3.1 Flash Free",
    "Muse Spark 1.3 Contributor Free",
    "MiMo-V2.6-Flash Free",
    "MiMo-V2.5 Free",
    "LongCat 2.5 Preview Free",
    "Exo Free",
    "Fledge Alpha Free",
]


def _rows(document):
    """Return the pipe-table rows of document that name a free model."""
    return [
        line for line in document.read_text(encoding="utf-8").splitlines()
        if line.startswith("|") and any(m in line for m in MODELS)
    ]


def _paragraphs(document):
    """
    Blank-line-separated blocks of text.

    The rotation section is hard-wrapped at 80 columns, so a sentence and the
    evidence that supports it routinely sit on different physical lines.
    Matching single lines would therefore flag correct prose, so the checks
    that are about meaning run over paragraphs instead.
    """
    text = document.read_text(encoding="utf-8")
    return [" ".join(block.split()) for block in text.split("\n\n") if block.strip()]


def _table_rows(document, header_fragment):
    """
    The body rows of the table whose header contains the fragment.

    Two of the rotation tables happen to have the same number of columns, so
    matching on width alone picks up the wrong one. Anchoring on the header
    text is what makes the check mean the table it claims to mean.
    """
    lines = document.read_text(encoding="utf-8").splitlines()
    for i, line in enumerate(lines):
        if not (line.startswith("|") and header_fragment in line
                and "---" not in line):
            continue
        rows = []
        for row in lines[i + 2:]:
            if not row.startswith("|"):
                break
            rows.append(row)
        return rows
    raise AssertionError(f"no table header containing {header_fragment!r} was found")


def _columns_of_table(document, header_fragment):
    """
    Number of pipe-split cells in the table whose header contains the fragment.

    Counting from the header rather than hard-coding the width is what stops a
    guard from passing vacuously when someone adds a column: a literal column
    count silently stops matching, and a check that finds nothing looks exactly
    like a check that found no problems.
    """
    return len(_table_rows(document, header_fragment)[0].split("|"))


@pytest.fixture(scope="module")
def agents_text():
    return AGENTS_MD.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def progression_text():
    return PROGRESSION_MD.read_text(encoding="utf-8")


class TestRotationTables:

    def test_the_rotation_lists_every_model(self, agents_text):
        for model in MODELS:
            assert model in agents_text, f"{model} is missing from AGENTS.md"

    def test_the_rotation_names_twelve_models(self, agents_text):
        """
        The count is stated in prose in two places, so a model added to the
        table without updating them leaves the document self-contradictory.
        """
        assert "twelve free" in agents_text, (
            "AGENTS.md no longer states how many free models are rotated"
        )
        assert "All\ntwelve free models share one endpoint" in agents_text or \
            "twelve free models share one endpoint" in agents_text, (
            "the shared-endpoint sentence does not agree with the model count"
        )

    def test_every_model_has_a_pros_and_cons_row(self, agents_text):
        """
        A model listed as usable but with no documented downside is the exact
        failure the hand-off rule exists to prevent, so it is made a test
        failure rather than a reviewer's job to notice.

        The column count is read from the table header rather than hard-coded.
        A literal here would quietly stop matching the moment a column was
        added, and the guard would then pass by finding nothing.
        """
        expected = _columns_of_table(AGENTS_MD, "Main assets")
        rows = _rows(AGENTS_MD)
        for model in MODELS:
            matching = [r for r in rows if r.startswith(f"| {model} ")]
            assert len(matching) >= 3, (
                f"{model} appears {len(matching)} time(s) in AGENTS.md's model "
                f"tables; it needs a pick-a-model row, a usage row and a "
                f"pros/cons row"
            )
            pros_cons = [r for r in matching if len(r.split("|")) == expected]
            assert pros_cons, (
                f"{model} has no Main purpose / assets / weaknesses row, so an "
                f"agent cannot tell when to hand the task off"
            )

    def test_every_model_states_assets_weaknesses_and_a_corrected_use(self):
        """
        The four categories the rotation is read by: what the model is for,
        what it is good at, what it is bad at, and the applied use that
        survived correction. A row missing any of them cannot answer question
        three of the pre-flight, which is applicability.
        """
        body = _table_rows(AGENTS_MD, "Main assets")
        checked = 0
        for row in body:
            checked += 1
            cells = [c.strip() for c in row.split("|")[1:-1]]
            name, purpose, assets, weaknesses, applied = cells
            assert purpose, f"{name} has no stated main purpose"
            assert assets, f"{name} must state its main assets"
            assert weaknesses, f"{name} must state its weaknesses"
            assert "corrected" in applied.lower(), (
                f"{name}'s applied use carries no note of what was corrected"
            )
        assert checked == len(MODELS), (
            f"the assets/weaknesses table has {checked} model rows for "
            f"{len(MODELS)} models"
        )

    def test_every_model_has_three_ranked_hand_offs(self, agents_text):
        """
        A ranked three is the actionable form. One recommendation is a shrug,
        and a flat list of the other seven hands the decision straight back to
        A.I.M, which is what the rule exists to avoid.
        """
        rows = _rows(AGENTS_MD)
        for model in MODELS:
            handoffs = [r for r in rows if r.startswith(f"| **{model}**")]
            assert handoffs, f"{model} has no hand-off row"
            row = handoffs[0]
            body = row.split("|", 2)[2].strip()
            numbered = re.findall(r"(?:^|[.;]\s)([123])\.\s", body)
            assert numbered[:3] == ["1", "2", "3"], (
                f"{model}'s hand-off row must offer three ranked models in "
                f"order, found {numbered[:3]}"
            )
            recommended = re.findall(r"[123]\.\s([^—\n]+?)—", body)[:3]
            named = [r.strip() for r in recommended]
            assert len(set(named)) == 3, (
                f"{model}'s hand-off row names the same model twice: {named}"
            )
            for name in named:
                assert name in MODELS, (
                    f"{model}'s hand-off recommends {name!r}, which is not a "
                    f"model in the rotation"
                )

    def test_no_hand_off_recommends_the_model_itself(self, agents_text):
        for row in _rows(AGENTS_MD):
            if not row.startswith("| **"):
                continue
            cells = [c.strip() for c in row.split("|")[1:-1]]
            current = cells[0].replace("*", "")
            body = row.split("|", 2)[2]
            for number in re.findall(r"[123]\.\s([^—\n]+?)—", body):
                assert current not in number, (
                    f"{current}'s hand-off recommends itself at position "
                    f"{number.strip()}"
                )

    def test_the_preflight_reads_the_allowance_file(self, agents_text):
        """
        Question two of the pre-flight is answered by reading a file, not by an
        agent guessing, so the path has to be right - not merely present.

        [AI-authored fix] The first version of this guard checked that the
        file's *name* appeared somewhere in the section, which passed against a
        mutation that stripped the folder from one of the two references: the
        other reference still satisfied it. A guard that only checks a substring
        somewhere is checking that the name exists, not that the path is right,
        and after the file moved into model_rotation/ those are different things.
        So every mention is now checked, and each one must carry the folder.
        """
        section = agents_text.split("Before each run: the pre-flight check")[1]
        section = section.split("####")[0]
        flat = " ".join(section.split())

        assert ALLOWANCE_MD.is_file(), (
            f"{ALLOWANCE_MD.name} is referenced by the pre-flight but "
            f"{ALLOWANCE_MD.relative_to(REPO_ROOT)} does not exist"
        )
        mentions = re.findall(r"`([^`]*MODEL_ALLOWANCE\.md)`", flat)
        assert mentions, (
            "the pre-flight does not name the allowance file, so the allowance "
            "check has no stated source"
        )
        relative = ALLOWANCE_MD.relative_to(REPO_ROOT).as_posix()
        stale = sorted({m for m in mentions if m != relative})
        assert stale == [], (
            f"the pre-flight refers to the allowance file as {stale}, but it "
            f"lives at {relative!r}; an agent opening the stated path from the "
            "repository root finds nothing"
        )
        assert "empty or stale" in flat, (
            "the pre-flight does not say that an empty or stale allowance row "
            "fails the check, so a blank table reads as a silent pass"
        )

    def test_privacy_override_is_stated(self, agents_text):
        """
        The one case where "best model for the task" is the wrong answer is a
        prompt carrying credentials or personal data, so the override has to
        live next to the table it overrides.
        """
        assert "Privacy overrides the ranking" in agents_text, (
            "AGENTS.md ranks models for fit but does not say that retention "
            "outranks fit, so a credential-bearing prompt has no stated rule"
        )
        override = " ".join(agents_text.split("Privacy overrides the ranking")[1].split())
        for zero_retention in ("Space Bunny Free", "LongCat 2.5 Preview Free"):
            assert zero_retention in override[:600], (
                f"{zero_retention} is not named as zero-retention in the "
                f"privacy override"
            )


class TestPreFlight:

    def test_the_preflight_names_all_three_questions(self, agents_text):
        """
        The pre-flight is only useful if it is the same three questions every
        time: does the task fit the limits, how much allowance is left, and is
        this the model's job. Dropping the third collapses the rule into "is it
        fast", which is the ordering the owner explicitly reversed.
        """
        assert "Before each run: the pre-flight check" in agents_text, (
            "AGENTS.md has no pre-flight check, so a model gets picked by habit "
            "instead of by the task"
        )
        section = agents_text.split("Before each run: the pre-flight check")[1]
        section = section.split("####")[0]
        # The section is hard-wrapped, so match on collapsed whitespace.
        flat = " ".join(section.split())
        for marker in ("**Tokens.**", "**Percentage left.**", "**Applicability.**"):
            assert marker in flat, f"the pre-flight is missing {marker}"
        assert "speed is the last consideration" in flat, (
            "the pre-flight does not record that speed ranks last"
        )
        assert "no agent can read" in flat, (
            "the pre-flight does not say that the remaining allowance has to be "
            "stated by A.I.M, so the check silently passes when nobody knows it"
        )

    def test_every_model_has_a_usage_share_row(self, agents_text):
        """
        Question two of the pre-flight needs a per-model figure, so each of the
        nine has to appear in the tokens-and-share table. A model missing there
        would be chosen without any idea of what share of the tier it carries.
        """
        rows = _table_rows(AGENTS_MD, "Share of listed traffic")
        for model in MODELS:
            assert any(r.startswith(f"| {model} ") for r in rows), (
                f"{model} has no row in the tokens-and-share table"
            )

    def test_unmeasured_share_is_not_invented(self, agents_text):
        """
        Four models are absent from the published ranking. The honest cell is
        "unmeasured"; a number there would be a guess with a table around it.
        """
        section = agents_text.split("Share of listed traffic")[1][:4000]
        for model in ("Big Pickle Free", "Ling 3.0 Flash Fin Free",
                      "Ling 3.1 Flash Free", "Exo Free"):
            row = next(
                (line for line in section.splitlines()
                 if line.startswith(f"| {model} ")),
                None,
            )
            assert row is not None, f"{model} has no usage row"
            assert re.search(r"unmeasured|below the published", row), (
                f"{model} has no measured share, so its cell must say so "
                f"rather than carry a number"
            )

    def test_the_share_denominator_is_named(self, agents_text):
        """
        A percentage is meaningless without its denominator. The figure is a
        share of the eighteen models the source page lists, not of all traffic,
        and the two are very different numbers.
        """
        section = agents_text.split("#### Tokens and usage share")[1][:2500]
        assert "144.879T" in section, (
            "the usage table does not state the token total its shares are "
            "taken against"
        )
        assert "eighteen" in section, (
            "the usage table does not say how many models that total covers"
        )


class TestRotationClaims:

    def test_progression_covers_the_same_models(self, progression_text):
        for model in MODELS:
            assert model in progression_text, (
                f"{model} is missing from PROGRESSION.md"
            )

    def test_the_hand_off_rule_is_explained(self, progression_text):
        """
        The rule is addressed to agents, so the narrative has to say why it
        exists rather than leaving it as an unexplained instruction.
        """
        assert "The rotation needed a rule, not just a list" in progression_text, (
            "PROGRESSION.md does not explain why the rotation grew a hand-off "
            "rule"
        )
        for phrase in ("three alternatives, ranked", "request, not a switch",
                       "Privacy outranks fit"):
            assert phrase in progression_text, (
                f"PROGRESSION.md omits the hand-off constraint: {phrase}"
            )

    def test_no_live_source_url_was_retracted(self, agents_text, progression_text):
        """
        The retracted URLs are named in PROGRESSION.md as things that failed
        verification. They must never be left as live references anywhere, or
        a reader would follow one and find nothing.
        """
        for dead in ("bittide.aicompass.dev", "pi.dev/models/opencode",
                     "models.opencode.ai/models", "longcat.chat/platform/docs"):
            assert dead not in agents_text, (
                f"AGENTS.md still points at {dead}, which was checked and does "
                f"not support the claim it was attached to"
            )
        evidence = " ".join(_paragraphs(PROGRESSION_MD))
        for dead in ("bittide.aicompass.dev", "pi.dev/models/opencode"):
            if dead in evidence:
                assert "did not survive" in evidence and "404" in evidence, (
                    f"{dead} appears in PROGRESSION.md without the correction "
                    f"that explains why it was dropped"
                )

    def test_unsupported_figures_are_not_repeated_as_facts(self, progression_text):
        """
        The retracted benchmark figure stays only inside the passage that
        retracts it. Quoted there it is history; quoted elsewhere it becomes a
        claim again, which is how it came back in the first place.
        """
        markers = ("did not survive", "news aggregator", "could not be traced",
                   "returns HTTP 404")
        for paragraph in _paragraphs(PROGRESSION_MD):
            for figure in ("50.8", "SWE Atlas"):
                if figure in paragraph:
                    assert any(m in paragraph for m in markers), (
                        f"{figure} is quoted in PROGRESSION.md outside the "
                        f"passage that retracts it"
                    )

