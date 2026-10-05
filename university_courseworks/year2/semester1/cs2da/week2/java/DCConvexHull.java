import java.util.LinkedList;
import java.util.Collections;
import java.util.Arrays;
import java.util.Random;
import java.awt.*;
import java.awt.event.*;

/*
To run in Notepad++ on lab PCs, or on your own PC with JDK installed and
java.exe on the path, use this command on the Run menu:
cmd /k java $(FULL_CURRENT_PATH)

(The "cmd /k" keeps the command prompt open, so you can see the output.)
*/

public class DCConvexHull {

    ///////////////////////////////////////////////////////////////////////////
    // TASK 1: MERGE SORT                                                    //
    ///////////////////////////////////////////////////////////////////////////

    // Split input list into 2 equal halves.
    // Return left half. Input list is updated to be right half.
    public static <T> LinkedList<T> split(LinkedList<T> xs) {
        LinkedList<T> left = new LinkedList<T>();

        int half = xs.size() / 2;
        for (int n = 0; n < half; n++) {
            left.addLast(xs.removeFirst());
        }

        return left;
    }

    // Merge 2 sorted lists.
    // Return a new list with items from both, also sorted. Input lists are emptied.
    public static <T extends Comparable<T>> LinkedList<T> merge(LinkedList<T> xs, LinkedList<T> ys) {
        LinkedList<T> zs = new LinkedList<T>();

        ///////////////////////////////////////////////////////////////////////
        // SUBTASK 1: MERGE - ~14 lines of code needed                       //
        ///////////////////////////////////////////////////////////////////////

        return zs;
    }

    // Merge sort a list.
    // Return a new list with items in sorted order. Input list is emptied.
    public static <T extends Comparable<T>> LinkedList<T> merge_sort(LinkedList<T> xs) {

        ///////////////////////////////////////////////////////////////////////
        // SUBTASK 2: DIVIDE & CONQUER - ~6 lines of code needed             //
        ///////////////////////////////////////////////////////////////////////

        return null; // Delete this line when you start the task.
    }

    // Spent ages trying to get merge_sort working and want to move onto the next task?
    // In merge_hull(), swap out merge_sort() for cheat_sort(), which just calls the Java standard library's sort routine.
    // Also, comment out the tests for merge_sort at the start of main().
    public static <T extends Comparable<T>> LinkedList<T> cheat_sort(LinkedList<T> xs) {
        LinkedList<T> ys = new LinkedList<T>(xs);
        Collections.sort(ys);
        return ys;
    }

    ///////////////////////////////////////////////////////////////////////////
    // TASK 2: MERGE HULL                                                    //
    ///////////////////////////////////////////////////////////////////////////

    // Imagine walking in a straight line from p1 to p2. To face p3, do you have to turn clockwise?
    // (Also returns true if you don't have to turn at all.)
    // p1 must be left-most for this to work.
    public static boolean clockwise(Point p1, Point p2, Point p3) {
        // Essentially this works by comparing the gradients of p1->p2 and p1->p3.
        // But we don't want to compute gradients directly, or we may (for example) divide by zero.
        // Source: https://jeffe.cs.illinois.edu/teaching/compgeom/notes/14-convexhull.pdf
        return (p3.y - p1.y)*(p2.x - p1.x) <= (p2.y - p1.y)*(p3.x - p1.x);
    }

    // This is the "conquer" and "combine" part of convex hull divide & conquer.
    // It has some similarities with merge(), but there are big differences too.
    public static LinkedList<Point> merge_disjoint_lower_hulls(LinkedList<Point> left, LinkedList<Point> right) {
        // Tighten the bridge:

        ///////////////////////////////////////////////////////////////////////
        // SUBTASK 1: MERGE - ~17 lines of code needed                       //
        ///////////////////////////////////////////////////////////////////////



        // Concatenate the remaining points from both.
        LinkedList<Point> hull = new LinkedList<Point>(left);
        hull.addAll(right);
        return hull;
    }

    // This is the "divide" part of convex hull divide & conquer.
    // It should look like very similar to merge_sort().
    public static LinkedList<Point> lower_hull(LinkedList<Point> ps) {

        ///////////////////////////////////////////////////////////////////////
        // SUBTASK 2: DIVIDE & CONQUER - ~6 lines of code needed             //
        ///////////////////////////////////////////////////////////////////////

        return null; // Delete this line when you start the task.
    }

    // This method calculates the upper and lower hull separately, then joins them.
    public static LinkedList<Point> upper_lower_hull(LinkedList<Point> ps) {

        // 2 points are already a convex hull.
        if (ps.size() <= 2) {
            return ps;
        }

        LinkedList<Point> upper = new LinkedList<Point>(ps);
        LinkedList<Point> lower = new LinkedList<Point>(ps);

        // Do lower hull.
        lower = lower_hull(lower);

        ///////////////////////////////////////////////////////////////////////
        // SUBTASK 3: UPPER CONVEX HULL - ~12 lines of code needed           //
        ///////////////////////////////////////////////////////////////////////



        return lower;
    }

    // Sort the points, then call the main algorithm.
    public static LinkedList<Point> merge_hull(LinkedList<Point> ps) {
        return upper_lower_hull(merge_sort(ps));
    }

    ///////////////////////////////////////////////////////////////////////////
    // YOU CAN MOSTLY IGNORE EVERYTHING BELOW HERE.                          //
    ///////////////////////////////////////////////////////////////////////////

    // Tests for merge().
    public static void test_merge() {
        Integer xss[][] = new Integer[][] {{}, {0}, {},  {1,2,3}, {2,4,6,8}};
        Integer yss[][] = new Integer[][] {{}, {} , {1}, {4,5,6}, {1,2,3,4}};
        String outs[] = {"[]", "[0]", "[1]", "[1, 2, 3, 4, 5, 6]", "[1, 2, 2, 3, 4, 4, 6, 8]"};

        for (int n = 0; n < outs.length; n++) {
            LinkedList<Integer> xs = new LinkedList<Integer>(Arrays.asList(xss[n]));
            LinkedList<Integer> ys = new LinkedList<Integer>(Arrays.asList(yss[n]));
            String expect = outs[n];
            System.out.printf("Test: merge(%s, %s)%n", xs.toString(), ys.toString());
            System.out.printf("Expected: %s%n", expect.toString());
            String actual = merge(xs, ys).toString();
            if (expect.equals(actual)) {
                System.out.printf("PASS%n%n");
            }
            else {
                System.out.printf("Actual: %s%nFAIL%n", actual);
                System.exit(-1);
            }
        }
    }

    // Tests for merge_sort().
    public static void test_merge_sort() {
        Integer xss[][] = new Integer[][] {{}, {0}, {1,2}, {2,1}, {2,7,5,1,6,8,3,4}, {3,1,4,5,6,2,7}};
        String outs[] = {"[]", "[0]", "[1, 2]", "[1, 2]", "[1, 2, 3, 4, 5, 6, 7, 8]", "[1, 2, 3, 4, 5, 6, 7]"};

        for (int n = 0; n < outs.length; n++) {
            LinkedList<Integer> xs = new LinkedList<Integer>(Arrays.asList(xss[n]));
            String expect = outs[n];
            System.out.printf("Test: merge_sort(%s)%n", xs.toString());
            System.out.printf("Expected: %s%n", expect.toString());
            String actual = merge_sort(xs).toString();
            if (expect.equals(actual)) {
                System.out.printf("PASS%n%n");
            }
            else {
                System.out.printf("Actual: %s%nFAIL%n", actual);
                System.exit(-1);
            }
        }
    }

    // Helper method for next set of tests: turn a sequence of co-ordinates into a list of points.
    public static LinkedList<Point> line(Double[] ps) {
        LinkedList<Point> line = new LinkedList<Point>();
        for (int n = 0; n < ps.length; n = n + 2) {
                line.addLast(new Point(ps[n], ps[n+1]));
        }
        return line;
    }

    // Tests for merge_disjoint_lower_hulls().
    public static void test_merge_disjoint_lower_hulls() {
        Double lefts[][] = new Double[][]  {{1.0, 5.0, 2.0, 1.0}, {1.0, 5.0, 2.0, 1.0, 3.0, 5.0}, {1.0, 5.0, 2.0, 6.0, 3.0, 7.0, 4.0, 8.0}, {1.0, 5.0, 2.0, 0.0}};
        Double rights[][] = new Double[][] {{4.0, 1.0, 5.0, 5.0}, {4.0, 5.0, 5.0, 1.0, 6.0, 5.0}, {5.0, 1.0, 6.0, 1.0}, {3.0, 5.0, 4.0, 4.5, 5.0, 4.0, 6.0, 3.5}};
        String outs[] = {"[(1.0,5.0), (2.0,1.0), (4.0,1.0), (5.0,5.0)]", "[(1.0,5.0), (2.0,1.0), (5.0,1.0), (6.0,5.0)]", "[(1.0,5.0), (5.0,1.0), (6.0,1.0)]", "[(1.0,5.0), (2.0,0.0), (6.0,3.5)]"};

        for (int n = 0; n < outs.length; n++) {
            LinkedList<Point> left = line(lefts[n]);
            LinkedList<Point> right = line(rights[n]);
            String expect = outs[n];
            System.out.printf("Test: merge_disjoint_lower_hulls(%s, %s)%n", left.toString(), right.toString());
            System.out.printf("Expected: %s%n", expect.toString());
            String actual = merge_disjoint_lower_hulls(left, right).toString();
            if (expect.equals(actual)) {
                System.out.printf("PASS%n%n");
            }
            else {
                System.out.printf("Actual: %s%nFAIL%n", actual);
                System.exit(-1);
            }
        }
    }

    // Test the algorithms with some fixed tests and random data.
    public static void main(String args[]) {
        // TASK 2: If you gave up on Task 1, comment out the next 4 lines.
        test_merge();
        System.out.printf("Testing Task 1.1 complete.%n%n");
        test_merge_sort();
        System.out.printf("Testing Task 1.2 complete.%n%n");

        test_merge_disjoint_lower_hulls();
        System.out.printf("Testing Task 2.1 complete.%n%n");

        Random r = new Random();
        LinkedList<Point> ps = new LinkedList<Point>();

        // Generate an inner ring of random points...
        for (int n = 0; n < 40; n++) {
            double theta = (2.0 * Math.PI / 10.0) * (n + r.nextDouble());
            double radius = 125.0 * (0.5 + (r.nextDouble()));
            double x = 250.0 + (radius * Math.cos(theta));
            double y = 250.0 + (radius * Math.sin(theta));
            ps.addLast(new Point (x, y));
        }

        // ...and an outer ring of non-random points.
        for (int n = 0; n < 10; n++) {
            double theta = (2.0 * Math.PI / 10.0) * (n);
            double radius = 200.0;
            double x = 250.0 + (radius * Math.cos(theta));
            double y = 250.0 + (radius * Math.sin(theta));
            ps.addLast(new Point (x, y));
        }

        // Calculate and display convex hull.
        LinkedList<Point> all = new LinkedList<Point>(ps);
        LinkedList<Point> hull = merge_hull(ps);
        new ConvexHullPlot(all, hull);
    }

}

// Class to represent a 2D point.
class Point implements Comparable<Point> {
    public double x;
    public double y;

    Point(double x, double y) {
        this.x = x;
        this.y = y;
    }

    // When sorting, sort by x-ordinate. Break ties by y-ordinate.
    public int compareTo(Point p2) {
        return (this.x == p2.x) ? Double.compare(this.y, p2.y) : Double.compare(this.x, p2.x);
    }

    // Negate the y-ordinate, mirroring the point in the x-axis.
    public void flip() {
        this.y = this.y * -1;
    }

    // String representation for easy printing/debugging.
    public String toString() {
        return "(" + this.x + "," + this.y + ")";
    }
}

// Simple GUI class to visualise convex hull.
class ConvexHullPlot extends Frame {
    LinkedList<Point> all;
    LinkedList<Point> hull;
    
    // all - All the points under consideration.
    // hull - Just those points on the convex hull's perimeter.
    ConvexHullPlot(LinkedList<Point> all, LinkedList<Point> hull) {
        this.all = all;
        this.hull = hull;

        this.setSize(500, 500);
        this.setVisible(true);

        // When the user closes the window, destroy it, so the program terminates.
        this.addWindowListener(new WindowAdapter() {
                public void windowClosing(WindowEvent we) {
                    ConvexHullPlot.this.dispose();
                }
            }
        );
    }

    public void paint(Graphics g) {
        super.paint(g);

        // Display co-ordinates are left-handed, so we have to do "500-" on all y-ordinates.

        // Draw all points in blue.
        g.setColor(Color.BLUE);
        for (Point p : this.all) {
            g.fillOval((int) p.x, 500 - (int) p.y, 5, 5);
        }

        // Draw perimeter of hull in green.
        g.setColor(Color.GREEN);
        Point p1 = this.hull.peekLast();
        for (Point p2 : this.hull) {
            g.drawLine((int) p1.x, 500 - (int) p1.y, (int) p2.x, 500 - (int) p2.y);
            p1 = p2;
        }

    }
}

