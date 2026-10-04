# Matrix Allocation (3x3 matrix initialized with zeros)
matrix = [[0] * 3 for _ in range(3)]

# Shortcut Initialization
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# Standard nested for loop (index-based)
for i in range(len(matrix)):

    for j in range(len(matrix[i])):
        print(matrix[i][j], end=" ")

    print()

# Nested for-each loop
for row in matrix:

    for element in row:
        print(element, end=" ")

    print()

# Identity Matrix Check
def is_identity_matrix(matrix: list[list[int]]) -> bool:

    for i in range(len(matrix)):

        for j in range(len(matrix[i])):

            if i == j and matrix[i][j] != 1:
                return False

            if i != j and matrix[i][j] != 0:
                return False

    return True

# 2 x 2 Matrix Determinant
def determinant_2x2(matrix: list[list[int]]) -> int:
    return (matrix[0][0] * matrix[1][1]) - (matrix[0][1] * matrix[1][0])

# Matrix Transpose
def transpose(matrix: list[list[int]]) -> list[list[int]]:
    rows = len(matrix)
    cols = len(matrix[0])
    result = [[0] * rows for _ in range(cols)]

    for i in range(rows):
        for j in range(cols):
            result[j][i] = matrix[i][j]

    return result

"""
Pythonic one-liner alternative for Transpose:
def transpose(matrix):
    return [list(col) for col in zip(*matrix)]
"""

