// TextUI Class - Text-Based User Interface Utilities

import java.util.List;
import java.util.Scanner;

public class TextUI {

    // Scanner for User Input
    private static final Scanner scanner = new Scanner(System.in);

    // Display a Box with Title and Lines
    public static void box(String title, List<String> lines) {
        int max = title.length();
        for (String line : lines) {
            if (line.length() > max)
                max = line.length();
        }
        int width = max + 4;
        printLine(width);
        printCenteredLine(title, width);
        printLine(width);
        for (String line : lines) {
            printPaddedLine(line, width);
        }
        printLine(width);
    }

    // Display a Box with Title and Varargs Lines
    public static void box(String title, String... lines) {
        box(title, java.util.Arrays.asList(lines));
    }

    // Print Horizontal Line
    private static void printLine(int width) {
        for (int i = 0; i < width; i++) {
            System.out.print("-");
        }
        System.out.println();
    }

    // Print Centered Line within Box
    private static void printCenteredLine(String text, int width) {
        int padding = (width - 2 - text.length()) / 2;
        System.out.print("|");
        for (int i = 0; i < padding; i++)
            System.out.print(" ");
        System.out.print(text);
        for (int i = 0; i < width - 2 - padding - text.length(); i++)
            System.out.print(" ");
        System.out.println("|");
    }

    // Print Padded Line within Box
    private static void printPaddedLine(String text, int width) {
        System.out.print("|");
        System.out.print(" ");
        System.out.print(text);
        for (int i = 0; i < width - 3 - text.length(); i++)
            System.out.print(" ");
        System.out.println("|");
    }

    // Prompt user for input
    public static String prompt(String label) {
        System.out.print(label + " ");
        return scanner.nextLine().trim();
    }
}
