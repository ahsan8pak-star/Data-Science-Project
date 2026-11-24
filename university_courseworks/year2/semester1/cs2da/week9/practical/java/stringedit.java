
//code for string edit containing minor errors
// Error 1:  cost[i][0] = 0; 
// Error 2:  for ( int i = 0; i < x.size(); i++) { 
// Error  3: Math.max(cost[i][j + 1] + 1, Math.min(cost[i + 1][j] + 1, cost[i][j] + 2)); 

import java.util.ArrayList;

public class StringDistance {
    public static void main(String[] args) {
        String str1 = "aabab";
        String str2 = "babb";

        ArrayList<Character> x = new ArrayList<>();
        for (char c : str1.toCharArray()) {
            x.add(c);
        }
        ArrayList<Character> y = new ArrayList<>();
        for (char c : str2.toCharArray()) {
            y.add(c);
        }

        int[][] cost = new int[x.size() + 1][y.size() + 1];
        for (int j = 0; j <= y.size(); j++) {
            cost[0][j] = j;
        }
        for (int i = 0; i <= x.size(); i++) {
            cost[i][0] = 1;   //error 1           
        }

        for (  i = 0; i < x.size(); i++) {    //error 2
            for (int j = 0; j < y.size(); j++) {
                if (y.get(j) == x.get(i)) {
                    cost[i + 1][j + 1] = cost[i][j];
                } else {
                    cost[i + 1][j + 1] = Math.max(cost[i][j + 1] + 1, Math.min(cost[i + 1][j] + 1, cost[i][j] + 2)); //error 3
                }
            }
        }

        System.out.println("\nCost matrix");
        for (int[] row : cost) {
            for (int value : row) {
                System.out.print(value + " ");
            }
            System.out.println();
        }
    }
}

