// Matrix
int[][] matrix = new int[3][3]; // 3x3 matrix[cite: 694]

// Shortcut initialization[cite: 694]
int[][] matrix = {
    {1, 2, 3},
    {4, 5, 6},
    {7, 8, 9}
};

// Standard nested for loop[cite: 695]
for (int i = 0; i < matrix.length; i++) {
    for (int j = 0; j < matrix[i].length; j++) {
        System.out.print(matrix[i][j] + " ");
    }
    System.out.println();
}

// Nested for-each loop[cite: 697]
for (int[] row : matrix) {
    for (int element : row) {
        System.out.print(element + " ");
    }
    System.out.println();
}

// Identity Matrix 
boolean isIdentityMatrix(int[][] matrix) {
    for (int i = 0; i < matrix.length; i++) {
        for (int j = 0; j < matrix[i].length; j++) {
            if (i == j && matrix[i][j] != 1) return false;
            if (i != j && matrix[i][j] != 0) return false;
        }
    }
    return true;
}

// 2 X 2 Matrix Determinant
int determinant2x2(int[][] matrix) {
    return (matrix[0][0] * matrix[1][1]) - (matrix[0][1] * matrix[1][0]);
}

// Matrix Transpose
int[][] transpose(int[][] matrix) {
    int[][] result = new int[matrix[0].length][matrix.length];
    for (int i = 0; i < matrix.length; i++) {
        for (int j = 0; j < matrix[i].length; j++) {
            result[j][i] = matrix[i][j];
        }
    }
    return result;
}

