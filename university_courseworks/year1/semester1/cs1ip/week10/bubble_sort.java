void bubbleSort(int[] array) {
    int n = array.length;
    boolean sorted = true;
    for (int i = n - 1; i >= 0; i--) {
        for (int j = 0; j < n - 1; j++) {
            if (array[j] > array[j + 1]) {
                int temp = array[j];
                array[j] = array[j + 1];
                array[j + 1] = temp;
                sorted = false;
            }
        }
        if (sorted) {
            break;
        }
    }
}

