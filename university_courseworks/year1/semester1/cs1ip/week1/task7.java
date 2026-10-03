public class Task7 {
    public static void main(String[] args) {
        double multipack = 11.0; 
        double cans = 24.0; 
        double unit = multipack/cans;

        System.out.printf("A pack of %.2f cans of cola costs %.2f pounds%n...", cans, multipack); 
        System.out.printf("...so the price per can is %.2f pounds.%n", unit);
    }
}

