// NothingDoor Class - A Door that Reveals Nothing and Does Not Change EXP

public class NothingDoor extends Door {
    public NothingDoor(String name, String description) {
        super(name, description);
    }

    @Override
    public String interact(Player player) {
        return "The door reveals nothing. Just empty space.";
    }
}