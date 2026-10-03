leg1Distance = 120.0  # km
leg1Speed = 80.0  # km/h
leg2Distance = 200.0  # km
leg2Speed = 100.0  # km/h

restBetweenLegsMinutes = 10
fuelStopAfterMinutes = 15

leg1Hours = leg1Distance / leg1Speed  # 1.5 h
leg2Hours = leg2Distance / leg2Speed  # 2.0 h
drivingHours = leg1Hours + leg2Hours  # 3.5 h

totalRestMinutes = restBetweenLegsMinutes + fuelStopAfterMinutes
totalHours = drivingHours + totalRestMinutes / 60.0

totalHoursWhole = int(totalHours)
totalMinutesRemainder = int(round((totalHours - totalHoursWhole) * 60))

if totalMinutesRemainder == 60:
    totalHoursWhole += 1
    totalMinutesRemainder = 0

totalDistance = leg1Distance + leg2Distance
averageSpeed = totalDistance / totalHours

print("Total travel time: %d hours %d minutes\n" % (totalHoursWhole, totalMinutesRemainder))
print("Overall average speed: %.2f km/h\n" % (averageSpeed))

