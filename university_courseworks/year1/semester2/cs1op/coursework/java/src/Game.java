// Game Class - Singleton Pattern Implementation
// Manages Game State, Doors, and Event Listeners

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;
import java.util.Scanner;

public class Game {

    // Win Condition EXP Threshold
    private static final int WIN_EXP = 500;

    // Maximum Player Name Length
    private static final int MAX_NAME_LENGTH = 15;

    // Singleton Instance
    private static Game instance;

    // Current Player
    private Player player;

    // List of Event Listeners for Observer Pattern
    private final List<GameEventListener> listeners = new ArrayList<>();

    // List of Doors for the Current Round
    private final List<Door> doors = new ArrayList<>();

    // Sound Toggle State
    private boolean soundOn = true;

    // Random Number Generator
    private final Random rnd = new Random();

    // Private Constructor for Singleton
    private Game() {
    }

    // Get Singleton Instance
    public static Game getInstance() {
        if (instance == null) {
            instance = new Game();
        }
        return instance;
    }

    // Reset Singleton for Replay
    public static void reset() {
        instance = new Game();
    }

    // Initialize Player for GUI Mode with Given Name
    public void initializePlayer(String name) {
        int startExp = rollStartingExp();
        player = new Player(name, startExp);
    }

    // Get Current Player
    public Player getPlayer() {
        return player;
    }

    // Add Event Listener
    public void addListener(GameEventListener l) {
        listeners.add(l);
    }

    // Notify All Listeners of an Event (Observer Pattern)
    public void notifyListeners(GameEvent e) {
        for (GameEventListener l : listeners) {
            l.onEvent(e);
        }
    }

    // Start the Text-Based Game
    @SuppressWarnings("incomplete-switch")
    public void start() {
        Scanner sc = new Scanner(System.in);
        TextUI.box("SPACE DOOR ADVENTURE", "A small text-based sci-fi roguelike.", "Navigate doors to earn EXP.");
        String name = getValidName(sc);
        int startExp = rollStartingExp();
        player = new Player(name, startExp);
        TextUI.box("Starting EXP", "You rolled the dice and start with " + startExp + " EXP.");

        addListener(event -> {
            switch (event.getType()) {
                case EXP_CHANGED -> {
                    if (soundOn)
                        System.out.println("[SFX] EXP updated.");
                    System.out.println("[DEBUG] EXP now " + ((Player) event.getPayload()).getExp());
                }
                case LIFE_LOST -> {
                    if (soundOn)
                        System.out.println("[SFX] Life lost!");
                    System.out.println("[DEBUG] Lives left " + ((Player) event.getPayload()).getLives());
                    handleLifeLoss();
                }
                case DOOR_CHOSEN -> {
                    if (soundOn)
                        System.out.println("[SFX] Door opening...");
                    System.out.println("[DEBUG] Door chosen: " + ((Door) event.getPayload()).getName());
                }
                case MINIGAME_STARTED -> {
                    if (soundOn)
                        System.out.println("[SFX] Launching minigame...");
                    System.out.println("[DEBUG] Minigame starting...");
                }
            }
        });

        mainMenu(sc);
    }

    // Get Valid Player Name with Length Validation
    private String getValidName(Scanner sc) {
        while (true) {
            System.out.print("Enter your name (1-" + MAX_NAME_LENGTH + " chars): ");
            String name = sc.nextLine().trim();
            if (name.isEmpty()) {
                TextUI.box("Invalid", "Name cannot be empty.");
            } else if (name.length() > MAX_NAME_LENGTH) {
                TextUI.box("Invalid", "Name too long. Maximum " + MAX_NAME_LENGTH + " characters.");
            } else {
                return name;
            }
        }
    }

    // Display Main Menu
    private void mainMenu(Scanner sc) {
        while (true) {
            TextUI.box("MAIN MENU", "1) Play", "2) Toggle sound (" + (soundOn ? "On" : "Off") + ")", "3) Quit");
            String choice = TextUI.prompt("Choose an option:");

            if (choice.equals("1")) {
                setupDoors();
                playLoop(sc);
                break;
            } else if (choice.equals("2")) {
                soundOn = !soundOn;
                TextUI.box("Sound", "Sound is now " + (soundOn ? "On" : "Off"));
            } else if (choice.equals("3") || choice.equalsIgnoreCase("q")) {
                TextUI.box("Exit", "Thanks for playing!");
                break;
            } else {
                TextUI.box("Invalid", "Please choose 1, 2, or 3.");
            }
        }
    }

    // Setup 5 Random Doors for Gameplay
    private void setupDoors() {
        DoorFactory factory = new DoorFactory();
        doors.clear();
        for (int i = 1; i <= 5; i++) {
            doors.add(factory.createRandomDoor(i));
        }
    }

    // Roll for starting EXP based on dice
    private int rollStartingExp() {
        int roll = rnd.nextInt(6) + 1;
        return switch (roll) {
            case 1 -> showDiceRoll(roll, "+-----+\n|     |\n|  o  |\n|     |\n+-----+", 50);
            case 2 -> showDiceRoll(roll, "+-----+\n|o    |\n|     |\n|    o|\n+-----+", 50);
            case 3 -> showDiceRoll(roll, "+-----+\n|o    |\n|  o  |\n|    o|\n+-----+", 100);
            case 4 -> showDiceRoll(roll, "+-----+\n|o   o|\n|     |\n|o   o|\n+-----+", 100);
            case 5 -> showDiceRoll(roll, "+-----+\n|o   o|\n|  o  |\n|o   o|\n+-----+", 200);
            case 6 -> showDiceRoll(roll, "+-----+\n|o   o|\n|o   o|\n|o   o|\n+-----+", 200);
            default -> showDiceRoll(roll, "+-----+\n|o   o|\n|o   o|\n|o   o|\n+-----+", 200);
        };
    }

    // Display dice roll result
    private int showDiceRoll(int roll, String art, int exp) {
        String[] lines = art.split("\\n");
        String[] all = new String[lines.length + 1];
        all[0] = "You rolled a " + roll + "!";
        System.arraycopy(lines, 0, all, 1, lines.length);
        TextUI.box("Dice Roll", all);
        return exp;
    }

    // Main gameplay loop
    private void playLoop(Scanner sc) {
        while (true) {
            if (player.getExp() >= WIN_EXP) {
                TextUI.box("VICTORY", "You have reached " + player.getExp() + " EXP!", "You win!");
                break;
            }
            if (player.isBankrupt() || player.getLives() <= 0) {
                TextUI.box("DEFEAT", "You have run out of EXP or lives.", "Game over.");
                break;
            }
            TextUI.box("STATUS", "Player: " + player.getName(), "EXP: " + player.getExp(),
                    "Lives: " + player.getLives());
            TextUI.box("DOOR SELECTION", "Choose a door to open (1-" + doors.size() + ") or type QUIT:",
                    "Each door is randomized.");

            for (int i = 0; i < doors.size(); i++) {
                TextUI.box("Door " + (i + 1), "[??] " + doors.get(i).getDescription());
            }

            String choice = TextUI.prompt("Your choice:");

            if (choice.equalsIgnoreCase("quit")) {
                TextUI.box("Exit", "Thanks for playing!");
                break;
            }

            int sel;
            try {
                sel = Integer.parseInt(choice) - 1;
            } catch (NumberFormatException e) {
                TextUI.box("Invalid", "Please enter a number between 1 and " + doors.size() + ".");
                continue;
            }

            if (sel < 0 || sel >= doors.size()) {
                TextUI.box("Invalid", "No such door.");
                continue;
            }

            Door selected = doors.get(sel);
            notifyListeners(new GameEvent(GameEvent.Type.DOOR_CHOSEN, selected));
            TextUI.box("Door Opened", "You open door " + (sel + 1) + ": " + selected.getDescription());

            if (selected instanceof MinigameDoor) {
                notifyListeners(new GameEvent(GameEvent.Type.MINIGAME_STARTED, selected));
                MinigameDoor mgDoor = (MinigameDoor) selected;
                TextUI.box("Minigame", "Starting " + mgDoor.getGameType() + "! (Play in GUI version)");
                player.loseLife();
                setupDoors();
            } else {
                String result = selected.interact(player);
                TextUI.box("Result", result);
                if (player.isBankrupt()) {
                    TextUI.box("Bankrupt", "Your EXP fell below 0.");
                    break;
                }
                doors.set(sel, new DoorFactory().createRandomDoor(sel + 1));
            }
        }
    }

    // Handle life loss event with dice roll
    private void handleLifeLoss() {
        int roll = rnd.nextInt(6) + 1;
        String diceArt = getDiceArt(roll);
        List<String> lines = new ArrayList<>();
        lines.add("You rolled a " + roll + "!");
        lines.addAll(Arrays.asList(diceArt.split("\\n")));
        TextUI.box("Life Lost", lines);

        if (roll <= 4) {
            player.setExp(0);
            TextUI.box("EXP Lost", "Unlucky! Your EXP has been wiped out.", "Current EXP: " + player.getExp());
        } else {
            TextUI.box("EXP Saved", "Lucky! You keep your EXP.", "Current EXP: " + player.getExp());
        }
    }

    // Get ASCII art for dice face
    private String getDiceArt(int roll) {
        return switch (roll) {
            case 1 -> "+-----+\n|     |\n|  o  |\n|     |\n+-----+";
            case 2 -> "+-----+\n|o    |\n|     |\n|    o|\n+-----+";
            case 3 -> "+-----+\n|o    |\n|  o  |\n|    o|\n+-----+";
            case 4 -> "+-----+\n|o   o|\n|     |\n|o   o|\n+-----+";
            case 5 -> "+-----+\n|o   o|\n|  o  |\n|o   o|\n+-----+";
            case 6 -> "+-----+\n|o   o|\n|o   o|\n|o   o|\n+-----+";
            default -> "+-----+\n|o   o|\n|o   o|\n|o   o|\n+-----+";
        };
    }
}