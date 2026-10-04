# The outer loop iterates through 1, 2, and 3
for i in range(1, 4):

    # The inner loop iterates through 1 and 2
    for j in range(1, 3):

        # Conditional check to trigger an early exit
        if i == 2 and j == 2:
            # Exits ONLY the inner 'j' loop; the outer 'i' loop continues
            break

        print(f"i={i}, j={j}")

