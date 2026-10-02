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

MODELS = [
    "Big Pickle Free",
    "Space Bunny Free",
    "Nemotron 3.5 Lightning Free",
    "Nemotron 3 Ultra Free",
    "Ling 3.0 Flash Fin Free",
    "Muse Spark 1.3 Contributor Free",
    "MiMo-V2.6-Flash Free",
    "LongCat 2.5 Preview Free",
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

    def test_the_rotation_names_nine_models(self, agents_text):
        """
        The count is stated in prose in two places, so a model added to the
        table without updating them leaves the document self-contradictory.
        """
        assert "nine free" in agents_text, (
            "AGENTS.md no longer states how many free models are rotated"
        )
        assert "All\nnine free models share one endpoint" in agents_text or \
            "nine free models share one endpoint" in agents_text, (
            "the shared-endpoint sentence does not agree with the model count"
        )

    def test_every_model_has_a_pros_and_cons_row(self, agents_text):
        """
        A model listed as usable but with no documented downside is the exact
        failure the hand-off rule exists to prevent, so it is made a test
        failure rather than a reviewer's job to notice.
        """
        rows = _rows(AGENTS_MD)
        for model in MODELS:
            matching = [r for r in rows if r.startswith(f"| {model} ")]
            assert len(matching) >= 2, (
                f"{model} appears {len(matching)} time(s) in AGENTS.md's model "
                f"tables; it needs both a pick-a-model row and a pros/cons row"
            )
            pros_cons = [r for r in matching if len(r.split("|")) == 6]
            assert pros_cons, (
                f"{model} has no Main purpose / Pros / Cons row, so an agent "
                f"cannot tell when to hand the task off"
            )

    def test_every_model_has_a_main_purpose(self, agents_text):
        for row in _rows(AGENTS_MD):
            cells = [c.strip() for c in row.split("|")[1:-1]]
            if len(cells) != 4:
                continue
            purpose, pros, cons = cells[1], cells[2], cells[3]
            assert purpose, f"{cells[0]} has no stated main purpose"
            assert pros and cons, f"{cells[0]} must state both a pro and a con"

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

