// Java Assertions & Precondition Check
static double divide(double a, double b) {
    assert b != 0; // Precondition check: prevents division by zero
    return a / b;
}

public static void main(String[] args) {
    assert divide(10, 2) == 5.0; // Functional test verification
}

// Java Javadoc Specification
/**
 * Adds two integers and returns the result.
 * 
 * @param a the first integer
 * @param b the second integer
 * @return the sum of a and b
 */
static int add(int a, int b) {
    return a + b;
}

