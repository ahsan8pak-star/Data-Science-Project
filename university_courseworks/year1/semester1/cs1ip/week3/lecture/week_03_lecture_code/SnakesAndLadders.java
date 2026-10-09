import java.util.Random;
import java.util.Scanner;

public class SnakesAndLadders {
    public static void main(String[] args) {
        final int WINNING_POSITION = 16; // 4x4 board, so max position is 16
        Scanner scanner = new Scanner(System.in);
        int playerPosition = 0;
        Random dice = new Random();
        boolean gameOver = false;
        while (!gameOver) {
            System.out.println("Your turn.");
            System.out.print("Press Enter to roll the dice...");
            scanner.nextLine();
            int diceRoll = dice.nextInt(6) + 1; // Roll a dice (1-6)
            System.out.println("You rolled a " + diceRoll);
            int newPosition = playerPosition + diceRoll;
            if (newPosition > WINNING_POSITION) {
                System.out.println("You rolled too high and stayed at " + playerPosition);
            } else {
                playerPosition = newPosition;
                // Handle ladders
                if (playerPosition == 3) {
                    System.out.println("You found a ladder! Climb up to 11.");
                    playerPosition = 11;
                } else if (playerPosition == 5) {
                    System.out.println("You found a ladder! Climb up to 9.");
                    playerPosition = 9;
                }
                // Handle snakes
                if (playerPosition == 15) {
                    System.out.println("Oops! You hit a snake! Slide down to 7.");
                    playerPosition = 7;
                } else if (playerPosition == 12) {
                    System.out.println("Oops! You hit a snake! Slide down to 2.");
                    playerPosition = 2;
                }
                System.out.println("You are now at position " + playerPosition);
                if (playerPosition == WINNING_POSITION) {
                    System.out.println("Congratulations! You win!");
                    gameOver = true;
                }
            }
        }
        scanner.close();
    }
}
