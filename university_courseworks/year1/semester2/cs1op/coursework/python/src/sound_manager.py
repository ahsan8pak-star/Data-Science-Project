"""
Central WAV sound registry with a pluggable playback backend.

Translation of ``SoundManager.java``. Path resolution keeps the Java
strategies: candidates relative to the working directory, then relative
to this file's location, then a package-resource lookup. Sounds live in
``resources/sound_effects/``; the WAV filenames are byte-identical to the
Java constants, spaces and capitals included.

Playback goes through a backend so the test suite never needs audio
hardware. The default ``SilentBackend`` resolves files and tracks loops
without playing anything; ``PygameBackend`` plays through ``pygame.mixer``
when it is available. Every entry point swallows backend errors, keeping
the Java guarantee that a missing file or a missing audio line can never
crash the game.
"""

import math
import os
from pathlib import Path


SOUND_FOLDER = "sound_effects"

DEFAULT_RESOURCES = Path(__file__).resolve().parent.parent / "resources"

MENU_NAVIGATE = "Movement 1.wav"
MENU_SELECT = "Main Menu GUI.wav"
TYPEWRITER = "Name Typped.wav"

DIALOGUE_YES = "Yes Pressed.wav"
DIALOGUE_NO = "No Pressed.wav"
HORROR_LOOP = "Game Over - No Input.wav"

DOOR_NAVIGATE = "Movement 2.wav"
DOOR_OPEN = "Nothing Door Open.wav"
DOOR_CLOSE = "Nothing Door Shut.wav"

CHEST_SHINE = "Shiny Chest.wav"
REWARD_POINTS = "EXP Gained.wav"

POISON_SMOKE = "Poison Bottle.wav"
PENALTY_POINTS = "EXP Lost.wav"

LIFE_LOST = "Life Lost.wav"
GAME_OVER_SOUND = "Game Over.wav"
GAME_WIN_SOUND = "Game Won.wav"

PONG_PLAYER_HIT = "Player Pong.wav"
PONG_CPU_HIT = "CPU Pong.wav"
PONG_PLAYER_POINT = "Player Point Pong.wav"
PONG_CPU_POINT = "CPU Point.wav"
PONG_WIN = "Pong Win.wav"
PONG_LOSE = "Pong Lose.wav"

SI_PLAYER_SHOOT = "Player Shoot.wav"
SI_MINI_LIFE_LOST = "Minilife lost.wav"
SI_UFO_FLY = "UFO Hovering.wav"
SI_UFO_SHOOT = "UFO Shooting.wav"
SI_UFO_DIE = "UFO Crashing.wav"
SI_SPACECRAFT_SHOOT = "Spacecraft Shooting.wav"
SI_SPACECRAFT_DIE = "Spacecraft Crashed.wav"
SI_ALIEN_SHOOT = "Aliens Shooting.wav"
SI_ALIEN_DIE = "Alien Killed.wav"
SI_NEXT_WAVE = "Point.wav"
SI_WIN = "Space Invader Won.wav"
SI_LOSE = "Game Lost.wav"

ALL_SOUNDS = (
    MENU_NAVIGATE, MENU_SELECT, TYPEWRITER,
    DIALOGUE_YES, DIALOGUE_NO, HORROR_LOOP,
    DOOR_NAVIGATE, DOOR_OPEN, DOOR_CLOSE,
    CHEST_SHINE, REWARD_POINTS,
    POISON_SMOKE, PENALTY_POINTS,
    LIFE_LOST, GAME_OVER_SOUND, GAME_WIN_SOUND,
    PONG_PLAYER_HIT, PONG_CPU_HIT, PONG_PLAYER_POINT, PONG_CPU_POINT,
    PONG_WIN, PONG_LOSE,
    SI_PLAYER_SHOOT, SI_MINI_LIFE_LOST, SI_UFO_FLY, SI_UFO_SHOOT,
    SI_UFO_DIE, SI_SPACECRAFT_SHOOT, SI_SPACECRAFT_DIE, SI_ALIEN_SHOOT,
    SI_ALIEN_DIE, SI_NEXT_WAVE, SI_WIN, SI_LOSE,
)


def volume_to_db(volume):
    """
    Master-gain decibels for a 0-100 volume, or None to use the minimum.

    Mirrors the Java mapping: silence maps to the control minimum, anything
    above follows ``20 * log10(volume / 100)``.
    """
    if volume <= 0:
        return None
    return 20.0 * math.log10(volume / 100.0)


def matches_exact_case(path):
    """
    True when every part of a resolved path matches disk case exactly.

    Windows resolves case-insensitively, so ``alien killed.wav`` would
    otherwise open ``Alien Killed.wav``. The coursework names its files
    with meaningful capitals, so resolution enforces them everywhere.
    """
    absolute = Path(path)
    try:
        parts = absolute.relative_to(absolute.anchor).parts
    except ValueError:
        return False
    current = absolute.anchor
    for part in parts:
        if part in (".", ".."):
            current = os.path.join(current, part)
            continue
        try:
            entries = os.listdir(current or ".")
        except OSError:
            return False
        if part not in entries:
            return False
        current = os.path.join(current, part)
    return True


def resolve_file(sound_file, resources_dir=None):
    """
    Locate a sound file, trying working-directory candidates first.

    Returns a ``Path`` to the file, or ``None`` when it cannot be found.
    """
    if not sound_file or not sound_file.strip():
        return None
    base = Path(resources_dir) if resources_dir else DEFAULT_RESOURCES
    candidates = [
        Path.cwd() / "resources" / SOUND_FOLDER / sound_file,
        Path("resources") / SOUND_FOLDER / sound_file,
        Path("..") / "resources" / SOUND_FOLDER / sound_file,
        Path("src") / ".." / "resources" / SOUND_FOLDER / sound_file,
        base / SOUND_FOLDER / sound_file,
        Path(__file__).resolve().parent.parent / "resources" / SOUND_FOLDER / sound_file,
    ]
    for candidate in candidates:
        absolute = candidate if candidate.is_absolute() else Path.cwd() / candidate
        if not matches_exact_case(absolute):
            continue
        try:
            resolved = candidate.resolve()
        except OSError:
            continue
        if resolved.is_file():
            return resolved
    return None


class SoundBackend:
    """
    Playback interface. Backends play, loop and stop named files.
    """

    def play_once(self, path, volume):
        """
        Play a file exactly once.
        """

    def play_loop(self, path, volume):
        """
        Loop a file until stopped.
        """

    def stop(self, sound_file):
        """
        Stop a looping file.
        """

    def stop_all(self):
        """
        Stop every looping file.
        """

    def is_running(self, sound_file):
        """
        True while the named loop is playing.
        """
        return False

    def set_volume(self, sound_file, volume):
        """
        Refresh a live loop's volume without restarting it.
        """


class SilentBackend(SoundBackend):
    """
    No-audio backend for tests and headless machines.

    Files still resolve and loops are still tracked, so registry logic
    and ``is_looping`` behave exactly as with real playback.
    """

    def __init__(self):
        self.played = []
        self.loops = {}

    def play_once(self, path, volume):
        self.played.append((str(path), volume))

    def play_loop(self, path, volume):
        self.loops[str(path)] = volume

    def stop(self, sound_file):
        self.loops = {k: v for k, v in self.loops.items() if not k.endswith(sound_file)}

    def stop_all(self):
        self.loops.clear()

    def is_running(self, sound_file):
        return any(key.endswith(sound_file) for key in self.loops)

    def set_volume(self, sound_file, volume):
        for key in self.loops:
            if key.endswith(sound_file):
                self.loops[key] = volume


class PygameBackend(SoundBackend):
    """
    Real playback through ``pygame.mixer``, imported lazily.

    Volumes map linearly onto the mixer (0-100 to 0.0-1.0); the decibel
    mapping above documents the Java behaviour for reference.
    """

    def __init__(self):
        import pygame
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        self._pygame = pygame
        self._loops = {}

    def play_once(self, path, volume):
        sound = self._pygame.mixer.Sound(str(path))
        sound.set_volume(max(0.0, min(1.0, volume / 100.0)))
        sound.play()

    def play_loop(self, path, volume):
        self.stop(path.rsplit("/", 1)[-1])
        sound = self._pygame.mixer.Sound(str(path))
        sound.set_volume(max(0.0, min(1.0, volume / 100.0)))
        sound.play(loops=-1)
        self._loops[str(path)] = sound

    def stop(self, sound_file):
        for key in [k for k in self._loops if k.endswith(sound_file)]:
            self._loops.pop(key).stop()

    def stop_all(self):
        for sound in self._loops.values():
            sound.stop()
        self._loops.clear()
        self._pygame.mixer.stop()

    def is_running(self, sound_file):
        return any(key.endswith(sound_file) for key in self._loops)

    def set_volume(self, sound_file, volume):
        level = max(0.0, min(1.0, volume / 100.0))
        for key, sound in self._loops.items():
            if key.endswith(sound_file):
                sound.set_volume(level)


_backend = SilentBackend()
_active_loops = {}


def set_backend(backend):
    """
    Swap the playback backend, stopping every loop first.
    """
    stop_all()
    global _backend
    _backend = backend


def get_backend():
    """
    The current playback backend.
    """
    return _backend


def _volume_of(sound_file):
    import sound_settings
    return sound_settings.get_volume(sound_file)


def play_once(sound_file):
    """
    Play a sound exactly once, silently skipping missing files.
    """
    if not sound_file or not sound_file.strip():
        return
    try:
        path = resolve_file(sound_file)
        if path is None:
            return
        _backend.play_once(path, _volume_of(sound_file))
    except Exception:
        pass


def play_loop(sound_file):
    """
    Loop a sound, stopping any existing loop of it first.
    """
    if not sound_file or not sound_file.strip():
        return
    try:
        stop_sound(sound_file)
        path = resolve_file(sound_file)
        if path is None:
            return
        _backend.play_loop(path, _volume_of(sound_file))
        _active_loops[sound_file] = path
    except Exception:
        pass


def stop_sound(sound_file):
    """
    Stop one looping sound by its filename.
    """
    if not sound_file or not sound_file.strip():
        return
    try:
        _active_loops.pop(sound_file, None)
        _backend.stop(sound_file)
    except Exception:
        pass


def stop_all():
    """
    Stop every looping sound.
    """
    try:
        _active_loops.clear()
        _backend.stop_all()
    except Exception:
        pass


def is_looping(sound_file):
    """
    True while the named loop is currently playing.
    """
    try:
        return sound_file in _active_loops and _backend.is_running(sound_file)
    except Exception:
        return False


def update_loop_volume(sound_file):
    """
    Refresh a live loop's volume without restarting it.
    """
    try:
        if sound_file in _active_loops and _backend.is_running(sound_file):
            _backend.set_volume(sound_file, _volume_of(sound_file))
    except Exception:
        pass

