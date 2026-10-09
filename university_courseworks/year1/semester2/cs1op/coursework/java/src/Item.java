// Item Class - Represents Collectible Items in the Game

public class Item {

    // Item name
    private final String name;

    // Item description
    private final String description;

    // Constructor
    public Item(String name, String description) {
        this.name = name;
        this.description = description;
    }

    // Get item name
    public String getName() {
        return name;
    }

    // Get item description
    public String getDescription() {
        return description;
    }

    // String representation
    @Override
    public String toString() {
        return name + ": " + description;
    }
}