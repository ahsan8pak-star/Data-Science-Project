"""
Run the CS1OP cross-language parity cases against the Python coursework.

[AI-authored fix] The Python coursework is a port of the Java original, and the
two were only ever checked separately: the Java suite proved the Java still
worked and the Python suite proved the Python still worked, which says nothing
about whether they still agree. A translation that compiles is not a translation
that behaves the same.

The cases live in ``ai_parity_cases.json`` next to the coursework rather than
here, because the same file is meant to be readable by a Java suite. Each case
names one behaviour, one shared expectation, and the Java class and method that
produce it on the original side. Python is the emphasis: every case is executed
against the Python modules below, and the Java half is checked statically - the
named class has to exist and the named method has to be public in it - so the
Java side of the spec cannot quietly rot.

`doors.txt` is enumerated through a scripted random number generator rather than
by drawing doors at random. The factory takes its generator as an argument, so
pinning it turns "the factory can make four kinds of door" into a certainty
instead of a test that passes or fails depending on the seed.
"""

import importlib
import json
import sys

from pathlib import Path

import pytest

from tests.test_university_courseworks.conftest import CS1OP_COURSEWORK, CS1OP_PYTHON_SRC

SPEC_PATH = CS1OP_COURSEWORK / "ai_parity_cases.json"
JAVA_SRC = CS1OP_COURSEWORK / "java" / "src"

sys.path.insert(0, str(CS1OP_PYTHON_SRC))


@pytest.fixture(scope="module")
def spec():
    assert SPEC_PATH.is_file(), f"missing parity spec at {SPEC_PATH}"
    return json.loads(SPEC_PATH.read_text(encoding="utf-8"))


class ScriptedRandom:
    """A random number generator that hands back a fixed sequence."""

    def __init__(self, values):
        self.values = list(values)
        self.position = 0

    def randrange(self, stop):
        value = self.values[self.position % len(self.values)]
        self.position += 1
        return value


def reset_crt():
    import crt_settings

    crt_settings.set_enabled(False)
    crt_settings.set_intensity(40)


def crt_disabled_by_default():
    import crt_settings

    reset_crt()
    return crt_settings.is_enabled()


def crt_default_intensity():
    import crt_settings

    reset_crt()
    return crt_settings.get_intensity()


def crt_toggle_flips_state():
    import crt_settings

    reset_crt()
    crt_settings.toggle()
    after_first = crt_settings.is_enabled()
    crt_settings.toggle()
    after_second = crt_settings.is_enabled()
    reset_crt()
    return [after_first, after_second]


def crt_intensity_is_settable():
    import crt_settings

    crt_settings.set_intensity(75)
    high = crt_settings.get_intensity()
    crt_settings.set_intensity(10)
    low = crt_settings.get_intensity()
    reset_crt()
    return [high, low]


def player_starts_with_three_lives():
    from player import Player

    return Player("Parity").get_lives()


def player_exp_accumulates():
    from player import Player

    player = Player("Parity")
    player.add_exp(50)
    first = player.get_exp()
    player.add_exp(20)
    second = player.get_exp()
    player.subtract_exp(65)
    return [first, second, player.get_exp()]


def losing_every_life_ends_the_game():
    from player import Player

    player = Player("Parity")
    readings = [player.is_game_over()]
    for _ in range(3):
        player.lose_life()
        readings.append(player.is_game_over())
    player.lose_life()
    readings.append(player.get_lives())
    return readings


def reset_difficulty():
    import game_settings

    game_settings.set_difficulty(game_settings.Difficulty.NORMAL)


def difficulty_defaults_to_normal():
    import game_settings

    reset_difficulty()
    return game_settings.difficulty_label()


def difficulty_cycles_through_all_three():
    import game_settings

    game_settings.set_difficulty(game_settings.Difficulty.HARD)
    labels = []
    for _ in range(4):
        game_settings.cycle_difficulty()
        labels.append(game_settings.difficulty_label())
    reset_difficulty()
    return labels


def sound_volumes_default_to_full():
    import sound_manager
    import sound_settings

    key = sound_manager.MENU_NAVIGATE
    original = sound_settings.get_volume(key)
    try:
        starting = sound_settings.get_volume(key)
        sound_settings.set_volume(key, 0)
        return [starting, sound_settings.get_volume(key), sound_settings.get_volume(key)]
    finally:
        sound_settings.set_volume(key, original)


def sound_display_names_are_shared():
    import sound_manager
    import sound_settings

    return [
        sound_settings.get_display_name(sound_manager.MENU_NAVIGATE),
        sound_settings.get_display_name(sound_manager.MENU_SELECT),
        sound_settings.get_display_name(sound_manager.TYPEWRITER),
    ]


def door_factory_makes_every_door_type():
    """Walk every template the factory read, pinning the generator to each one."""
    from door_factory import DoorFactory

    template_count = len(DoorFactory().templates)
    types = set()
    for index in range(template_count):
        scripted = DoorFactory(rng=ScriptedRandom([index]))
        types.add(type(scripted.create_random_door(index + 1)).__name__)
    return sorted(types)


def text_ui_box_width_follows_content(capsys):
    import text_ui

    widths = []
    for title, line in (("Room", "Hi"), ("A longer title", "x")):
        capsys.readouterr()
        text_ui.box(title, [line])
        printed = capsys.readouterr().out.splitlines()
        widths.append(max(len(row) for row in printed))
    return widths


# Every case in the spec resolves to one of these. A case added to the JSON
# without a harness call here fails, rather than being quietly skipped.
HARNESS = {
    "crt_disabled_by_default": crt_disabled_by_default,
    "crt_default_intensity": crt_default_intensity,
    "crt_toggle_flips_state": crt_toggle_flips_state,
    "crt_intensity_is_settable": crt_intensity_is_settable,
    "player_starts_with_three_lives": player_starts_with_three_lives,
    "player_exp_accumulates": player_exp_accumulates,
    "losing_every_life_ends_the_game": losing_every_life_ends_the_game,
    "difficulty_defaults_to_normal": difficulty_defaults_to_normal,
    "difficulty_cycles_through_all_three": difficulty_cycles_through_all_three,
    "sound_volumes_default_to_full": sound_volumes_default_to_full,
    "sound_display_names_are_shared": sound_display_names_are_shared,
    "door_factory_makes_every_door_type": door_factory_makes_every_door_type,
    "text_ui_box_width_follows_content": text_ui_box_width_follows_content,
}


# Cases that print and need their output captured, listed rather than sniffed
# out of the function signature.
NEEDS_CAPSYS = frozenset({"text_ui_box_width_follows_content"})


def case_ids(spec):
    return [case["id"] for case in spec["cases"]]


class TestParityCasesRunAgainstPython:
    """The emphasis: every case is actually executed against the port."""

    @pytest.mark.parametrize("case_id", case_ids(
        json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    ))
    def test_case_matches_its_shared_expectation(self, spec, case_id, capsys):
        case = next(item for item in spec["cases"] if item["id"] == case_id)
        harness_call = HARNESS[case["python"]["harness_call"]]

        if case["python"]["harness_call"] in NEEDS_CAPSYS:
            actual = harness_call(capsys)
        else:
            actual = harness_call()

        assert actual == case["expected"], (
            f"{case_id}: Python returned {actual!r}, the shared expectation "
            f"between both languages is {case['expected']!r}. "
            f"{case['title']}"
        )


class TestTheSpecIsComplete:
    """A parity file is only worth something if neither language can drift out of it."""

    def test_every_case_has_both_languages(self, spec):
        for case in spec["cases"]:
            assert "python" in case and "java" in case, (
                f"{case['id']} does not describe both languages"
            )

    def test_every_case_has_a_harness_call(self, spec):
        for case in spec["cases"]:
            name = case["python"]["harness_call"]
            assert name in HARNESS, f"{case['id']} names a harness call that does not exist"
            assert HARNESS[name].__name__ == name, (
                f"{case['id']} maps to a differently named function"
            )

    def test_case_ids_are_unique(self, spec):
        ids = case_ids(spec)
        assert len(ids) == len(set(ids)), "two cases share an id"

    def test_python_is_named_as_the_emphasis(self, spec):
        assert spec["emphasis_language"] == "python"
        assert spec["reference_language"] == "java"


class TestTheJavaHalfStillPointsAtRealCode:
    """
    No Java is written for these cases, per the decision to keep the effort on
    the Python side. What is checked is that the spec still names real Java:
    the class exists and the method is public in it, so the Java suite can be
    pointed at the same file later without the spec having rotted.
    """

    @pytest.mark.parametrize("case_id", case_ids(
        json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    ))
    def test_named_java_class_exists(self, spec, case_id):
        case = next(item for item in spec["cases"] if item["id"] == case_id)
        assert (JAVA_SRC / f"{case['java']['class']}.java").is_file(), (
            f"{case_id} names {case['java']['class']}, which is not in java/src/"
        )

    @pytest.mark.parametrize("case_id", case_ids(
        json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    ))
    def test_named_java_method_is_public(self, spec, case_id):
        case = next(item for item in spec["cases"] if item["id"] == case_id)
        source = (JAVA_SRC / f"{case['java']['class']}.java").read_text(encoding="utf-8")
        signature = f"public static" if case["java"].get("static") else "public"
        assert f"{signature} " in source, f"{case['java']['class']} is not public"
        assert f" {case['java']['method']}(" in source, (
            f"{case_id} names {case['java']['class']}.{case['java']['method']}(), "
            f"which does not exist in the Java source"
        )

    @pytest.mark.parametrize("case_id", case_ids(
        json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    ))
    def test_named_python_api_exists(self, spec, case_id):
        """The Python side is checked against the modules, not just claimed."""
        case = next(item for item in spec["cases"] if item["id"] == case_id)
        for dotted in case["python"]["api"]:
            parts = dotted.split(".")
            module = importlib.import_module(parts[0])
            target = module
            for attribute in parts[1:]:
                assert hasattr(target, attribute), (
                    f"{case_id} names {dotted}, which the Python coursework "
                    f"does not have"
                )
                target = getattr(target, attribute)


class TestTheWorkflowIsRecorded:
    def test_the_spec_says_how_it_was_produced(self, spec):
        workflow = spec["workflow"]
        assert "OpenCode" in workflow["assistant"]
        assert workflow["recorded_in"] == "agentic_models/TASK_MODEL_GUIDE.md"
        assert (Path(__file__).resolve().parents[2] / workflow["recorded_in"]).is_file()

    def test_every_case_says_what_was_done(self, spec):
        for case in spec["cases"]:
            assert case["steps"], f"{case['id']} does not say what it does"
            assert case["title"], f"{case['id']} has no description"

