// Player Class - Manages Player State and Progression

import java.util.ArrayList;
import java.util.List;

public class Player {

    // Player Name
    private final String name;

    // Player Experience Points
    private int exp;

    // Player Lives Remaining
    private int lives;

    // Player Inventory for Collected Items
    private final List<Item> inventory;

    // Reference to Game (for Observer Pattern) - Injected to Reduce Coupling
    private Game game;

    // Constructor with Default 0 EXP
    public Player(String name) {
        this(name, 0);
    }

    // Constructor with Custom Starting EXP
    public Player(String name, int startingExp) {
        this.name = name;
        this.exp = startingExp;
        this.lives = 3;
        this.inventory = new ArrayList<>();
        this.game = Game.getInstance();
    }

    // Constructor with Game Reference for Dependency Injection
    public Player(String name, int startingExp, Game game) {
        this.name = name;
        this.exp = startingExp;
        this.lives = 3;
        this.inventory = new ArrayList<>();
        this.game = game;
    }

    // Set the Game Reference (for Dependency Injection)
    public void setGame(Game game) {
        this.game = game;
    }

    // Get the Game Reference
    private Game getGame() {
        if (game == null) {
            game = Game.getInstance();
        }
        return game;
    }

    // Set EXP to a Specific Value
    public void setExp(int exp) {
        this.exp = exp;
        getGame().notifyListeners(new GameEvent(GameEvent.Type.EXP_CHANGED, this));
    }

    // Add EXP to Current Total
    public void addExp(int amount) {
        this.exp += amount;
        getGame().notifyListeners(new GameEvent(GameEvent.Type.EXP_CHANGED, this));
    }

    // Subtract EXP from Current Total
    public void subtractExp(int amount) {
        this.exp -= amount;
        getGame().notifyListeners(new GameEvent(GameEvent.Type.EXP_CHANGED, this));
    }

    // Get Player Name
    public String getName() {
        return name;
    }

    // Get Current EXP
    public int getExp() {
        return exp;
    }

    // Get Remaining Lives
    public int getLives() {
        return lives;
    }

    // Lose One Life (Minimum 0)
    public void loseLife() {
        lives = Math.max(0, lives - 1);
        getGame().notifyListeners(new GameEvent(GameEvent.Type.LIFE_LOST, this));
    }

    // Check if Game is Over
    public boolean isGameOver() {
        return lives <= 0 || exp < 0;
    }

    // Change EXP by Delta Amount
    public void changeExp(int delta) {
        exp += delta;
        getGame().notifyListeners(new GameEvent(GameEvent.Type.EXP_CHANGED, this));
    }

    // Check if Player is Bankrupt (Negative EXP)
    public boolean isBankrupt() {
        return exp < 0;
    }

    // Add Item to Inventory
    public void addItem(Item item) {
        inventory.add(item);
        getGame().notifyListeners(new GameEvent(GameEvent.Type.ITEM_COLLECTED, item));
    }

    // Check if Player has Specific Item
    public boolean hasItem(String itemName) {
        return inventory.stream().anyMatch(i -> i.getName().equalsIgnoreCase(itemName));
    }

    // Get player inventory
    public List<Item> getInventory() {
        return inventory;
    }
}