"""
Number guessing - find a hidden number from higher/lower feedback.

Tracks an experience score that rises while the guesses are close and falls
when they are not, which gives the loop a second progress signal beyond the
attempt count. The hidden value comes from random, so the number of attempts
is the only thing a test can predict.
"""

import random

EXP = 0 # Started with
print("Welcome to the Guessing Game!")

while EXP < 100: # Game's goal and the only condition to start playing
    answer = random.randint(1, 100) # any number between 1 and 100
    attempts = 10
    count = 0 # used to count attempts made
    print(f"New Round! Current Progress: {EXP} / 100.")
    
    while attempts > 0:
        try:
            guess = int(input("Guess: "))
        except ValueError:
            print("Enter a valid integer.") # specifies to type down what data type
            continue

        count += 1 # adds every attempt failed/tried 
        if guess == answer:
            print(f"Correct. You guessed it in {count} attempt(s)")
            level = attempts * 10
            EXP += level
            print(f"You have gained {level} EXP.")
            break
        
        attempts -= 1 # For every attempt failed
        if attempts > 0:
            print(f"Try again. You have {attempts} tries left.")
            if guess < answer:
                print("Guess higher") # when the guess is lower than the answer
            else:
                print("Guess lower") # when the guess is higher than expcted
                
    if attempts == 0:
        print(f"Unlucky. It was {answer}. You were {100 - EXP} EXP away.")
        break # ends the game

if EXP >= 100:
    print("Congrats. You Won!") # completes the game


