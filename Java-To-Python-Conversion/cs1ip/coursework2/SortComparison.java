import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class SortComparison {

    public static void main(String[] args) {
        try {
            System.out.println("Testing cardCompare");
            System.out.println("cardCompare(\"4H\", \"4H\") = " + cardCompare("4H", "4H")); // Expected: 0
            System.out.println("cardCompare(\"4H\", \"3S\") = " + cardCompare("4H", "3S")); // Expected: -1
            System.out.println("cardCompare(\"4H\", \"3H\") = " + cardCompare("4H", "3H")); // Expected: 1
            System.out.println("cardCompare(\"7C\", \"7D\") = " + cardCompare("7C", "7D")); // Expected: -1
            System.out.println("cardCompare(\"1S\", \"13S\") = " + cardCompare("1S", "13S")); // Expected: -1

            System.out.println("\nTesting bubbleSort ");
            ArrayList<String> list1 = new ArrayList<>(List.of("4H", "3S", "7S", "8C", "2D", "3H"));
            System.out.println("Original: " + list1);
            System.out.println("Sorted:   " + bubbleSort(list1));
            // Expected: [3H, 4H, 8C, 2D, 3S, 7S]

            System.out.println("\nTesting mergeSort ");
            ArrayList<String> list2 = new ArrayList<>(List.of("4H", "3S", "7S", "8C", "2D", "3H"));
            System.out.println("Original: " + list2);
            System.out.println("Sorted:   " + mergeSort(list2));
            // Expected: [3H, 4H, 8C, 2D, 3S, 7S]

            System.out.println("\nRunning sortComparison ");
            System.out.println("Analyzing files: sort10.txt, sort100.txt, sort10000.txt");
            sortComparison(new String[] { "sort10.txt", "sort100.txt", "sort10000.txt" });
            System.out.println("✓ CSV file 'sortComparison.csv' generated successfully!");
            System.out.println("Check the file for performance results.");

        } catch (IOException e) {
            System.err.println("ERROR: " + e.getMessage());
            System.err.println("\nMake sure the following files exist in your project directory:");
            System.err.println("  - sort10.txt");
            System.err.println("  - sort100.txt");
            System.err.println("  - sort10000.txt");
            e.printStackTrace();
        }
    }

    static int cardCompare(String card1, String card2) {
        // Extract numbers and suits from each card
        int num1 = Integer.parseInt(card1.substring(0, card1.length() - 1));
        char suit1 = card1.charAt(card1.length() - 1);

        int num2 = Integer.parseInt(card2.substring(0, card2.length() - 1));
        char suit2 = card2.charAt(card2.length() - 1);

        // Convert suits into unique priority values: H = 0, C = 1, D = 2, S = 3
        int suitPriority1 = getSuitPriority(suit1);
        int suitPriority2 = getSuitPriority(suit2);

        // Compare suits first
        if (suitPriority1 < suitPriority2) {
            return -1;
        } else if (suitPriority1 > suitPriority2) {
            return 1;
        }

        // If suits are equal, compare numbers
        if (num1 < num2) {
            return -1;
        } else if (num1 > num2) {
            return 1;
        }

        // Cards are equal
        return 0;
    }

    private static int getSuitPriority(char suit) {
        switch (suit) {
            case 'H':
                return 0;
            case 'C':
                return 1;
            case 'D':
                return 2;
            case 'S':
                return 3;
            default:
                return -1;
        }
    }

    static ArrayList<String> bubbleSort(ArrayList<String> list) {
        // Create a copy to avoid modifying the original list
        ArrayList<String> sortedList = new ArrayList<>(list);
        int n = sortedList.size();

        // Bubble sort algorithm
        for (int i = 0; i < n - 1; i++) {
            for (int j = 0; j < n - i - 1; j++) {
                // Compare adjacent cards using cardCompare
                if (cardCompare(sortedList.get(j), sortedList.get(j + 1)) > 0) {
                    // Swap if the current card is greater than the next card
                    String temp = sortedList.get(j);
                    sortedList.set(j, sortedList.get(j + 1));
                    sortedList.set(j + 1, temp);
                }
            }
        }

        return sortedList;
    }

    static ArrayList<String> mergeSort(ArrayList<String> array) {
        // Base case: if list has 0 or 1 element, it's already sorted
        if (array.size() <= 1) {
            return new ArrayList<>(array);
        }

        // Divide the list into two halves
        int mid = array.size() / 2;
        ArrayList<String> left = new ArrayList<>(array.subList(0, mid));
        ArrayList<String> right = new ArrayList<>(array.subList(mid, array.size()));

        // Recursively sort both halves
        left = mergeSort(left);
        right = mergeSort(right);

        // Merge the sorted halves
        return merge(left, right);
    }

    private static ArrayList<String> merge(ArrayList<String> left, ArrayList<String> right) {
        ArrayList<String> result = new ArrayList<>();
        int i = 0; // Index for left list
        int j = 0; // Index for right list

        // Compare elements from both lists and add the smaller one to result
        while (i < left.size() && j < right.size()) {
            if (cardCompare(left.get(i), right.get(j)) <= 0) {
                result.add(left.get(i));
                i++;
            } else {
                result.add(right.get(j));
                j++;
            }
        }

        // Add remaining elements from left list (if any)
        while (i < left.size()) {
            result.add(left.get(i));
            i++;
        }

        // Add remaining elements from right list (if any)
        while (j < right.size()) {
            result.add(right.get(j));
            j++;
        }

        return result;
    }

    static void sortComparison(String[] files) throws IOException {
        // ArrayLists to store the number of cards and execution times
        ArrayList<Integer> cardCounts = new ArrayList<>();
        ArrayList<Long> bubbleTimes = new ArrayList<>();
        ArrayList<Long> mergeTimes = new ArrayList<>();

        // Process each file
        for (String filename : files) {
            // Read the file and load cards into an ArrayList
            ArrayList<String> cards = readFile(filename);
            cardCounts.add(cards.size());

            // Measure bubbleSort execution time
            ArrayList<String> bubbleList = new ArrayList<>(cards);
            long bubbleStart = System.currentTimeMillis();
            bubbleSort(bubbleList);
            long bubbleEnd = System.currentTimeMillis();
            long bubbleTime = bubbleEnd - bubbleStart;
            bubbleTimes.add(bubbleTime);

            // Measure mergeSort execution time
            ArrayList<String> mergeList = new ArrayList<>(cards);
            long mergeStart = System.currentTimeMillis();
            mergeSort(mergeList);
            long mergeEnd = System.currentTimeMillis();
            long mergeTime = mergeEnd - mergeStart;
            mergeTimes.add(mergeTime);
        }

        // Write results to CSV file
        writeResultsToCSV(cardCounts, bubbleTimes, mergeTimes);
    }

    private static ArrayList<String> readFile(String filename) throws IOException {
        ArrayList<String> cards = new ArrayList<>();

        // Try multiple possible locations for the file
        File file = new File(filename);

        // If file doesn't exist in current directory, try coursework2 subdirectory
        if (!file.exists()) {
            file = new File("coursework2/" + filename);
        }

        // If still not found, try parent directory
        if (!file.exists()) {
            file = new File("../" + filename);
        }

        BufferedReader reader = new BufferedReader(new FileReader(file));
        String line;

        while ((line = reader.readLine()) != null) {
            line = line.trim();
            if (!line.isEmpty()) {
                cards.add(line);
            }
        }

        reader.close();
        return cards;
    }

    private static void writeResultsToCSV(ArrayList<Integer> cardCounts,
            ArrayList<Long> bubbleTimes,
            ArrayList<Long> mergeTimes) throws IOException {
        BufferedWriter writer = new BufferedWriter(new FileWriter("sortComparison.csv"));

        // Write header with card counts
        writer.write(",");
        for (int i = 0; i < cardCounts.size(); i++) {
            writer.write(" " + cardCounts.get(i));
            if (i < cardCounts.size() - 1) {
                writer.write(",");
            }
        }
        writer.newLine();

        // Write bubbleSort times
        writer.write("bubbleSort,");
        for (int i = 0; i < bubbleTimes.size(); i++) {
            writer.write(" " + bubbleTimes.get(i));
            if (i < bubbleTimes.size() - 1) {
                writer.write(",");
            }
        }
        writer.newLine();

        // Write mergeSort times
        writer.write("mergeSort,");
        for (int i = 0; i < mergeTimes.size(); i++) {
            writer.write(" " + mergeTimes.get(i));
            if (i < mergeTimes.size() - 1) {
                writer.write(",");
            }
        }
        writer.newLine();

        writer.close();
    }
}