public class Task12 {
    public static void main(String[] args) {
        double initialVelocity = 12.0; 
        double acceleration = 3.0; 
        double time = 5.0;

        double finalVelocity = initialVelocity + (acceleration * time); // v = u + at
        double displacement = (initialVelocity * time) + (0.5 * acceleration * time * time); // s = ut + 1/2 at^2
        
        System.out.println("The final velocity is: " + finalVelocity + " m/s"); 
        System.out.println("The displacement is: " + displacement + " meters");
    }
}

