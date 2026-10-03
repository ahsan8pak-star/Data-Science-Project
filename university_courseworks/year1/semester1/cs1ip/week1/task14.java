public class Task14 { 
    public static void main(String[] args) { 
        double leg1Distance = 120.0;  // km 
        double leg1Speed    = 80.0;   // km/h 
        double leg2Distance = 200.0;  // km 
        double leg2Speed    = 100.0;  // km/h 
         
        int restBetweenLegsMinutes = 10; 
        int fuelStopAfterMinutes   = 15; 
        
        double leg1Hours = leg1Distance / leg1Speed;  // 1.5 h 
        double leg2Hours = leg2Distance / leg2Speed;  // 2.0 h 
        double drivingHours = leg1Hours + leg2Hours;  // 3.5 h 
        
        int totalRestMinutes = restBetweenLegsMinutes + fuelStopAfterMinutes;  
        double totalHours = drivingHours + totalRestMinutes / 60.0; 
        
        int totalHoursWhole = (int) totalHours; 
        int totalMinutesRemainder = (int) Math.round((totalHours - totalHoursWhole) * 60); 
        
        if (totalMinutesRemainder == 60) { 
            totalHoursWhole += 1; 
            totalMinutesRemainder = 0; 
        } 
        
        double totalDistance = leg1Distance + leg2Distance; 
        double averageSpeed = totalDistance / totalHours; 
        
        System.out.printf("Total travel time: %d hours %d minutes%n", totalHoursWhole, totalMinutesRemainder); 
        System.out.printf("Overall average speed: %.2f km/h%n", averageSpeed); 
    } 
}

