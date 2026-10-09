// PenaltyDoor Class - Door that Takes EXP from Player

public class PenaltyDoor extends Door {

    // EXP value to deduct
    private final int exp;

    // Constructor
    public PenaltyDoor(String name, String description, int exp) {
        super(name, description);
        this.exp = exp;
    }

    // Get the penalty EXP value
    public int getExpValue() {
        return -exp; // Negative value for penalty
    }

    // Interact with door - deducts EXP
    @Override
    public String interact(Player player) {
        player.changeExp(-exp);
        return "You lost " + exp + " EXP.";
    }
}