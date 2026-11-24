// The code is incomplete with errors;

import java.util.Arrays;
public class Main {
    public static void main(String[] args) {
        double m = 20.0; // Capacity
        double[] p = {24.0, 15.0, 25.0}; // Profit
        double[] w = {15.0, 10.0, 18.0}; // Weights
        double[] x = new double[p.length];

        for (int i = 0; i < x.length; i++) {
        x[i] = 0.0; // Initialisation
        }

        double capacity = m;
 
        for (int i = 0; i < x.length; i++) { // error 1
            if (int i <= x.length - 1) {
                x[i] = capacity / w[i];}
            
            if (w[i] > capacity) {
                break;
            } 
            
            else {
                x[i] = 1.0;
                double capacity -= w[i]; // error 2
            }
        }

       
        System.out.println("\n Fraction solution");
        for (double value : x) {
            System.out.println(value);
        }
    }
}

