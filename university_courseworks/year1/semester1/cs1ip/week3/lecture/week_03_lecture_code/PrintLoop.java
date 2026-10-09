public class PrintLoop {
    static void main(String args[]) {
        for (int i = 1; i <= 3; i++) {
            int j; // allow be used in if
            for (j = 1; j <= 2; j++) {
                if (i == 2 && j == 2) {
                    break;
                }
                System.out.print("i=" + i);
                System.out.println(",j=" + j);
            }
            if (i == 2 && j == 2) {
                break;
            }
        }
    }
}
