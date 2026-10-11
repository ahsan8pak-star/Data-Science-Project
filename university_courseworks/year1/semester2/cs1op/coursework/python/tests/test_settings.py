"""
Difficulty, CRT overlay and per-sound volume settings.
"""

import crt_settings
import game_settings
import sound_manager
import sound_settings
from game_settings import Difficulty


def test_difficulty_defaults_normal():
    assert game_settings.get_difficulty() == Difficulty.NORMAL
    assert game_settings.difficulty_label() == "NORMAL"


def test_difficulty_cycles_and_labels():
    game_settings.cycle_difficulty()
    assert game_settings.difficulty_label() == "HARD"
    game_settings.cycle_difficulty()
    assert game_settings.difficulty_label() == "EASY"
    game_settings.cycle_difficulty()
    assert game_settings.difficulty_label() == "NORMAL"


def test_difficulty_set():
    game_settings.set_difficulty(Difficulty.HARD)
    assert game_settings.get_difficulty() == Difficulty.HARD


def test_crt_defaults_off_at_forty():
    assert not crt_settings.is_enabled()
    assert crt_settings.get_intensity() == 40


def test_crt_toggle_and_set():
    crt_settings.toggle()
    assert crt_settings.is_enabled()
    crt_settings.toggle()
    assert not crt_settings.is_enabled()
    crt_settings.set_enabled(True)
    assert crt_settings.is_enabled()


def test_crt_intensity_clamps():
    crt_settings.set_intensity(150)
    assert crt_settings.get_intensity() == 100
    crt_settings.set_intensity(-20)
    assert crt_settings.get_intensity() == 0
    crt_settings.set_intensity("55")
    assert crt_settings.get_intensity() == 55


def test_crt_scan_alpha_bounds():
    assert crt_settings.scan_alpha(0) == 0.08
    assert abs(crt_settings.scan_alpha(100) - 0.45) < 1e-9
    assert abs(crt_settings.scan_alpha(40) - (0.08 + 0.4 * 0.37)) < 1e-9


def test_crt_vignette_caps_at_point_seven():
    assert crt_settings.vignette_alpha(34) < 0.70
    assert crt_settings.vignette_alpha(100) == 0.70


def test_crt_flicker_fires_every_twentieth_tick():
    assert crt_settings.flicker_fires(0)
    assert crt_settings.flicker_fires(20)
    assert not crt_settings.flicker_fires(7)
    crt_settings.reset_flicker()
    assert crt_settings.advance_flicker() is False
    for _ in range(19):
        crt_settings.advance_flicker()
    assert crt_settings.flick_tick == 20


def test_volumes_default_to_hundred_in_order():
    files = sound_settings.get_all_sound_files()
    assert len(files) == 34
    assert all(sound_settings.get_volume(f) == 100 for f in files)
    assert files[0] == sound_manager.MENU_NAVIGATE
    assert files[-1] == sound_manager.SI_LOSE


def test_volume_set_clamps_and_refreshes_loop():
    sound_settings.set_volume(sound_manager.MENU_NAVIGATE, 150)
    assert sound_settings.get_volume(sound_manager.MENU_NAVIGATE) == 100
    sound_settings.set_volume(sound_manager.MENU_NAVIGATE, -5)
    assert sound_settings.get_volume(sound_manager.MENU_NAVIGATE) == 0
    sound_settings.set_volume(sound_manager.MENU_NAVIGATE, 60)
    assert sound_settings.get_volume(sound_manager.MENU_NAVIGATE) == 60


def test_display_names_fall_back_to_filename():
    assert sound_settings.get_display_name(sound_manager.MENU_NAVIGATE) == "Menu Navigation"
    assert sound_settings.get_display_name(sound_manager.SI_WIN) == "Invaders Victory"
    assert sound_settings.get_display_name("missing.wav") == "missing.wav"
    assert sound_settings.get_volume("missing.wav") == 100


def test_category_filters():
    pong = sound_settings.get_sound_files_for_category("Pong")
    assert len(pong) == 6
    assert sound_manager.PONG_WIN in pong
    invaders = sound_settings.get_sound_files_for_category("Invaders")
    assert len(invaders) == 12
    general = sound_settings.get_general_sound_files()
    assert len(general) == 16
    assert sound_manager.MENU_NAVIGATE in general
    assert sound_manager.PONG_WIN not in general
    assert sound_manager.SI_WIN not in general

