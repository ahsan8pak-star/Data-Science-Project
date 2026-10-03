// The outer loop manages the 'i' variable
for (int i = 1; i <= 3; i++) { 
    
    // The inner loop fully executes its cycle for every single outer loop iteration
    for (int j = 1; j <= 2; j++) { 
        
        // Conditional check to trigger an early exit
        if (i == 2 && j == 2) { 
            // Exits ONLY the inner 'j' loop; the outer 'i' loop will move to i=3
            break; 
        }
        System.out.print("i=" + i); 
        System.out.println(", j=" + j); 
    }
}

