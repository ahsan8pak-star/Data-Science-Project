def AverageGrades(grades, weights):
    
    # Null / empty check
    if grades is None or weights is None:
        return []

    students = len(grades)
    if students == 0:
        return []

    comps = len(weights)
    result = [0] * students  # Creates a list of length 'students' pre-filled with 0

    for i in range(students):
        total_sum = 0
        
        for j in range(comps):
            total_sum += grades[i][j] * weights[j]
        
        # Integer division in Python is // (or / if you want floating point)
        result[i] = total_sum // 100

    return result


if __name__ == "__main__":

    # Define the input data in main
    grades = [[51, 83, 28], [0, 38, 95]]
    weights = [30, 40, 30]

    av = AverageGrades(grades, weights)
    print(av)  # Outputs: [56, 43]

