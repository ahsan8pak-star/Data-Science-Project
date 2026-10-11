"""
Sound constants, file resolution and the pluggable backend.

Covers the renamed ``sound_effects`` folder end to end: every one of
the 34 WAV constants resolves to a real file, missing files resolve to
nothing, and loops track state through the silent backend without
audio hardware.
"""

import math

import sound_manager
from sound_manager import PygameBackend, SilentBackend


def test_thirty_four_sounds_registered():
    assert len(sound_manager.ALL_SOUNDS) == 34
    assert len(set(sound_manager.ALL_SOUNDS)) == 34


def test_every_constant_resolves_to_a_real_file():
    missing = [name for name in sound_manager.ALL_SOUNDS if sound_manager.resolve_file(name) is None]
    assert missing == []


def test_filenames_keep_exact_case_and_spaces():
    assert sound_manager.resolve_file("Alien Killed.wav") is not None
    assert sound_manager.resolve_file("alien killed.wav") is None
    assert sound_manager.resolve_file("Game Over - No Input.wav") is not None


def test_resolve_rejects_blank_and_missing():
    assert sound_manager.resolve_file("") is None
    assert sound_manager.resolve_file("   ") is None
    assert sound_manager.resolve_file(None) is None
    assert sound_manager.resolve_file("No Such Sound.wav") is None


def test_resolved_files_live_in_sound_effects():
    path = sound_manager.resolve_file(sound_manager.MENU_NAVIGATE)
    assert path.parent.name == "sound_effects"


def test_play_once_records_through_silent_backend():
    backend = SilentBackend()
    sound_manager.set_backend(backend)
    sound_manager.play_once(sound_manager.MENU_NAVIGATE)
    assert len(backend.played) == 1
    assert backend.played[0][0].endswith(sound_manager.MENU_NAVIGATE)
    assert backend.played[0][1] == 100


def test_play_once_skips_missing_silently():
    backend = SilentBackend()
    sound_manager.set_backend(backend)
    sound_manager.play_once("No Such Sound.wav")
    sound_manager.play_once("")
    sound_manager.play_once(None)
    assert backend.played == []


def test_loop_lifecycle_tracks_state():
    backend = SilentBackend()
    sound_manager.set_backend(backend)
    assert not sound_manager.is_looping(sound_manager.HORROR_LOOP)
    sound_manager.play_loop(sound_manager.HORROR_LOOP)
    assert sound_manager.is_looping(sound_manager.HORROR_LOOP)
    sound_manager.play_loop(sound_manager.HORROR_LOOP)
    assert sound_manager.is_looping(sound_manager.HORROR_LOOP)
    sound_manager.stop_sound(sound_manager.HORROR_LOOP)
    assert not sound_manager.is_looping(sound_manager.HORROR_LOOP)


def test_stop_all_clears_every_loop():
    sound_manager.play_loop(sound_manager.HORROR_LOOP)
    sound_manager.play_loop(sound_manager.SI_UFO_FLY)
    sound_manager.stop_all()
    assert not sound_manager.is_looping(sound_manager.HORROR_LOOP)
    assert not sound_manager.is_looping(sound_manager.SI_UFO_FLY)


def test_stop_unknown_sound_is_safe():
    sound_manager.stop_sound("No Such Sound.wav")
    sound_manager.stop_sound("")
    sound_manager.stop_sound(None)


def test_update_loop_volume_refreshes_without_restart():
    backend = SilentBackend()
    sound_manager.set_backend(backend)
    sound_manager.play_loop(sound_manager.SI_UFO_FLY)
    import sound_settings
    sound_settings.set_volume(sound_manager.SI_UFO_FLY, 40)
    key = next(k for k in backend.loops if k.endswith(sound_manager.SI_UFO_FLY))
    assert backend.loops[key] == 40
    assert sound_manager.is_looping(sound_manager.SI_UFO_FLY)


def test_volume_to_db_mapping():
    assert sound_manager.volume_to_db(0) is None
    assert sound_manager.volume_to_db(-3) is None
    assert sound_manager.volume_to_db(100) == 0.0
    assert abs(sound_manager.volume_to_db(50) - (20.0 * math.log10(0.5))) < 1e-9


def test_backend_swap_stops_loops_first():
    old = SilentBackend()
    sound_manager.set_backend(old)
    sound_manager.play_loop(sound_manager.HORROR_LOOP)
    assert sound_manager.is_looping(sound_manager.HORROR_LOOP)
    sound_manager.set_backend(SilentBackend())
    assert not sound_manager.is_looping(sound_manager.HORROR_LOOP)
    assert isinstance(sound_manager.get_backend(), SilentBackend)


def test_pygame_backend_imports_lazily():
    backend = PygameBackend.__new__(PygameBackend)
    assert isinstance(backend, sound_manager.SoundBackend)

