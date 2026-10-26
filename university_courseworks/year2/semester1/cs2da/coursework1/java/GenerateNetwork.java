import java.util.Random;

public class GenerateNetwork {

    public static void main(String args[]) {

        // Replace this with your student ID.
        long studentNumber = 1234567890;

        int n = 6;
        double[][] distances = new double[n][n];

        Random random = new Random(studentNumber);
        double offset = Math.floorMod(studentNumber, 5) / 5.0;

        // Generate a symmetric matrix of non-negative integer distances.
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                double distance = Math.floor(30 * Math.abs(offset - random.nextGaussian()));
                distances[i][j] = distance;
                distances[j][i] = distance;
            }
        }

        // Mark two distinct, randomly chosen entries in each row as missing.
        // These omissions are independent by row, so the displayed matrix need not remain symmetric.
        for (int i = 0; i < n; i++) {
            int first = random.nextInt(n);
            int second = random.nextInt(n - 1);
            if (second >= first) {
                second++;
            }
            distances[i][first] = Double.NaN;
            distances[i][second] = Double.NaN;
        }

        // The diagonal represents the distance from each location to itself.
        for (int i = 0; i < n; i++) {
            distances[i][i] = 0;
        }

        if (studentNumber == 1234567890) {
            System.out.println("WARNING: YOU NEED TO PUT YOUR STUDENT ID IN THE PROGRAM SOURCE CODE.");
        }
        System.out.println("Student ID: " + studentNumber);
        System.out.println("The adjacency matrix showing direct distances (miles)");
        System.out.println("amongst A, B, C, D, E, F is given by:");
        System.out.println();
        for (double[] row : distances) {
            for (double distance : row) {
                System.out.printf("%8.0f", distance);
            }
            System.out.println();
        }

    }

}

