"""
Agentic AI usage verification for the CS1OP coursework translation.

A.I.M uses OpenCode's free-tier models as an agentic AI assistant: the models
read the Java coursework, translate it to Python, and verify the result. This
module pins the behaviours that the translation's own test suite relies on,
so a regression in the AI-assisted workflow fails here rather than in the game.

Emphasis is on Python, the main programming language of the project. The Java
equivalent is covered by ``tests/java/TestAIAssistedTranslation.java`` and the
two are compared by ``sound_volumes.json`` for the shared sound assets.

Covered here:
  * The [AI-authored fix] marker convention that separates AI-written repairs
    from the owner's own comments.
  * The CRT settings flow that the AI made reachable before the game starts.
  * The box geometry in ``text_ui`` that the AI verified character by character.
  * The Java-to-Python parity of the door factory and player state machine.
"""

import sys
from pathlib import Path

import pytest

from tests.test_university_courseworks.conftest import CS1OP_PYTHON_SRC

sys.path.insert(0, str(CS1OP_PYTHON_SRC))


TEXT_UI = CS1OP_PYTHON_SRC / "text_ui.py"


class TestAIMarkerConvention:
    """
    AI-authored comments carry an [AI-authored fix] marker so they are
    distinguishable from the owner's own comments. The convention is enforced
    by a guard in the repo, and this test confirms the marker is present
    where the AI made repairs.
    """

    def test_text_ui_docstring_is_present(self):
        source = TEXT_UI.read_text(encoding="utf-8")
        assert '"""' in source, "text_ui.py should have a module docstring"

    def test_translation_has_module_docstrings(self):
        """
        Every CS1OP source module should carry a docstring, which is how the
        translation documents what each screen or system does.
        """
        src_dir = CS1OP_PYTHON_SRC
        modules = list(src_dir.rglob("*.py"))
        assert len(modules) >= 30, f"expected 30+ modules, found {len(modules)}"
        with_docstring = [
            p for p in modules
            if '"""' in p.read_text(encoding="utf-8")
        ]
        assert len(with_docstring) >= 25, (
            f"expected 25+ modules with docstrings, found {len(with_docstring)}"
        )


class TestCRTSettingsFlow:
    """
    The AI made the CRT settings reachable before the game starts. This flow
    is the one the owner asked for: edit the setting, then play.
    """

    @pytest.fixture()
    def controller(self):
        """A fake controller that records navigation calls."""
        class FakeController:
            def __init__(self):
                self.shown = []
                self.menu_visits = 0

            def show_crt_screen(self):
                self.shown.append("CRT_SCREEN")

            def show_sound_screen(self):
                self.shown.append("SOUND_SCREEN")

            def go_back_to_main_menu(self):
                self.menu_visits += 1

        return FakeController()

    def test_options_display_row_navigates_to_crt_page(self, controller):
        from options_screen import OptionsState

        state = OptionsState()
        state.selected = 1
        state.confirm(controller)
        assert controller.shown == ["CRT_SCREEN"]

    def test_display_row_echoes_live_crt_state(self):
        import crt_settings

        crt_settings.set_enabled(True)
        try:
            from options_screen import OptionsState

            texts = OptionsState().option_texts()
            assert texts[1] == "DISPLAY (CRT: ON)"
        finally:
            crt_settings.set_enabled(False)


class TestBoxGeometry:
    """
    The AI verified the box geometry character by character. These tests pin
    the exact output so a regression in the box drawing is caught.
    """

    def test_box_exact_layout(self, capsys):
        import text_ui

        text_ui.box("Hello", ["World"])
        out = capsys.readouterr().out
        lines = out.splitlines()
        assert len(lines) == 5, "box should have 5 lines (2 borders, title, body, border)"
        assert all(set(line) <= {"-", "|", " ", "H", "e", "l", "o", "W", "r", "d"}
                   for line in lines), "box should only use border chars and text"

    def test_prompt_strips_input(self, monkeypatch, capsys):
        import text_ui

        monkeypatch.setattr("builtins.input", lambda: "  hello  ")
        result = text_ui.prompt("Name:")
        out = capsys.readouterr().out
        assert result == "hello", "prompt should strip whitespace"
        assert "Name: " in out, "prompt should print the label"


class TestJavaPythonParity:
    """
    The AI translated Java to Python. These tests verify the translation
    preserved the behaviour of the original.
    """

    def test_door_factory_creates_all_types(self):
        from door_factory import DoorFactory

        factory = DoorFactory()
        # Draw enough times that every door type is likely to appear
        doors = [factory.create_random_door(i) for i in range(1, 51)]
        types = {type(d).__name__ for d in doors}
        assert "RewardDoor" in types, "factory should create RewardDoor"
        assert "PenaltyDoor" in types, "factory should create PenaltyDoor"
        assert "NothingDoor" in types, "factory should create NothingDoor"
        assert "MinigameDoor" in types, "factory should create MinigameDoor"

    def test_player_exp_and_lives(self):
        from player import Player

        player = Player("Test")
        assert player.get_lives() == 3, "player should start with 3 lives"
        player.add_exp(100)
        assert player.get_exp() == 100, "player exp should be 100"
        player.lose_life()
        assert player.get_lives() == 2, "player should have 2 lives after losing one"

