import random

EXP = 0
print("Welcome to the Guessing Game!")

while EXP < 100:
    answer = random.randint(1, 100)
    attempts = 5
    count = 0
    print(f"New Round! Current Progress: {EXP} / 100.")
    
    while attempts > 0:
        try:
            guess = int(input("Guess: "))
        except ValueError:
            print("Enter a valid integer.")
            continue

        count += 1
        if guess == answer:
            print(f"Correct. You guessed it in {count} attempts")
            level = attempts * 10
            EXP += level
            print(f"You have gained {level} EXP.")
            break
        
        attempts -= 1
        if attempts > 0:
            print(f"Try again. You have {attempts} tries left.")
            if guess < answer:
                print("Guess higher")
            else:
                print("Guess lower")
                
    if attempts == 0:
        print(f"Unlucky. It was {answer}. You were {100 - EXP} EXP away.")
        break

if EXP >= 100:
    print("Congrats. You Won!")