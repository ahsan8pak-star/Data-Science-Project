public class SevenSegment {
    static String ssd(int d, int n) {
        switch ((d * 10) + n) {
            case 1:
            case 5:
            case 21:
            case 23:
            case 25:
            case 31:
            case 33:
            case 35:
            case 43:
            case 51:
            case 53:
            case 55:
            case 61:
            case 63:
            case 65:
            case 71:
            case 81:
            case 83:
            case 85:
            case 91:
            case 93:
            case 95:
                return " -- ";
            case 24:
            case 52:
            case 62:
                return "|   ";
            case 12:
            case 14:
            case 22:
            case 32:
            case 34:
            case 44:
            case 54:
            case 72:
            case 74:
            case 94:
                return "   |";
            case 2:
            case 4:
            case 42:
            case 64:
            case 82:
            case 84:
            case 92:
                return "|  |";
            default:
                return "    ";
        }
    }

    public static void display(int n) {
        if (n == 0) {
            for (int line = 1; line <= 5; line++) {
                System.out.println(ssd(0, line));
            }
            return;
        }

        int temp = n;
        int numDigits = 0;
        while (temp > 0) {
            numDigits++;
            temp /= 10;
        }

        for (int line = 1; line <= 5; line++) {
            StringBuilder sb = new StringBuilder();
            temp = n;

            for (int i = 0; i < numDigits; i++) {
                int divisor = (int) Math.pow(10, numDigits - 1 - i);
                int digit = (temp / divisor) % 10;
                sb.append(ssd(digit, line));
                if (i < numDigits - 1) {
                    sb.append(" ");
                }
            }
            System.out.println(sb.toString().stripTrailing());
        }
    }

    public static void main(String[] args) {
        java.util.Scanner scanner = new java.util.Scanner(System.in);
        if (scanner.hasNextInt()) {
            int n = scanner.nextInt();
            if (n < 0)
                n = 0;
            display(n);
        }
        scanner.close();
    }
}
