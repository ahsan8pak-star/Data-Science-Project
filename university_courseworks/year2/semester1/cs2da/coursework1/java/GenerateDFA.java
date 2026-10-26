public class GenerateDFA {

    public static void main(String args[]) {

        // Replace this with your student ID.
        long id = 1234567890;

        // djb2 hash function
        // Based on: https://compile7.org/hashing/how-to-use-bernsteins-hash-djb2-in-java/
        long hash = 5381; // Initial seed value
        while (id > 0) {
            // hash = hash * 33 + c
            hash = ((hash << 5) + hash) + (id & 255);
            id = id >>> 8;
        }

        // Compute graph from hash.

        int delta[][] = {
            {-1, -1, -1},
            {-1, -1, -1},
            {-1, -1, -1},
        };

        for (int q = 0; q < delta.length; q++) {
            for (int a = 0; a < delta[0].length; a++) {
                delta[q][a] = (int) (hash & 3) - 1;
                hash = hash >>> 2;
            }
        }

        // Force connectivity.
        if (delta[0][0] != 1 && delta[0][1] != 1 && delta[0][2] != 1) {
            delta[0][0] = 1;
        }
        if (delta[1][0] != 2 && delta[1][1] != 2 && delta[1][2] != 2) {
            delta[1][1] = 2;
        }

        boolean accepting[] = {
            false, false, true
        };
        int initial = 0;

        // End compute graph from hash.

        if (id == 1234567890) {
            System.out.println("WARNING: YOU NEED TO PUT YOUR STUDENT ID IN THE PROGRAM SOURCE CODE.");
        }
        System.out.println("Student ID: " + id);
        System.out.println();

        // Print table:
        System.out.println("  q |  a |  b |  c");
        System.out.println("-------------------");
        for (int q = 0; q < delta.length; q++) {
            System.out.print(" q" + q);
            for (int a = 0; a < delta[0].length; a++) {
                if (delta[q][a] == -1) {
                    System.out.print(" | --");
                }
                else {
                    System.out.print(" | q" + delta[q][a]);
                }
            }
            System.out.println();
        }

        // Print list of states:
        System.out.print("Accepting states: ");
        for (int q = 0; q < delta.length; q++) {
            if (accepting[q]) {
                System.out.print(" q" + q);
            }
        }
        System.out.println();
    }

}