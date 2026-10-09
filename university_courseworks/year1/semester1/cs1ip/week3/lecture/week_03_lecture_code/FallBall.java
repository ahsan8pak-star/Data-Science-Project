public class FallBall {
    public static void main(String[] args) throws InterruptedException {
        // clear screen and hide cursor
        String hide = "\033[?25l";
        String erase = "\033[2J";
        System.out.print(erase);
        System.out.print(hide);
        // display ball position
        String home = "\033[H";
        double height = 20.0;
        int rows = 20;
        double velocity = 0.0;
        double acceleration = -0.1;
        while (true) {
            height = height + velocity;
            velocity = velocity + acceleration;
            if (height <= 0)
                break;
            System.out.print(home);
            int row = rows - (int) height;
            for (int y = 1; y <= rows; y++) {
                if (y == row) {
                    System.out.println("O");
                } else {
                    System.out.println(" ");
                }
            }
            Thread.sleep(60);
        }
    }
}
