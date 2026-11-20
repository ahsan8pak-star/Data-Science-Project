import java.lang.management.ThreadMXBean;
import java.lang.management.ManagementFactory;
import java.util.Random;

public class SortBenchmarkSolution {

    private static ThreadMXBean thread_timer;
    private static long time = -1;

    public static void start_timer() {
        if (time == -1) {
            time = thread_timer.getCurrentThreadCpuTime();
        }
        else {
            throw new Error();
        }
    }

    public static long stop_timer() {
        if (time == -1) {
            throw new Error();
        }
        else {
            long diff = thread_timer.getCurrentThreadCpuTime() - time;
            time = -1;
            return diff;
        }
    }

	private static Random r = null;

    public static Integer[] random_list(int n) {
        Integer[] a = new Integer[n];

		for (int x = 0; x < n; x++) {
			a[x] = r.nextInt();
		}
		
        return a;
    }
	
	public static void print_array(Object[] a) {
		for (int x = 0; x < a.length; x++) {
			System.out.print(a[x]);
			System.out.print(" ");
		}
		System.out.println();
	}

    public static void main(String[] args) {
		Integer[] a = null;
        thread_timer = ManagementFactory.getThreadMXBean();
		long time;

		// As expected, insertion sort scales very badly.
		// It cannot even manage an array of 100,000 integers in 10s on my machine.

		r = new Random(20241024);
		time = 0;
		// Start with 10,000, because anything less is too fast to measure.
		// Keep increasing the input size until the running time for the sort exceeds 10s.
		// Increasing by 20% each time, rather than by a constant amount,
		// means that we reach 10s without an excessive number of iterations,
		// while still getting a good number of datapoints in the 1s-10s range.
		// If you use non-linear spacing of datapoints like this, make sure you draw an
		// X-Y scatter graph, not an ordinary line graph.
		for (int n = 10000; time < 10000000000L; n = (n * 12)/10) {
			a = random_list(n);
			start_timer();
			Insertion.sort(a);
			time = stop_timer();
			System.out.printf("insertion,%d,%d%n", n, time/1000000);
		}

		// On my machine, mergesort turns out to be fastest and has a nice, gradual curve.
		// Note thst this implementation of mergesort is bottom-up (hence MergeBU).
		// This avoids the need for recursion.
		r = new Random(20241024);
		time = 0;
		for (int n = 10000; time < 10000000000L; n = (n * 12)/10) {
			a = random_list(n);
			start_timer();
			MergeBU.sort(a);
			time = stop_timer();
			System.out.printf("merge,%d,%d%n", n, time/1000000);
		}

		// Quicksort has a similar curve to mergesort, but is slower on my machine.
		// This might be surprising, as everyone usually says, "quicksort is fastest in practice".
		// However, that refers to quicksort with all the low-level optimisations.
		// This implementation includes one optimisation, namely 3-way partition.
		// This makes it extremely fast on input with many repeated values,
		// as you will discover if you restrict the input arrays to integers in the range 0-99.
		// The other sorts also improve somewhat, as this reduces the number of exchanges needed.

		// This quicksort also uses a random shuffle to avoid worst-case O(n^2) behaviour.
		// Other common optimisations include reverting to insertion sort for very small arrays
		// and taking the median of 3 candidate pivots to use as the actual pivot.
		r = new Random(20241024);
		time = 0;
		for (int n = 10000; time < 10000000000L; n = (n * 12)/10) {
			a = random_list(n);
			start_timer();
			Quick3way.sort(a);
			time = stop_timer();
			System.out.printf("quick,%d,%d%n", n, time/1000000);
		}

		// The running time of Shell sort is highly dependent on the stride sequence used.
		// The sequence in this implementation gives O(n^2/3) complexity.
		// This is definitely slower than mergesort and quicksort,
		// but it only takes about twice as long to sort 2,000,000 integers.
		// You may recall that Shell sort is used to implement "qsort" in the embedded C library ulibC
		// because it uses no recursion and O(1) working space.
		// 2,000,000 32-bit integers is 8 MB of data, which exceeds the amount of memory
		// on many embedded systems, making performance beyond this irrelevant.
		r = new Random(20241024);
		time = 0;
		for (int n = 10000; time < 10000000000L; n = (n * 12)/10) {
			a = random_list(n);
			start_timer();
			Shell.sort(a);
			time = stop_timer();
			System.out.printf("shell,%d,%d%n", n, time/1000000);
		}

    }

}


///////////////////////////////////////////////////////////////////////////////
// INSERTION SORT                                                            //
///////////////////////////////////////////////////////////////////////////////

class Insertion {

    // This class should not be instantiated.
    private Insertion() { }

    /**
     * Rearranges the array in ascending order, using the natural order.
     * @param a the array to be sorted
     */
    public static void sort(Comparable[] a) {
        int n = a.length;
        for (int i = 1; i < n; i++) {
            for (int j = i; j > 0 && less(a[j], a[j-1]); j--) {
                exch(a, j, j-1);
            }
        }
    }

   /***************************************************************************
    *  Helper sorting functions.
    ***************************************************************************/

    // is v < w ?
    private static boolean less(Comparable v, Comparable w) {
        return v.compareTo(w) < 0;
    }

    // exchange a[i] and a[j]
    private static void exch(Object[] a, int i, int j) {
        Object swap = a[i];
        a[i] = a[j];
        a[j] = swap;
    }

}


///////////////////////////////////////////////////////////////////////////////
// MERGESORT                                                                 //
///////////////////////////////////////////////////////////////////////////////

class MergeBU {

    // This class should not be instantiated.
    private MergeBU() { }

    // stably merge a[lo..mid] with a[mid+1..hi] using aux[lo..hi]
    private static void merge(Comparable[] a, Comparable[] aux, int lo, int mid, int hi) {

        // copy to aux[]
        for (int k = lo; k <= hi; k++) {
            aux[k] = a[k];
        }

        // merge back to a[]
        int i = lo, j = mid+1;
        for (int k = lo; k <= hi; k++) {
            if      (i > mid)              a[k] = aux[j++];  // this copying is unnecessary
            else if (j > hi)               a[k] = aux[i++];
            else if (less(aux[j], aux[i])) a[k] = aux[j++];
            else                           a[k] = aux[i++];
        }

    }

    /**
     * Rearranges the array in ascending order, using the natural order.
     * @param a the array to be sorted
     */
    public static void sort(Comparable[] a) {
        int n = a.length;
        Comparable[] aux = new Comparable[n];
        for (int len = 1; len < n; len *= 2) {
            for (int lo = 0; lo < n-len; lo += len+len) {
                int mid  = lo+len-1;
                int hi = Math.min(lo+len+len-1, n-1);
                merge(a, aux, lo, mid, hi);
            }
        }
    }

  /***********************************************************************
    *  Helper sorting functions.
    ***************************************************************************/

    // is v < w ?
    private static boolean less(Comparable v, Comparable w) {
        return v.compareTo(w) < 0;
    }

}


///////////////////////////////////////////////////////////////////////////////
// QUICKSORT                                                                 //
///////////////////////////////////////////////////////////////////////////////

class Quick3way {

    // This class should not be instantiated.
    private Quick3way() { }

    /**
     * Rearranges the array in ascending order, using the natural order.
     * @param a the array to be sorted
     */
    public static void sort(Comparable[] a) {
        shuffle(a);
        sort(a, 0, a.length - 1);
    }

    public static void shuffle(Object[] a) {
        int n = a.length;
        for (int i = 0; i < n; i++) {
            // choose index uniformly in [0, i]
            int r = (int) (Math.random() * (i + 1));
            Object swap = a[r];
            a[r] = a[i];
            a[i] = swap;
        }
    }

    // quicksort the subarray a[lo .. hi] using 3-way partitioning
    private static void sort(Comparable[] a, int lo, int hi) {
        if (hi <= lo) return;
        int lt = lo, gt = hi;
        Comparable v = a[lo];
        int i = lo + 1;
        while (i <= gt) {
            int cmp = a[i].compareTo(v);
            if      (cmp < 0) exch(a, lt++, i++);
            else if (cmp > 0) exch(a, i, gt--);
            else              i++;
        }

        // a[lo..lt-1] < v = a[lt..gt] < a[gt+1..hi].
        sort(a, lo, lt-1);
        sort(a, gt+1, hi);
    }



   /***************************************************************************
    *  Helper sorting functions.
    ***************************************************************************/

    // is v < w ?
    private static boolean less(Comparable v, Comparable w) {
        return v.compareTo(w) < 0;
    }

    // exchange a[i] and a[j]
    private static void exch(Object[] a, int i, int j) {
        Object swap = a[i];
        a[i] = a[j];
        a[j] = swap;
    }

}


///////////////////////////////////////////////////////////////////////////////
// SHELLSORT                                                                 //
///////////////////////////////////////////////////////////////////////////////

class Shell {

    // This class should not be instantiated.
    private Shell() { }

    /**
     * Rearranges the array in ascending order, using the natural order.
     * @param a the array to be sorted
     */
    public static void sort(Comparable[] a) {
        int n = a.length;

        // 3x+1 increment sequence:  1, 4, 13, 40, 121, 364, 1093, ...
        int h = 1;
        while (h < n/3) h = 3*h + 1;

        while (h >= 1) {
            // h-sort the array
            for (int i = h; i < n; i++) {
                for (int j = i; j >= h && less(a[j], a[j-h]); j -= h) {
                    exch(a, j, j-h);
                }
            }
            h /= 3;
        }
    }

   /***************************************************************************
    *  Helper sorting functions.
    ***************************************************************************/

    // is v < w ?
    private static boolean less(Comparable v, Comparable w) {
        return v.compareTo(w) < 0;
    }

    // exchange a[i] and a[j]
    private static void exch(Object[] a, int i, int j) {
        Object swap = a[i];
        a[i] = a[j];
        a[j] = swap;
    }

}