"""
Global CRT overlay settings and layer thresholds.

Translation of ``CRTSettings.java``. The module holds the enabled flag,
the clamped 0-100 intensity and the flicker tick; the tkinter views read
these when drawing scanlines, vignette and flicker. Thresholds are
preserved: scanlines always, vignette from 34, flicker from 67.
"""

_enabled = False
_intensity = 40
flick_tick = 0

SCANLINES_ONLY_MAX = 33
VIGNETTE_MIN = 34
FLICKER_MIN = 67
FLICKER_PERIOD = 20


def is_enabled():
    """
    Whether the CRT overlay draws at all.
    """
    return _enabled


def set_enabled(value):
    """
    Switch the CRT overlay on or off.
    """
    global _enabled
    _enabled = bool(value)


def toggle():
    """
    Flip the CRT overlay on or off.
    """
    set_enabled(not _enabled)


def get_intensity():
    """
    The overlay intensity from 0 to 100.
    """
    return _intensity


def set_intensity(value):
    """
    Clamp the overlay intensity into 0 to 100.
    """
    global _intensity
    _intensity = max(0, min(100, int(value)))


def scan_alpha(intensity=None):
    """
    Scanline opacity for an intensity: 0.08 at zero rising to 0.45.
    """
    level = _intensity if intensity is None else intensity
    return 0.08 + (level / 100.0) * 0.37


def vignette_alpha(intensity=None):
    """
    Vignette opacity for an intensity, capped at 0.70.
    """
    level = _intensity if intensity is None else intensity
    return min(0.70, (level / 100.0) * 0.75)


def flicker_fires(tick=None):
    """
    True on every twentieth flicker tick, when the overlay flashes.
    """
    current = flick_tick if tick is None else tick
    return current % FLICKER_PERIOD == 0


def advance_flicker():
    """
    Step the flicker counter and report whether this frame flashes.
    """
    global flick_tick
    flick_tick += 1
    return flicker_fires()


def reset_flicker():
    """
    Restart the flicker counter, used when the overlay is re-enabled.
    """
    global flick_tick
    flick_tick = 0

