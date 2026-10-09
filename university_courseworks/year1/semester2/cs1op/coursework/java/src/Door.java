// Door Abstract Class - Base Class for All Door Types

public abstract class Door {

    // Door Name
    protected String name;

    // Door Description
    protected String description;

    // Constructor
    public Door(String name, String description) {
        this.name = name;
        this.description = description;
    }

    // Gets Door Name
    public String getName() {
        return name;
    }

    // Gets Door Description
    public String getDescription() {
        return description;
    }

    // Interacts with Door (Returns Result Message)
    public abstract String interact(Player player);
}