public class SelectionStatements {
    public static void main(String[] args) {
        int score = 85;
        char grade = 'B';

        // Conditional logic using if, else if, and else with relational and logical operators
        if (score >= 90 && score <= 100) {
            System.out.println("Grade: A");
        } else if (score >= 80 || score == 85) {
            System.out.println("Grade: B");
        } else {
            System.out.println("Grade: C or lower");
        }

        // Selection using switch-case statements
        switch (grade) {
            case 'A':
                System.out.println("Status: Excellent");
                break;
            case 'B':
                System.out.println("Status: Good");
                break;
            default:
                System.out.println("Status: Passing or Needs Improvement");
                break;
        }
    }
}

