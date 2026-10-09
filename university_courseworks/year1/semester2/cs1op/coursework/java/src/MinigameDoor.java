// MinigameDoor Class - Door that Leads to Minigame

public class MinigameDoor extends Door {

    // Type of Minigame (PONG or SPACE_INVADERS)
    private String gameType;

    // Constructor
    public MinigameDoor(String name, String description, String gameType) {
        super(name, description);
        this.gameType = gameType;
    }

    // Get minigame type
    public String getGameType() {
        return gameType;
    }

    // Interact with door - placeholder for minigame
    @Override
    public String interact(Player player) {
        return "You enter the spaceship!";
    }
}
