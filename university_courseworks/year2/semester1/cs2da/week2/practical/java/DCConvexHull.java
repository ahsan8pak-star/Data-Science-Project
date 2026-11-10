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
    //
    // SOLUTION: Remove the first half of elements from xs and return them.
    // After this call, xs holds the right half (mutated in place).
    //
    // COMMON MISTAKE: Creating a copy instead of removing from xs.
    //   If xs is not emptied, merge_sort() and lower_hull() will recurse on
    //   the same full list, causing infinite recursion or wrong results.
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
    //
    // SOLUTION (merge step of merge-sort):
    //   Classic two-pointer merge: compare the heads of xs and ys, append the
    //   smaller to the result, repeat until one list is empty, then drain the
    //   remainder of the other. Using <= (not <) keeps equal elements stable.
    //
    // COMMON MISTAKES:
    //   - Forgetting to drain the leftovers: the loop exits when one list
    //     empties, leaving the other's tail unmerged.
    //   - Using '<' instead of '<=' reverses equal elements, breaking stability.
    //   - Not removing from xs/ys: the loop never terminates (infinite loop).
    //   - Comparing peekLast() instead of peekFirst(): merges in reverse order.
    public static <T extends Comparable<T>> LinkedList<T> merge(LinkedList<T> xs, LinkedList<T> ys) {
        LinkedList<T> zs = new LinkedList<T>();

        while (!xs.isEmpty() && !ys.isEmpty()) {
            if (xs.peekFirst().compareTo(ys.peekFirst()) <= 0) {
                zs.addLast(xs.removeFirst());
            }
            else {
                zs.addLast(ys.removeFirst());
            }
        }

        while (!xs.isEmpty()) {
            zs.addLast(xs.removeFirst());
        }

        while (!ys.isEmpty()) {
            zs.addLast(ys.removeFirst());
        }

        return zs;
    }

    // Merge sort a list.
    // Return a new list with items in sorted order. Input list is emptied.
    //
    // SOLUTION (divide & conquer):
    //   Base case: a list of 0 or 1 elements is already sorted.
    //   Recursive case: split into left/right halves, sort each, merge.
    //   split(xs) removes the first half from xs and returns it; xs becomes
    //   the right half. Both halves are sorted independently, then merged.
    //
    // COMMON MISTAKES:
    //   - Forgetting split() mutates xs: after split, xs holds the RIGHT half.
    //     Passing xs to both recursive calls re-sorts the same data.
    //   - Returning null instead of the sorted list (xs is empty after split).
    //   - Using merge_sort(xs) on the same list in both calls (infinite
    //     recursion or incorrect results).
    //   - Not handling the base case: xs.size() <= 1 means 0 or 1 elements.
    public static <T extends Comparable<T>> LinkedList<T> merge_sort(LinkedList<T> xs) {
        if (xs == null || xs.size() <= 1) {
            return xs;
        }

        LinkedList<T> left = split(xs);
        return merge(merge_sort(left), merge_sort(xs));
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
    //
    // SOLUTION: Cross product avoids division (no divide-by-zero risk).
    //   (p3.y - p1.y) * (p2.x - p1.x)  <=  (p2.y - p1.y) * (p3.x - p1.x)
    // Rearranged: this is equivalent to cross(p1, p2, p3) <= 0, which means
    // clockwise or collinear. A positive cross product means counter-clockwise.
    //
    // COMMON MISTAKE: Computing the gradient (p2.y-p1.y)/(p2.x-p1.x) directly
    // and dividing by zero when p2.x == p1.x (vertical line). The cross product
    // form avoids this entirely.
    public static boolean clockwise(Point p1, Point p2, Point p3) {
        // Essentially this works by comparing the gradients of p1->p2 and p1->p3.
        // But we don't want to compute gradients directly, or we may (for example) divide by zero.
        // Source: https://jeffe.cs.illinois.edu/teaching/compgeom/notes/14-convexhull.pdf
        return (p3.y - p1.y)*(p2.x - p1.x) <= (p2.y - p1.y)*(p3.x - p1.x);
    }

    // Cross product of vectors (o->a) and (o->b).
    // Positive = counter-clockwise turn, Negative = clockwise, Zero = collinear.
    // This is the core geometric test used throughout the hull algorithm.
    //
    // COMMON MISTAKE: Confusing the sign convention. In this codebase:
    //   cross <= 0 means "remove the middle point" (clockwise or collinear).
    //   cross > 0 means "keep the middle point" (counter-clockwise).
    // Getting this backwards removes the wrong points and produces an incorrect hull.
    private static double cross(Point o, Point a, Point b) {
        return (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x);
    }

    // This is the "conquer" and "combine" part of convex hull divide & conquer.
    // It has some similarities with merge(), but there are big differences too.
    //
    // SOLUTION (bridge tightening):
    //   1. Concatenate left hull + right hull into one ordered list.
    //   2. Scan left-to-right, maintaining a stack of hull points.
    //   3. For each new point p, while the last two hull points + p form a
    //      non-left turn (cross <= 0), pop the last hull point.
    //   4. Add p to the hull.
    //   cross <= 0 means clockwise or collinear: the middle point is inside
    //   the convex boundary and must be removed.
    //
    // COMMON MISTAKES:
    //   - Using cross < 0 instead of <= 0: collinear points are not removed,
    //     leaving redundant interior points on the hull.
    //   - Just concatenating left + right without pruning: returns a chain
    //     with interior points, not a true convex hull.
    //   - Scanning right-to-left instead of left-to-right: wrong pruning
    //     direction for the lower hull.
    //   - Forgetting that left and right are already lower hulls, not raw
    //     point sets: they must be merged, not re-sorted.
    public static LinkedList<Point> merge_disjoint_lower_hulls(LinkedList<Point> left, LinkedList<Point> right) {
        if (left == null || left.isEmpty()) {
            return right;
        }
        if (right == null || right.isEmpty()) {
            return left;
        }

        LinkedList<Point> ordered = new LinkedList<Point>();
        for (Point p : left) {
            ordered.addLast(p);
        }
        for (Point p : right) {
            ordered.addLast(p);
        }

        LinkedList<Point> lower = new LinkedList<Point>();
        for (Point p : ordered) {
            while (lower.size() >= 2 && cross(lower.get(lower.size() - 2), lower.getLast(), p) <= 0) {
                lower.removeLast();
            }
            lower.addLast(p);
        }

        return lower;
    }

    // This is the "divide" part of convex hull divide & conquer.
    // It should look like very similar to merge_sort().
    //
    // SOLUTION (divide & conquer):
    //   Base case: 0, 1 or 2 points are already a lower convex hull.
    //   Recursive case: split into left/right halves, compute lower hull
    //   for each, then merge the two disjoint lower hulls.
    //   split(ps) removes the first half from ps and returns it; ps becomes
    //   the right half (same pattern as merge_sort).
    //
    // COMMON MISTAKES:
    //   - Passing the same list to both recursive calls: split() mutates ps,
    //     so after split, ps holds the right half. Both calls must use
    //     different halves.
    //   - Forgetting the base case: a list of 2 points is already a hull.
    //   - Not copying ps before passing to lower_hull: the original is
    //     consumed by split().
    public static LinkedList<Point> lower_hull(LinkedList<Point> ps) {
        if (ps == null || ps.isEmpty() || ps.size() <= 2) {
            return new LinkedList<Point>(ps);
        }

        LinkedList<Point> left = split(ps);
        LinkedList<Point> leftHull = lower_hull(left);
        LinkedList<Point> rightHull = lower_hull(ps);
        return merge_disjoint_lower_hulls(leftHull, rightHull);
    }

    // This method calculates the upper and lower hull separately, then joins them.
    //
    // SOLUTION (full convex hull = lower chain + upper chain):
    //   1. Compute the lower hull (left-to-right chain on the bottom).
    //   2. Compute the upper hull by scanning RIGHT-TO-LEFT, applying the
    //      same cross-product pruning (cross <= 0 means remove the middle).
    //   3. Join: add all lower hull points, then add upper hull points that
    //      are not already in the hull (avoids duplicating shared endpoints).
    //
    // WHY SCAN RIGHT-TO-LEFT FOR UPPER HULL:
    //   The lower hull scans left-to-right (increasing x). The upper hull
    //   must scan right-to-left (decreasing x) so that the cross product
    //   test correctly identifies interior points on the top chain.
    //   Scanning left-to-right for the upper hull would produce wrong results.
    //
    // COMMON MISTAKES:
    //   - Scanning left-to-right for the upper hull: wrong pruning direction.
    //   - Returning only the lower hull: gives half the boundary.
    //   - Duplicating shared endpoints (leftmost/rightmost points appear in
    //     both chains): the seen-check prevents this.
    //   - Forgetting to copy ps before lower_hull: ps is consumed by split().
    //   - Using cross < 0 instead of <= 0: collinear points remain.
    public static LinkedList<Point> upper_lower_hull(LinkedList<Point> ps) {
        if (ps == null || ps.isEmpty() || ps.size() <= 2) {
            return new LinkedList<Point>(ps);
        }

        LinkedList<Point> lower = lower_hull(new LinkedList<Point>(ps));
        LinkedList<Point> upper = new LinkedList<Point>();

        for (int i = ps.size() - 1; i >= 0; i--) {
            Point p = ps.get(i);
            while (upper.size() >= 2 && cross(upper.get(upper.size() - 2), upper.getLast(), p) <= 0) {
                upper.removeLast();
            }
            upper.addLast(p);
        }

        LinkedList<Point> hull = new LinkedList<Point>();
        for (Point p : lower) {
            hull.addLast(p);
        }
        for (Point p : upper) {
            boolean seen = false;
            for (Point q : hull) {
                if (p == q) {
                    seen = true;
                    break;
                }
            }
            if (!seen) {
                hull.addLast(p);
            }
        }

        return hull;
    }

    // Sort the points, then call the main algorithm.
    //
    // SOLUTION: Sort points by x (then y) first, then compute the full hull.
    // Sorting is essential: the divide-and-conquer assumes points are sorted
    // by x-coordinate so the left/right split is geometrically meaningful.
    //
    // COMMON MISTAKE: Calling upper_lower_hull() on unsorted points. Without
    // sorting, split() divides arbitrarily and the hull will be wrong.
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

