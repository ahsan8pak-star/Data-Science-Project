import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.PriorityQueue;
import java.util.Random;

public class GenerateNetwork {

    public static void main(String args[]) {

        // Student ID for this coursework.
        long studentNumber = 34001219;
        String sid = Long.toString(studentNumber); // convert student id to string for format check

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

        if (sid.length() != 8 || !sid.startsWith("34")) { // check student id format: 8 digits starting with 34
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

        double[][] times = new double[n][n];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                double distance = distances[i][j];
                if (Double.isNaN(distance)) {
                    times[i][j] = Double.NaN;
                } else if (distance < 5) {
                    times[i][j] = distance / 5;
                } else if (distance <= 10) {
                    times[i][j] = distance / 20;
                } else {
                    times[i][j] = distance / 30;
                }
            }
        }

        List<Double> shortestDistances = dijkstra(distances, 0);
        List<Double> shortestTimes = dijkstra(times, 0);
        System.out.println("The shortest distances (miles) from A are:");
        for (int i = 0; i < n; i++) {
            double value = shortestDistances.get(i);
            String valueStr = Double.isNaN(value) ? "NaN" : String.format("%.0f", value);
            System.out.println("Shortest distance from " + (char) ('A' + i) + ": " + valueStr);
        }
        System.out.println("The shortest travel times (hours) from A are:");
        for (int i = 0; i < n; i++) {
            double value = shortestTimes.get(i);
            String valueStr = Double.isNaN(value) ? "NaN" : String.format("%.2f", value);
            System.out.println("Shortest travel time from " + (char) ('A' + i) + ": " + valueStr);
    }

    // Dijkstra's algorithm over an adjacency matrix, where the entries are
    // miles for the distances matrix and hours for the travel-time matrix. The
    // standard-library priority queue has no decrease-key operation, so the
    // decrease-key step is implemented as lazy deletion: push a new queue entry
    // whenever a shorter path is found, and skip stale entries when extracted.
    static List<Double> dijkstra(double[][] graph, int start) {
        int size = graph.length;
        double[] dist = new double[size];
        Arrays.fill(dist, Double.POSITIVE_INFINITY);
        dist[start] = 0;
        PriorityQueue<QueueEntry> queue = new PriorityQueue<QueueEntry>();
        queue.add(new QueueEntry(0, start));
        while (!queue.isEmpty()) {
            QueueEntry entry = queue.poll();
            if (entry.cost > dist[entry.node]) {
                continue; // stale entry: the decrease-key was applied when it was pushed
            }
            for (int v = 0; v < size; v++) {
                if (v == entry.node) {
                    continue;
                }
                double weight = graph[entry.node][v];
                if (Double.isNaN(weight)) {
                    continue;
                }
                double candidate = entry.cost + weight;
                if (candidate < dist[v]) {
                    dist[v] = candidate;
                    queue.add(new QueueEntry(candidate, v));
                }
            }
        }
        List<Double> shortest = new ArrayList<>();
        for (int i = 0; i < size; i++) {
            shortest.add(Double.isInfinite(dist[i]) ? Double.NaN : dist[i]);
        }
        return shortest;
    }

    static class QueueEntry implements Comparable<QueueEntry> {
        double cost;
        int node;

        QueueEntry(double cost, int node) {
            this.cost = cost;
            this.node = node;
        }

        public int compareTo(QueueEntry other) {
            return Double.compare(this.cost, other.cost);
        }
    }

}

