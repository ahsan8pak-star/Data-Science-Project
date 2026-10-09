# CS1OP Project Report #

**Module Code:** CS1OP

**Assignment Title:** Project

**Student Number:** om001219

**Actual hours spent:** ~150 hours

**AI tools used:** Claude (Anthropic), Gemini (Google)

**Repository URL:** <https://csgitlab.reading.ac.uk/om001219/CS1OP-TextGame>

---

## 1. Introduction (10%) #

Space Mission is a Java GUI Sci-Fi adventure game built using Swing Utilities, with a retro green-on-black aesthetic inspired by Geometry Wars 2 (found in Project Gotham Racing 4 arcade machines across all 4 garages - Amateur, Professional, Hot Shot and Master). The player wakes up in orbit aboard a space station and must accumulate **500 EXP** by opening mystery doors. Each door delivers an EXP reward, penalty, or triggers a minigame challenge.

The project addresses 4 learning outcomes: decomposing a problem into multiple classes using design patterns; demonstrating encapsulation, polymorphism, abstraction, and inheritance; evaluating OOP design trade-offs; and communicating the solution through GitLab and markdown documentation.

The game includes 2 fully playable minigames (Pong and Space Invaders), a branching dialogue system with ASCII art, a dice-based starting EXP mechanic, and 3 difficulty levels. 30 classes implement the complete game loop, covering GUI management, game logic, door mechanics, minigame engines, event handling, sound management, and testing infrastructure. All 47 JUnit tests pass.

The game provides 2 UI modes to satisfy coursework requirements:

- **GUI Mode** (default): Swing-based interface with extensive ASCII art (chest, poison, helmet, pong, space invaders)
- **Text Mode** (`--text`): Terminal-based UI using `TextUI.java` with box-drawn menus, ASCII dice, and text prompts

---

## 2. Analysis of AI Support in Software Development (25%) #

### How AI Tools Were Used #

Context engineering played a crucial role in maximising AI effectiveness. By carefully crafting prompts with specific context — including existing code structure, Java version (JDK 21), the Swing API constraints, and the game mechanics already implemented — I was able to get highly relevant suggestions that required minimal adaptation. This iterative approach of providing context, receiving suggestions, applying them, and refining the context for the next iteration was key to successful AI collaboration.

The project consists of 30 Java source files. AI (Claude and Gemini) assisted with 15 files (50%) related to GUI architecture, controls, minigame concepts, and difficulty scaling. The remaining 15 files covering game logic (Game classes, Player, Door classes, Event system, SoundManager, and Item) were implemented independently.

**Claude (Anthropic) assisted in 5 specific areas:**

1. **GUI Architecture** — Advised on using `CardLayout` inside a single `JFrame` so that screens (main menu, name entry, dialogue, door selection, minigames) could be swapped without creating and destroying windows. Assisted files: `GameGUI.java`, `GameController.java`.

2. **Smooth Pong Controls** — Suggested replacing `KeyListener.keyTyped` with a persistent `Set<Integer>` of currently held keys, sampled every frame. Assisted file: `PongMinigame.java`.

3. **Difficulty Scaling** — Proposed EXP thresholds (≤200 / 201–350 / >350) to drive 3 distinct difficulty bands across both minigames. Assisted file: `GameSettings.java`.

4. **DiceSystem Logic** — Generated the initial dice-rolling scaffold and ASCII dice-face arrays. Assisted file: `DiceSystem.java`.

5. **Inheritance Hierarchy** — Recommended the `BaseGameScreen` abstract class to centralise shared constants, border-drawing utilities, and anti-aliasing setup. Assisted files: `BaseGameScreen.java`, `MainMenuScreen.java`, `NameEntryScreen.java`, `DialogueScreen.java`, `GamePlayScreen.java`, `DoorSelectionScreen.java`, `OptionsScreen.java`.

**Gemini (Google)** was consulted for suggesting the minigames (Pong and Space Invaders) and generating the initial concepts for the Poison Door and Door Selection ASCII art. Gemini acted as a guide, while the actual ASCII art conversion was performed using **ASCII Art EU** (<https://asciiart.eu>), a web-based image-to-ASCII converter — this is not an AI tool but a reference utility used for generating Chest, Reward, Nothing, Pong/Space Invaders, and Astronaut Helmet ASCII art.

### Major Update: Terminal to GUI Transition #

After setting up the basics of terminal-based programming, I transitioned to a full GUI implementation:

**New GUI Files Created:**

```
src/
├── BaseGameScreen.java
├── CRTSettings.java
├── DialogueScreen.java
├── DiceSystem.java
├── DoorFactory.java
├── DoorSelectionScreen.java
├── GameController.java
├── GameEvent.java
├── GameEventListener.java
├── GameGUI.java
├── GamePlayScreen.java
├── GameSettings.java
├── MainMenuScreen.java
├── MinigameDoor.java
├── NameEntryScreen.java
├── NothingDoor.java
├── OptionsScreen.java
├── PenaltyDoor.java
├── PongMinigame.java
├── RewardDoor.java
├── SpaceInvadersMinigame.java
├── SoundManager.java
├── SoundScreen.java
├── SoundSettings.java
└── TextUI.java

tests/
├── GameTest.java
├── GameTestSuite.java
├── ManualTestRunner.java
├── SimpleTestRunner.java
└── TestGameLogic.java
```

I implemented Gradle to successfully run JUnit tests, which allowed structuring src, resources, and tests folders properly. The project structure follows the coursework guidelines with Gradle as the build tool. The project evolved from a terminal-based game to a full GUI application with smooth, event-driven input handling via key-state tracking.

### Benefits of AI Tools #

AI reduced implementation time on the most technically complex features. The key-state approach for Pong input was a direct improvement over standard event-driven input. The `CardLayout` architecture gave a clean, extensible screen management system, avoiding the common pitfall of multiple `JFrame` windows.

### Challenges and Limitations #

All AI-generated code required substantial adaptation. The Swing API calls in early suggestions were often incorrect for Java 21 and required manual correction. Visual output (ASCII art alignment, screen layout) required iterative manual testing — AI could not validate visual correctness.

AI did not generate test cases — all 47 JUnit tests were written independently.

### Overall Impact #

AI was treated as a senior developer consultant rather than a code generator. Out of 30 source files, 15 files (50%) received AI assistance for GUI architecture, controls, minigame concepts, and difficulty scaling. All game logic, door mechanics, event system, sound management, and tests were implemented independently. This approach maintained academic integrity while accelerating development.

---

## 3. Analysis of Software Patterns in the Project (25%) #

Per coursework requirements, **at least one design pattern (the Factory Pattern) was implemented with AI assistance (Claude)**, documented in Section 2.

### Singleton Pattern — Game.java #

`Game` is the central authority for game state using lazy instantiation:

```java
private static Game instance;

public static Game getInstance() {
    if (instance == null) {
        instance = new Game();
    }
    return instance;
}
```

This ensures a single shared game state across all screens and components.

**Benefits:** Eliminates passing Game reference through every constructor. Guarantees consistent state across all screens.

**Drawbacks:** Global mutable state introduces tight coupling and makes testing in isolation difficult.

### Factory Pattern — DoorFactory.java #

`DoorFactory` reads type tokens from `resources/doors.txt` and instantiates appropriate `Door` subclasses:

```java
return switch (type) {
    case "reward" -> new RewardDoor(...);
    case "penalty" -> new PenaltyDoor(...);
    case "minigame" -> new MinigameDoor(...);
    default -> createFallbackDoor(index);
};
```

**Benefits:** Door configuration lives in external data file, not source code. Adding new door types requires only a new class and case branch.

**Drawbacks:** Parsing adds I/O complexity and potential failure points if file format changes.

### Observer Pattern — GameEventListener.java / GameEvent.java #

`GameEvent` carries typed payloads (`EXP_CHANGED`, `LIFE_LOST`, `ITEM_COLLECTED`, `DOOR_CHOSEN`, `MINIGAME_STARTED`). Player methods call `notifyListeners` after each state change.

**Benefits:** Player and UI are decoupled. Multiple listeners can register simultaneously. Adding new listeners requires no changes to Player.

**Drawbacks:** Event ordering is implicit. Listeners not removed would cause memory leaks.

### Overall Pattern Impact #

3 patterns work together: Singleton provides the instance that Factory populates with doors and Observer keeps synchronized with the UI.

---

## 4. Ethical and Legal Considerations (20%) #

### Benefits of AI Tools #

1. **Accelerated Development** — AI reduced time on complex GUI architecture decisions, allowing focus on game logic implementation.

2. **Architectural Guidance** — `CardLayout` provided a clean screen management system that would have taken significant research to discover independently.

3. **Control Optimization** — The key-state input pattern for Pong (tracking held keys rather than individual `keyTyped` events) improves gameplay feel — a pattern AI suggested that is now standard in game development.

4. **Pattern Introduction** — Exposed design patterns (Factory, Singleton, Observer) apply in real code, reinforcing academic learning.

5. **Error Prevention** — AI flagged potential issues (e.g., thread safety in Swing) that would have caused bugs later.

### Drawbacks of AI Tools #

1. **Code Adaptation Required** — All AI suggestions required manual correction for Java 21 compatibility. Swing API calls were often outdated or incorrect.

2. **Visual Validation Impossible** — AI cannot validate ASCII art alignment or screen layout. All graphics required iterative manual testing — no way to verify correctness programmatically.

3. **Learning Risk** — Over-reliance on AI for solutions rather than understanding concepts undermines the academic purpose. Every AI suggestion was reviewed to understand *why* before integration.

4. **Debugging Complexity** — AI-generated code structure can be unfamiliar, making debugging harder than self-written code.

5. **No Testing Assistance** — All 47 JUnit tests were written independently. AI could not generate context-specific test cases for this project.

### Application to This Coursework #

This coursework required demonstrating OOP principles (encapsulation, polymorphism, abstraction, inheritance) and design patterns. AI was used as a *consultant* — receiving context and providing suggestions — rather than a sole *code generator*. Out of 30 source files, 15 files (50%) received AI assistance for GUI architecture, controls, and difficulty scaling. All game logic, door mechanics, event system, sound management, test cases (47 total), and core OOP implementations were developed independently.

The Factory Pattern implementation involved AI assistance (Claude helped design the switch-based instantiation), satisfying the requirement that at least one pattern involve AI collaboration.

### Data Privacy #

The game collects only the player's name, existing only in JVM heap memory for the session duration — never written to disk or transmitted. No external API calls, cookies, or persistent storage. GDPR compliance is satisfied.

### Accessibility #

The green-on-black colour scheme is high contrast, inspired by Geometry Wars 2. All interactive elements support keyboard-only navigation. ASCII art provides text-based visual feedback.

### Licensing #

The project uses only Java Standard Library (Oracle BCL) and JUnit 5 (Eclipse Public License 2.0). Both permit academic use. Pong and Space Invaders mechanics are in the public domain. No third-party assets with restrictive licenses are included.

---

## 5. Conclusion (10%) #

The project successfully delivers a complete Java game demonstrating OOP principles. 30 classes implement encapsulation, polymorphism, abstraction, and inheritance through abstract bases (`Door`, `BaseGameScreen`) and interfaces (`GameEventListener`).

Three design patterns — Singleton, Factory, and Observer — are correctly implemented with trade-off analysis. Factory was implemented with AI assistance (Claude helped design the switch-based instantiation), satisfying the requirement that at least one pattern involve AI.

`SoundManager.java` manages 34 WAV sound effects using `javax.sound.sampled`. All playback is wrapped in try-catch blocks to prevent crashes. Sounds are organised in `resources/Sound Effects/`.

The game handles invalid inputs gracefully: `NameEntryScreen` enforces character limits; `DoorFactory` falls back to hard-coded doors on file errors; a global `UncaughtExceptionHandler` prevents silent crashes.

**Text-Based UI Requirement:** The game provides 2 modes:

- **GUI Mode** (default): Launched via `java -cp out Main` — uses Swing with ASCII art
- **Text Mode**: Launched via `java -cp out Main --text` — uses `TextUI.java` with box-drawn menus

47 JUnit Tests verify core logic. All tests pass flawlessly.

Future improvements would include file-based persistence and high-contrast accessibility mode.

---

## 6. References (10%) #

- Atari. (1972). *Pong*. <https://en.wikipedia.org/wiki/Pong> — Classic Arcade Tennis Game that inspired the Pong Minigame.

- Taito. (1978). *Space Invaders*. <https://en.wikipedia.org/wiki/Space_Invaders> — Classic Arcade Shooter Game that inspired the Space Invaders Minigame.

- Bizarre Creations. (2007). *Geometry Wars: Retro Evolved 2*. Visual Design Inspiration from Project Gotham Racing 4 Arcade Machines scattered across all 4 Garages - Amateur, Professional, Hot Shot, Master.

- ASCII Art EU. (2026). <https://www.asciiart.eu/image-to-ascii> — Image to ASCII converter for Art Assets.

- Oracle. (2026). *Java Swing Tutorial*. <https://docs.oracle.com/javase/tutorial/uiswing/>

- JUnit Team. (2026). *JUnit 5 User Guide*. <https://junit.org/junit5/docs/current/user-guide/>

- Anthropic. (2026). *Claude AI*. <https://www.claude.ai> — used for GUI architecture, Pong controls, difficulty scaling, and inheritance design.

- Google. (2026). *Gemini AI*. <https://gemini.google.com> — used for minigame suggestions and Poison Door ASCII art.

---

## Testing Evidence #

### Test Suite Summary #

| Class | Tests | Result |
|---|---|---|
| GameTest.java | 6 | All Passed |
| TestGameLogic.java | 20 | All Passed |
| GameTestSuite.java | 21 | All Passed |
| **Total** | **47** | **100%** |

### Key Test Cases #

- `testSingletonPattern` — asserts Game.getInstance() returns the same object
- `testFactoryPattern` — asserts DoorFactory never returns null
- `testObserverPattern` — verifies listeners receive events
- `testPlayerCreation` — verifies starting EXP
- `testChangeExp` — verifies EXP arithmetic
- `testDoorInteract` — verifies door interaction returns valid output

### Test Run Output #

```
Tests run: 47, Failures: 0, Errors: 0, Skipped: 0
BUILD SUCCESS
```

### Test Evidence Log #

A detailed test evidence log (`test-results.log`) is included in the repository root, containing:

- Test file listing
- @Test annotation counts per file (47 total)
- Key test case descriptions
- Compilation verification
- Test framework information (JUnit 5)

### Running Tests #

```cmd
cd Gradle
test.bat
```
