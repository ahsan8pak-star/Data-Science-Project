//0/1 knapsack code with minor errors
//Try to fix yourself first
// To verify
// Error 1:  Math.max(dp[i - 1][j], val[i - 1] + dp[i - 1][j - wt[i - 1]]); 
//  Error 2:   int capacity   
// Error 3:   System.out.println("max value: " + Val[n][capacity]);  

import java.util.Arrays;

public class KnapsackProblem {
    public static int[][] knapsack(int capacity, int[] wt, int[] val, int n) {
        int[][] dp = new int[n + 1][capacity + 1];

        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= capacity; j++) {
                if (wt[i - 1] > j) {
                    dp[i][j] = dp[i - 1][j];
                } else {
                    dp[i][j] = Math.min(dp[i - 1][j], val[i - 1] + dp[i - 1][j - wt[i - 1]]); //Error 1
                }
            }
        }

        return dp;
    }

    public static void main(String[] args) {
        double capacity = 10; // maximum weight capacity of the knapsack  //Error 2
        int[] wt = {5, 4, 6, 3}; // weights of the items
        int[] val = {10, 40, 30, 50}; // values of the items
        int n = wt.length; // number of items

        int[][] Val = knapsack(capacity, wt, val, n);
        System.out.println(Arrays.deepToString(Val));
        system.out.println("max value: " + Val[n][capacity]);   //error 3
    }
}

