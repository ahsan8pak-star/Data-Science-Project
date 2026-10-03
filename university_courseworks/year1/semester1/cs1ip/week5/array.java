TYPE[] VAR_NAME; // e.g., int[] arr; or String[] arr;

// Initialise Array
TYPE[] VAR_NAME = new TYPE[SIZE]; // e.g., int[] arr = new int[5];

// Increment each element array sequentially
int[] incrementArray(int[] numbers) {
    int[] incrementedArray = new int[numbers.length];
    for (int i = 0; i < numbers.length; i++) {
        incrementedArray[i] = numbers[i] + 1;
    }
    return incrementedArray;
}

// Initialise Example
int[] numbers = {1, 2, 3, 4, 5};
String[] words = {"Imperative", "Programming", "is", "nice", "!"};

// For Loop Iteration
int[] arr = {1, 2, 3, 4, 5};
for (int i = 0; i < arr.length; i++) {
    System.out.println(arr[i]);
}

// For-Each Loop Iteration
for (int element : arr) {
    System.out.println(element);
}

