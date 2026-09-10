public class AverageGrades {
    static int[] average_grades(int grades[][], int weights[]) {
        if (grades == null || weights == null)
            return new int[0];

        int students = grades.length;
        if (students == 0)
            return new int[0];

        int comps = weights.length;
        int[] result = new int[students];

        for (int i = 0; i < students; i++) {
            int sum = 0;
            for (int j = 0; j < comps; j++) {
                sum += grades[i][j] * weights[j];
            }
            result[i] = sum / 100;
        }

        return result;
    }

    public static void main(String[] args) {
        int[][] grades = { { 51, 83, 28 }, { 0, 38, 95 } };
        int[] weights = { 30, 40, 30 };

        int[] av = average_grades(grades, weights);

        System.out.println(av);
    }

}

