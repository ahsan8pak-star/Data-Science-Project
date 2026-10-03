boolean search(int[] arr, int target) {
    if (arr == null || arr.length == 0) {
        throw new IllegalArgumentException("Input array is null or empty");
    }
    for (int i : arr) {
        if (i == target) {
            return true;
        }
    }
    return false;
}

String sanitizeInput(String input) {
    return input.replaceAll("[^a-zA-Z0-9]", "");
}

