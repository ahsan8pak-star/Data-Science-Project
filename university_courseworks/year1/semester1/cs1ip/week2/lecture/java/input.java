import java.util.Scanner;

public class FormattedInputOutput {
    public static void main(String[] args) {
        // Instantiate Scanner to read from standard input
        Scanner input = new Scanner(System.in);

        // Read an integer input
        System.out.print("Enter an integer: ");
        int userInt = input.nextInt();

        // Consume trailing newline character
        input.nextLine();

        // Read a line of string input
        System.out.print("Enter a sentence: ");
        String userString = input.nextLine();

        // Read a single char input
        System.out.print("Enter a character: ");
        char userChar = input.nextLine().charAt(0);

        // Display output using formatted printing
        System.out.printf("Integer: %d%nString: %s%nCharacter: %c%n", userInt, userString, userChar);

        input.close();
    }
}

