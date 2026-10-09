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
│   └── CRTSettings.java             # CRT scanline/vignette overlay
├── resources/
│   ├── doors.txt                    # Door definitions
│   ├── GUI.txt                      # GUI assets
│   └── Sound Effects/               # 34 WAV files
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

This project contains 30 Java source files. AI (Claude and Gemini) assisted with 15 files (50%) for GUI architecture, controls, minigame concepts, and difficulty scaling:

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

## Sound Effects Setup

Place all `.wav` files inside:

```
resources/Sound Effects/
```

The folder must be named exactly `Sound Effects` (capital S + space).

All 34 WAV mappings are defined in `SoundManager.java`. If a file is missing, the sound is silently skipped — the game will not crash.

**Note:** Only standard PCM WAV files (44.1kHz/22.05kHz) work with `javax.sound.sampled`. Use Audacity or FFmpeg to convert other formats.

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
