"""
Global per-sound volume storage with display names.

Translation of ``SoundSettings.java``. Volumes are 0-100 integers kept
in insertion order; every known sound defaults to 100. Setting a volume
also refreshes any live loop through the sound manager, as the Java does.
"""

import sound_manager


_volumes = {}
_display_names = {}


def _register(sound_file, display_name, volume=100):
    _volumes[sound_file] = volume
    _display_names[sound_file] = display_name


def _register_all():
    _register(sound_manager.MENU_NAVIGATE, "Menu Navigation")
    _register(sound_manager.MENU_SELECT, "Menu Confirm")
    _register(sound_manager.TYPEWRITER, "Name Entry Key")
    _register(sound_manager.DIALOGUE_YES, "Yes Choice")
    _register(sound_manager.DIALOGUE_NO, "No Choice")
    _register(sound_manager.HORROR_LOOP, "Rejection Music")
    _register(sound_manager.DOOR_NAVIGATE, "Door Switching")
    _register(sound_manager.DOOR_OPEN, "Door Opening")
    _register(sound_manager.DOOR_CLOSE, "Door Closing")
    _register(sound_manager.CHEST_SHINE, "Chest Reveal")
    _register(sound_manager.REWARD_POINTS, "EXP Gain Jingle")
    _register(sound_manager.POISON_SMOKE, "Poison Reveal")
    _register(sound_manager.PENALTY_POINTS, "EXP Loss Jingle")
    _register(sound_manager.LIFE_LOST, "Life Lost")
    _register(sound_manager.GAME_OVER_SOUND, "Game Over Music")
    _register(sound_manager.GAME_WIN_SOUND, "Victory Theme")
    _register(sound_manager.PONG_PLAYER_HIT, "Pong Player Hit")
    _register(sound_manager.PONG_CPU_HIT, "Pong CPU Hit")
    _register(sound_manager.PONG_PLAYER_POINT, "Pong Player Point")
    _register(sound_manager.PONG_CPU_POINT, "Pong CPU Point")
    _register(sound_manager.PONG_WIN, "Pong Victory")
    _register(sound_manager.PONG_LOSE, "Pong Defeat")
    _register(sound_manager.SI_PLAYER_SHOOT, "Invaders Player Shot")
    _register(sound_manager.SI_MINI_LIFE_LOST, "Invaders Player Hit")
    _register(sound_manager.SI_UFO_FLY, "Invaders UFO Engine Loop")
    _register(sound_manager.SI_UFO_SHOOT, "Invaders UFO Fire")
    _register(sound_manager.SI_UFO_DIE, "Invaders UFO Explosion")
    _register(sound_manager.SI_SPACECRAFT_SHOOT, "Invaders Ship Fire")
    _register(sound_manager.SI_SPACECRAFT_DIE, "Invaders Ship Explosion")
    _register(sound_manager.SI_ALIEN_SHOOT, "Invaders Alien March Loop")
    _register(sound_manager.SI_ALIEN_DIE, "Invaders Alien Kill")
    _register(sound_manager.SI_NEXT_WAVE, "Invaders Wave Clear")
    _register(sound_manager.SI_WIN, "Invaders Victory")
    _register(sound_manager.SI_LOSE, "Invaders Defeat")


_register_all()


def get_volume(sound_file):
    """
    The 0-100 volume for a sound, defaulting to 100 when unknown.
    """
    return _volumes.get(sound_file, 100)


def set_volume(sound_file, volume):
    """
    Clamp a sound's volume into 0-100 and refresh any live loop of it.
    """
    _volumes[sound_file] = max(0, min(100, int(volume)))
    sound_manager.update_loop_volume(sound_file)


def get_display_name(sound_file):
    """
    The friendly name for a sound, or the filename when unregistered.
    """
    return _display_names.get(sound_file, sound_file)


def get_all_sound_files():
    """
    Every registered sound file in registration order.
    """
    return list(_volumes)


def get_sound_files_for_category(category_prefix):
    """
    Registered sounds whose display name starts with the given prefix.
    """
    return [key for key in _volumes if _display_names.get(key, "").startswith(category_prefix)]


def get_general_sound_files():
    """
    Registered sounds outside the Pong and Invaders minigame categories.
    """
    return [
        key for key in _volumes
        if not _display_names.get(key, "").startswith(("Pong", "Invaders"))
    ]

