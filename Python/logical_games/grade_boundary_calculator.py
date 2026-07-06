grade = input("Score (out of 100): ")

print(f"{int(grade)} / 100")

if int(grade) > 100 or int(grade) < 0:
    print(f"{str(grade)}!!! HOW?! YOU ARE LYING!")

elif int(grade) == 100:    
    print(f"{str(grade)}! Unbelievable!")

elif int(grade) >= 90:
    print(f"{str(grade)}! Really Good.")

elif int(grade) >= 80:
    print(f"{str(grade)}! Solid.")

elif int(grade) >= 70:
    print(f"{str(grade)}! Decent!")

elif int(grade) >= 60:
    print(f"{str(grade)}! Not bad!")

elif int(grade) >= 50:
    print(f"{str(grade)}! Well done! You passed!")

elif int(grade) >= 40:
    print(f"{str(grade)}. Better luck next time.")

elif int(grade) >= 30:
    print(f"{str(grade)}. You must have slept the exam")

elif int(grade) >= 20:
    print(f"{str(grade)}. We can do way better, You know that.")

elif int(grade) >= 10:
    print(f"{str(grade)}. Did you forgot the exam?")

elif int(grade) > 0:
    print(f"{str(grade)}!!! SERIOUSLY?! THAT LOW?!! DO BETTER!!!")

else:
    print(f"{str(grade)}!!! ARE YOU KIDDING ME???!!! GET OUT!!!")

