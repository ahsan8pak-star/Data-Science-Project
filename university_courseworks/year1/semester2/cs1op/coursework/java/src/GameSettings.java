// GameSettings Class - Stores Global Game Settings (Difficulty)
// Accessed as a Static Class; No Instantiation Needed

public class GameSettings {

    public enum Difficulty {
        EASY, NORMAL, HARD
    }

    private static Difficulty difficulty = Difficulty.NORMAL;

    public static Difficulty getDifficulty() {
        return difficulty;
    }

    public static void setDifficulty(Difficulty d) {
        difficulty = d;
    }

    public static void cycleDifficulty() {
        difficulty = switch (difficulty) {
            case EASY -> Difficulty.NORMAL;
            case NORMAL -> Difficulty.HARD;
            case HARD -> Difficulty.EASY;
        };
    }

    public static String difficultyLabel() {
        return switch (difficulty) {
            case EASY -> "EASY";
            case NORMAL -> "NORMAL";
            case HARD -> "HARD";
        };
    }
}