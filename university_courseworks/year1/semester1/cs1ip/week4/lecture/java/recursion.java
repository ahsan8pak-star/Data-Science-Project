// Factorial Example

static int factorial(int n) {
    if (n == 0) return 1;          // Base case: stops recursion when n reaches 0
    return n * factorial(n - 1);  // Recursive case: multiplies n by sub-problem
}

// Fibonacci Example

static int fibonacci(int n) {
    if (n == 0) return 0;                             // Base case 1
    if (n == 1) return 1;                             // Base case 2
    return fibonacci(n - 1) + fibonacci(n - 2);      // Double recursive call
}

