// RewardDoor Class - Door that Grants EXP to Player

public class RewardDoor extends Door {

    // EXP value to grant
    private final int exp;

    // Constructor
    public RewardDoor(String name, String description, int exp) {
        super(name, description);
        this.exp = exp;
    }

    // Get the EXP value
    public int getExpValue() {
        return exp;
    }

    // Interact with door - grants EXP
    @Override
    public String interact(Player player) {
        player.changeExp(exp);
        return "You gained " + exp + " EXP!";
    }
}
