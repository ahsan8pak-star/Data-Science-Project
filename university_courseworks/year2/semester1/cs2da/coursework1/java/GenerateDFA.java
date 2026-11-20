public class GenerateDFA {

    public static void main(String args[]) {

        // Student ID for this coursework.
        long id = 34001219;
        String sid = Long.toString(id); // convert student id to string for format check

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

        if (sid.length() != 8 || !sid.startsWith("34")) { // check student id format: 8 digits starting with 34
            System.out.println("WARNING: YOU NEED TO PUT YOUR STUDENT ID IN THE PROGRAM SOURCE CODE.");
        }
        
        System.out.println("Student ID: " + id);
        System.out.println();

        System.out.println("---------------------"); // print table top border
        System.out.println("|  q |  a |  b |  c |"); // print table header
        System.out.println("---------------------"); // print table bottom border before rows

        for (int q = 0; q < delta.length; q++) {
            String row = "| q" + q; // build table row for state q
            for (int a = 0; a < delta[0].length; a++) {
                if (delta[q][a] == -1) {
                    row = row + " | --"; // missing transition
                } else {
                    row = row + " | q" + delta[q][a]; // transition to state
                }
            }
            System.out.println(row); // print table row
        }

        System.out.println("---------------------"); // print table bottom border after rows
        System.out.println();
        StringBuilder acceptingLine = new StringBuilder("Accepting states: "); // build accepting states line
        for (int q = 0; q < delta.length; q++) {
            if (accepting[q]) {
                acceptingLine.append(" q").append(q); // append accepting state
            }
        }
        System.out.println(acceptingLine.toString()); // print accepting states line
    }

}

