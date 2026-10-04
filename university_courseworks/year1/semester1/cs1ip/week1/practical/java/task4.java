public class Task4 {
    public static void main(String[] args) {
        String x = "Goodbye."; 
        String y = "Hello."; 
        String tmp = x; 
        
        x = y; 
        y = tmp; 

        System.out.println(x); 
        System.out.println(y);
    }
}

