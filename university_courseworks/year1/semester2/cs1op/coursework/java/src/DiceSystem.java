// DiceSystem Class - Handles Dice Rolling Mechanics with Almost Symmetrical ASCII art

import java.util.Random;

public class DiceSystem {

    // Last Rolled Value
    private int lastRoll = 0;

    // Random Number Generator
    private final Random random = new Random();

    // Roll Dice (returns 1-6)
    public int roll() {
        lastRoll = random.nextInt(6) + 1;
        return lastRoll;
    }

    // Gets Last Rolled Value
    public int getLastRoll() {
        return lastRoll;
    }

    // Gets HP based on Dice Roll - 1-2 = 50 HP, 3-4 = 100 HP, 5-6 = 200 HP
    public int getHPFromRoll(int diceValue) {
        if (diceValue <= 2)
            return 50;
        if (diceValue <= 4)
            return 100;
        return 200;
    }

    // Gets Door Bonus based on Dice Roll
    // 1-2 = base value (1x)
    // 3-4 = base value * 2 (2x)
    // 5-6 = base value * 4 (4x)
    public int getDoorBonusFromRoll(int diceValue, int baseValue) {
        if (diceValue <= 2)
            return baseValue;
        if (diceValue <= 4)
            return baseValue * 2;
        return baseValue * 4;
    }

    // Gets ASCII Art Array for a Specific Dice Face - Switch Case
    public String[] getDiceFaceArray(int face) {
        return switch (face) {
            case 1 -> DICE_1;
            case 2 -> DICE_2;
            case 3 -> DICE_3;
            case 4 -> DICE_4;
            case 5 -> DICE_5;
            case 6 -> DICE_6;
            default -> DICE_BLANK;
        };
    }

    // Gets ASCII Art for Current Roll
    public String[] getCurrentDiceArray() {
        return getDiceFaceArray(lastRoll);
    }

    // Near Symmetrical Dice Faces - Centered in 11x7 Boxes
    private static final String[] DICE_1 = {
            " ╔═════════════╗ ",
            " ║           ║ ",
            " ║           ║ ",
            " ║     ●     ║ ",
            " ║           ║ ",
            " ║           ║ ",
            " ╚═════════════╝ "
    };

    private static final String[] DICE_2 = {
            " ╔═════════════╗ ",
            " ║ ●         ║ ",
            " ║           ║ ",
            " ║           ║ ",
            " ║           ║ ",
            " ║        ●  ║ ",
            " ╚═════════════╝ "
    };

    private static final String[] DICE_3 = {
            " ╔═════════════╗ ",
            " ║  ●        ║ ",
            " ║           ║ ",
            " ║     ●     ║ ",
            " ║           ║ ",
            " ║        ●  ║ ",
            " ╚═════════════╝ "
    };

    private static final String[] DICE_4 = {
            " ╔═════════════╗ ",
            " ║ ●      ● ║ ",
            " ║           ║ ",
            " ║           ║ ",
            " ║           ║ ",
            " ║ ●      ● ║ ",
            " ╚═════════════╝ "
    };

    private static final String[] DICE_5 = {
            " ╔═════════════╗ ",
            " ║ ●      ● ║ ",
            " ║           ║ ",
            " ║     ●     ║ ",
            " ║           ║ ",
            " ║ ●      ● ║ ",
            " ╚═════════════╝ "
    };

    private static final String[] DICE_6 = {
            " ╔═════════════╗ ",
            " ║ ●      ● ║ ",
            " ║           ║ ",
            " ║ ●      ● ║ ",
            " ║           ║ ",
            " ║ ●      ● ║ ",
            " ╚═════════════╝ "
    };

    private static final String[] DICE_BLANK = {
            " ╔═════════════╗ ",
            " ║             ║ ",
            " ║             ║ ",
            " ║             ║ ",
            " ║             ║ ",
            " ║             ║ ",
            " ╚═════════════╝ "
    };

    // Legacy Method for Compatibility
    public String getDiceFaceASCII() {
        String[] face = getCurrentDiceArray();
        StringBuilder sb = new StringBuilder();
        for (String line : face) {
            sb.append(line).append("\n");
        }
        return sb.toString();
    }
}