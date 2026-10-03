initialVelocity = 12.0
acceleration = 3.0
time = 5.0

finalVelocity = initialVelocity + (acceleration * time)  # v = u + at
displacement = (initialVelocity * time) + (0.5 * acceleration * time * time)  # s = ut + 1/2 at^2

print("The final velocity is: " + str(finalVelocity) + " m/s")
print("The displacement is: " + str(displacement) + " meters")

