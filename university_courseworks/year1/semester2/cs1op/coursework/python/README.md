# CS1OP Python translation

A faithful Python port of the Java text adventure in `../java/src/`,
mirroring its file layout one class per module. The Java submission is
untouched; this tree exists so the same game can be read, run and tested
as Python.

## Layout

```
python/
├── src/            # the game, one module per Java class (snake_case)
├── tests/          # pytest suite: ports of the Java suites plus new pins
├── resources/      # doors.txt, GUI.txt and sound_effects/ (34 WAVs)
└── README.md       # this file
```

## Running it

```bash
# from this folder, with the repo venv
/mnt/c/Users/A.I.M/C.S/Data-Science-Project/.venv/Scripts/python.exe src/main.py        # GUI version
/mnt/c/Users/A.I.M/C.S/Data-Science-Project/.venv/Scripts/python.exe src/main.py --text # terminal version
```

## Testing

```bash
/mnt/c/Users/A.I.M/C.S/Data-Science-Project/.venv/Scripts/python.exe -m pytest tests/ -q
```

178 tests, all headless: no window and no audio device needed. Every
interactive screen and both minigames split pure state (tested) from
the tkinter canvas (import-safe without a display). Sound plays through
a backend: silent by default, `PygameBackend` when real playback is
wanted.

## CRT settings

The overlay is one global setting in `crt_settings.py`, so it is edited in
one place and applies everywhere. Two paths reach it before a game starts:
OPTIONS then DISPLAY opens the full-screen `crt_screen.py` (toggle,
0-100 intensity and the band legend), and the OPTIONS row itself echoes the
live state so the current setting is visible without opening it. Both
minigame pause menus keep the same controls for adjusting mid-game, because
the setting is global rather than per-screen.

The overlay is drawn by the in-game screens: both minigames, the door
selection screen, the dialogue and the gameplay panel. The pre-game menus
(main menu, options, name entry, sound and the CRT page itself) deliberately
leave it off, so the setting is legible while it is being changed. `ESC`
from the CRT page returns to OPTIONS, which is the route out again.

## Intentional divergences from the Java

Three places translate what the Java means rather than what it says,
because the Java as committed is broken there:

1. `game_controller.py` builds a `CRTScreen` that does not exist in the
   Java sources, so the Java tree does not compile. The Python adds the
   clearly intended `crt_screen.py` (on/off toggle, 0-100 intensity,
   same bands as the pause menus) instead of reproducing the break.
2. The saucer hit message read "minigame lifes". The Python writes
   "lives".
3. Sounds live in `resources/sound_effects/` (renamed from
   `Sound Effects` on both trees), and resolution is case-exact even on
   case-insensitive filesystems.
