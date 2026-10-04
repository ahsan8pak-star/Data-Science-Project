public class Week1Demo {
    public static void main(String[] args) {
        // Variables and primitive types
        String uni = "Reading";
        int totalDays = 275;
        int targetDays = 360;
        
        // Division and modulus arithmetic
        int weeks = (targetDays - totalDays) / 7;
        int days = (targetDays - totalDays) % 7;
        
        // Formatted console output
        System.out.printf("The University of %s was founded in %d.%n", uni, 1892);
        System.out.printf("There are %d weeks and %d days until Christmas.%n", weeks, days);
    }
}

