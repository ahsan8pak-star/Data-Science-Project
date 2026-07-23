public class Volume {
    public static double sphere(double diameter) {
        double radius = (1 / 2.0) * diameter;
        double volume = (4.0 / 3.0) * Math.PI * Math.pow(radius, 3);
        return volume;
    }

    public static void main(String[] args) {
        System.out.println(sphere(20.24));
    }
}
