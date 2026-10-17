# CS1OP-TextGame : Space Mission

**Module Code:** CS1OP

**Assignment Title:** Project

**Student Number:** om001219

**Actual hours spent:** ~150 hours

**AI tools used:** Claude (Anthropic), Gemini (Google)

**Repository URL:** <https://csgitlab.reading.ac.uk/om001219/CS1OP-TextGame>

---

## Game Description

Space Mission is a Java GUI Sci-Fi adventure game built using Swing Utilities, with a retro green-on-black aesthetic inspired by Geometry Wars 2. The player wakes up in orbit aboard a space station and must accumulate **500 EXP** by opening mystery doors. Each door delivers an EXP reward, penalty, or triggers a minigame challenge.

The game includes two fully playable minigames:

- **Pong** — Retro Arcade Table Tennis
- **Space Invaders** — Classic Arcade Space Shooter

Plus a dice-based starting EXP mechanic, three difficulty levels, and 30 OOP-compliant Java classes.

---

## Project Structure

```
CS1OP-TextGame/
├── src/
│   ├── Main.java                    # Entry point
│   ├── Game.java                    # Singleton game state
│   ├── Player.java                  # Player EXP, lives, inventory
│   ├── Door.java                    # Abstract base for doors
│   ├── RewardDoor.java              # EXP reward door
│   ├── PenaltyDoor.java             # EXP penalty door
│   ├── NothingDoor.java             # No-change door
│   ├── MinigameDoor.java            # Minigame trigger door
│   ├── DoorFactory.java             # Factory pattern door creation
│   ├── GameController.java          # Screen navigation
│   ├── GameGUI.java                 # JFrame with CardLayout
│   ├── BaseGameScreen.java          # Abstract screen base
│   ├── MainMenuScreen.java          # Title screen
│   ├── NameEntryScreen.java         # Name input
│   ├── DialogueScreen.java          # CAPTAIN dialogue
│   ├── GamePlayScreen.java          # Status screen
│   ├── DoorSelectionScreen.java     # Door selection
│   ├── OptionsScreen.java           # Settings
│   ├── PongMinigame.java            # Pong game
│   ├── SpaceInvadersMinigame.java   # Space Invaders game
│   ├── DiceSystem.java              # Dice logic + art
│   ├── GameSettings.java            # Difficulty settings
│   ├── GameEvent.java               # Observer event
│   ├── GameEventListener.java       # Observer interface
│   ├── Item.java                    # Collectible items
│   ├── TextUI.java                  # Terminal UI utilities
│   ├── SoundManager.java            # WAV sound management
│   ├── SoundScreen.java             # In-game sound settings panel
│   ├── SoundSettings.java           # Per-sound volume storage
│   ├── CRTScreen.java               # Full-screen CRT display settings page
│   └── CRTSettings.java             # CRT scanline/vignette overlay
├── resources/
│   ├── doors.txt                    # Door definitions
│   ├── GUI.txt                      # GUI assets
│   └── sound_effects/               # 34 WAV files
├── tests/
│   ├── GameTest.java                # 6 tests
│   ├── TestGameLogic.java           # 20 tests
│   ├── GameTestSuite.java           # 21 tests
│   ├── SimpleTestRunner.java
│   └── ManualTestRunner.java
├── Gradle/                         # Build system
├── README.md
├── REPORT.md
└── .gitignore
```

---

## How to Run

### Requirements

- Java 21 or higher (JDK 21 recommended)
- No external dependencies (Swing built-in)

### Run Game (Compile & Execute)

**GUI Mode (Default):**

```cmd
javac -d out -sourcepath src src/Main.java
java -cp out Main
```

**Text-Based Mode (Mandatory Coursework Requirement):**

```cmd
java -cp out Main --text
```

Runs a terminal-based UI with ASCII art, dice rolls, and text menus.

### Run Tests

Using Gradle:

```cmd
cd Gradle
test.bat
```

---

## Controls

| Screen | Action | Key |
|---|---|---|
| Main Menu | Navigate | ↑ ↓ / W S |
| Main Menu | Select | Enter |
| Name Entry | Type | Keyboard (1-15 chars) |
| Door Selection | Navigate | ← → / A D |
| Door Selection | Open | Enter |
| Pong | Move Paddle | ↑ ↓ / W S |
| Space Invaders | Move | ← → / A D |
| Space Invaders | Shoot | Space |

---

## Game Objective

Reach **500 EXP** before losing all 3 lives:

- **Reward Door** → + EXP
- **Penalty Door** → - EXP  
- **Nothing Door** → No change
- **Minigame Door** → Win = + EXP; Lose = -1 life

**Starting EXP (Dice Roll):** 1 – 2 → 50, 3 – 4 → 100, 5 – 6 → 200.

---

## Design Patterns

| Pattern | Class | Role | AI-Assisted |
|---|---|---|---|
| Singleton | `Game.java` | One shared game instance | No |
| Factory | `DoorFactory.java` | Creates doors from data | **Yes (Claude)** |
| Observer | `GameEventListener.java` | Event notification | No |

---

## AI Usage

**Context engineering** was essential for effective AI collaboration. By providing detailed context in each prompt — including existing code structure, Java constraints, Swing API specifics, and game state — the AI delivered highly relevant suggestions.

This project contains 31 Java source files. AI (Claude and Gemini) assisted with 15 files (50%) for GUI architecture, controls, minigame concepts, and difficulty scaling:

- **Claude** — GUI architecture, controls, smooth input handling  
  Assisted files: `GameGUI.java`, `GameController.java`, `PongMinigame.java`, `GameSettings.java`, `DiceSystem.java`, `BaseGameScreen.java`, `MainMenuScreen.java`, `NameEntryScreen.java`, `DialogueScreen.java`, `GamePlayScreen.java`, `DoorSelectionScreen.java`, `OptionsScreen.java`, `SpaceInvadersMinigame.java`, `CRTSettings.java`, `SoundManager.java`.

- **Gemini** — Minigame suggestions (Pong, Space Invaders), initial Poison Door ASCII art  
  Assisted files: `PongMinigame.java`, `SpaceInvadersMinigame.java`, `DoorSelectionScreen.java`

---

## Assumptions

- Difficulty scales with EXP: ≤200 Easy, 201–350 Normal, >350 Hard
- `doors.txt` must exist; `DoorFactory` falls back to hardcoded doors on error
- Sound files are optional — missing files won't crash the game
- WAV filenames must match `SoundManager.java` constants exactly
- No persistent storage or external API calls

---

## Sound Setup

Place all `.wav` files inside:

```
resources/sound_effects/
```

The folder must be named exactly `sound_effects` (lowercase, underscore).

All 34 WAV mappings are defined in `SoundManager.java`. If a file is missing, the sound is silently skipped — the game will not crash.

**Note:** Only standard PCM WAV files (44.1kHz/22.05kHz) work with `javax.sound.sampled`. Use Audacity or FFmpeg to convert other formats.

### Sound levels

The 34 clips were recorded and exported at different times and were not close to
a common level — the quietest sat at 6% of the loudest, which is far enough
below the rest to be inaudible in play. They are now mapped by range compression
onto a floor of 20% of the loudest clip, so nothing is too quiet while every
effect keeps its own relative level.

`sound_volumes.json` at the coursework root records every clip's format, level
and gain before and after, and is regenerated by:

```
.venv/Scripts/python.exe scripts/normalize_sound_volumes.py
```

Two details are worth knowing before editing that script:

- **The clips are not all the same format.** They are 8-bit, 16-bit and 24-bit
  PCM, mono and stereo, at 11025, 44100 and 48000 Hz, so each has to be decoded
  and re-encoded at its own width. Reading them all as 16-bit shifts every
  sample after the first in a 24-bit frame and quietly destroys the file.
- **Level is judged on RMS gated to 50 dB below each clip's own peak**, not on
  plain RMS. `Main Menu GUI.wav` is 88% silence around a short burst, so its
  plain RMS is the lowest in the folder while its peak is -3.50 dBFS — it is not
  quiet, and ranking it by plain RMS asks for a boost that only a hard limiter
  could deliver.

Peaks rest at the -1 dBFS ceiling by design and never reach full scale, so
nothing is hard clipped. `python/` and `java/` hold byte-identical copies and
are rewritten together; `tests/test_university_courseworks/test_sound_asset_levels.py`
re-measures the clips from disk and fails if they diverge, if any clip is at
full scale, or if the floor slips below 20%.

---

## Cross-language parity cases

`ai_parity_cases.json` at the coursework root holds thirteen cases that describe
behaviour both implementations share. Java is the original and the reference;
Python is the port and the emphasis, because it is the project's main language.
Each case names one behaviour, one shared expectation, the Java class and method
that produce it, and the steps in plain language so neither side gets a case
phrased in the other's terms.

The cases live in a file both languages can read rather than inside the Python
test file, because the point is comparison: written inside the Python suite they
would be Python's opinion of the Java original, checked by Python, and true by
construction. From the file they are a claim about the Java that Python has to
match, and a JUnit suite can be pointed at the same list.

`tests/test_university_courseworks/test_ai_parity.py` runs every case against
the Python modules and checks the Java half statically — the named class exists,
the named method is public in it — so the Java side cannot rot without a test
failing, even though no Java was written for these cases.

---

## OOP Compliance

- **Encapsulation:** All fields private with getters/setters (`Player.java`, `Door.java`)
- **Inheritance:** `Door` abstract base → `RewardDoor`, `PenaltyDoor`, `NothingDoor`, `MinigameDoor`
- **Polymorphism:** `door.interact(player)` behaves differently per subclass
- **Abstraction:** `BaseGameScreen` abstract class for shared screen logic
- **Composition:** `Game` has `Player`, `Player` has `Item` inventory

---

## Text-Based UI (Coursework Requirement)

The game provides a **text-based user interface** using ASCII art and terminal menus:

- Launched via `java -cp out Main --text`
- Uses `TextUI.java` for box-drawn menus and prompts
- Dice rolls display ASCII art dice faces
- Resembles Pokemon Red-style text UI with ASCII graphics
- GUI mode also uses extensive ASCII art (chest, poison, helmet, pong, space invaders)
