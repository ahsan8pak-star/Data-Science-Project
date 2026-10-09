// GameController Class
// Links the GUI to Game Logic and Manages All Screen Transitions
// Handles Minigame Results - Win Grants EXP, Loss Deducts a Life
// Stops All Sounds on Major Screen Transitions to Prevent Audio Overlap

public class GameController {

    // Reference to the Main Game Window
    private final GameGUI gui;

    // The Currently Active Player
    private Player currentPlayer;

    // The Singleton Game State Instance
    private Game gameInstance;

    // Constructor
    public GameController(GameGUI gui) {
        this.gui = gui;
    }

    // Start a New Game Session by Navigating to Name Entry
    public void startGame() {
        SoundManager.stopAll();
        gui.showScreen("NAME_ENTRY");
    }

    // Show the Options Screen with Difficulty, CRT, Sound, Volume, and Back
    public void showOptions() {
        gui.addScreen(new OptionsScreen(gui, this), "OPTIONS");
        gui.showScreen("OPTIONS");
    }

    // Show the Full-Screen CRT Display Settings Page
    public void showCRTScreen() {
        gui.addScreen(new CRTScreen(gui, this), "CRT_SCREEN");
        gui.showScreen("CRT_SCREEN");
    }

    // Show the Individual Sound Volume Settings Screen
    public void showSoundScreen() {
        gui.addScreen(new SoundScreen(gui, this), "SOUND_SCREEN");
        gui.showScreen("SOUND_SCREEN");
    }

    // Return to the Main Menu and Stop All Sounds
    public void goBackToMainMenu() {
        SoundManager.stopAll();
        gui.showScreen("MAIN_MENU");
    }

    // Navigate to a Screen by Its Registered Name
    public void showScreen(String name) {
        gui.showScreen(name);
    }

    // Refresh and Show the Door Selection Screen
    public void startDoorSelection() {
        gui.addScreen(new DoorSelectionScreen(gui, this), "DOOR_SELECTION");
        gui.showScreen("DOOR_SELECTION");
    }

    // Create a New Player with the Given Name and Transition to the Dialogue Screen
    public void setPlayerName(String name) {
        gameInstance = Game.getInstance();
        gameInstance.initializePlayer(name);
        currentPlayer = gameInstance.getPlayer();
        gui.showScreen("DIALOGUE");
    }

    // Launch the Specified Minigame Screen
    public void startMinigame(String gameName) {
        if (currentPlayer == null || currentPlayer.getLives() <= 0) {
            gui.showScreen("GAMEPLAY");
            return;
        }

        SoundManager.stopAll();

        if ("PONG".equals(gameName)) {
            gui.addScreen(new PongMinigame(this), "MINIGAME_PONG");
            gui.showScreen("MINIGAME_PONG");
        } else if ("SPACE_INVADERS".equals(gameName)) {
            gui.addScreen(new SpaceInvadersMinigame(this), "MINIGAME_SPACE_INVADERS");
            gui.showScreen("MINIGAME_SPACE_INVADERS");
        }
    }

    // Called When the Player Wins a Minigame
    public void onMinigameWon(String gameType, int expGained) {
        SoundManager.stopAll();
        gui.removeScreen("MINIGAME_PONG");
        gui.removeScreen("MINIGAME_SPACE_INVADERS");

        if (currentPlayer != null) {
            currentPlayer.addExp(expGained);
        }

        checkWinLossOrContinue();
    }

    // Called When the Player Loses a Minigame
    public void onMinigameLost() {
        SoundManager.stopAll();
        gui.removeScreen("MINIGAME_PONG");
        gui.removeScreen("MINIGAME_SPACE_INVADERS");

        if (currentPlayer != null) {
            SoundManager.playOnce(SoundManager.LIFE_LOST);
            currentPlayer.loseLife();
        }

        checkWinLossOrContinue();
    }

    // Evaluate Win/Loss Conditions and Navigate Accordingly
    private void checkWinLossOrContinue() {
        if (currentPlayer == null) {
            gui.showScreen("MAIN_MENU");
            return;
        }

        if (currentPlayer.getExp() >= 500
                || currentPlayer.getLives() <= 0
                || currentPlayer.getExp() < 0) {
            gui.showScreen("GAMEPLAY");
        } else {
            startDoorSelection();
        }
    }

    // End the Game and Return to the Main Menu
    public void gameOver() {
        SoundManager.stopAll();
        gui.showScreen("MAIN_MENU");
    }

    // Get the Currently Active Player
    public Player getCurrentPlayer() {
        return currentPlayer;
    }
}