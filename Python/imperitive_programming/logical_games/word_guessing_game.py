# Uses a random function for selecting the words
import random

# The list of words available for the game to choose from
# Has to be lowercase to avoid functional errors based on line 27-28
word_bank = ['python', 'java', 'lua', 'gitlab', 'github', 'copilot', 'powershell', 'linux', 'windows', 'arch', 'ubuntu'] 

# Outer loop: Keeps the whole game restarting so you can play multiple rounds
while True: 

    # Randomly picks one word from the word bank list
    word = random.choice(word_bank) 

    # Creates an underscore for every letter of the secret word to be guessed
    guessedWord = ['_'] * len(word) 

    # Total number of attempts to guess the word
    attempts = 10 

    # Inner loop: Keeps the game running while attempts are greater than 0
    while attempts > 0:

        # Shows the secret word progress with spaces between the underscores
        print('\nCurrent word: ' + ' '.join(guessedWord))
    
        # Gets the player's guess and automatically turns it into lowercase
        guess = input('Guess a letter: ').lower()
        
        # Checks if the guessed letter is actually inside the secret word
        if guess in word:
            
            # Looks through every letter position in the word
            for i in range(len(word)):
                
                # If the letter at this specific position matches the guess
                if word[i] == guess:
            
                    # Replaces the underscore with the correct letter at that exact spot
                    guessedWord[i] = guess
            
            # Prints a success message after updating the letters
            print('Great guess!')
        
        # Runs if the guessed letter is not in the word
        else:
        
            # Subtracts 1 from your remaining turns
            attempts -= 1
        
            # Tells the player they missed and shows how many turns are left
            print('Wrong guess! Attempts left: ' + str(attempts)) 
            
        # Checks if there are no underscores left (meaning you found all the letters)
        if '_' not in guessedWord:
        
            # Celebrates the win and shows the completed word
            print('\nCongratulations!!! You guessed the word: ' + word)
        
            # Stops the game loop immediately
            break

    # Runs if you run out of turns and the word is still hidden
    if attempts == 0 and '_' in guessedWord:

        # Game over message and reveals the final answer
        print('\nYou\'ve run out of attempts! The word was: ' + word)

    # Asks the player if they want to play another game round
    play_again = input('\nDo you want to play again? (y/n): ').lower()
    
    # If they type anything except 'y', stop the whole program
    if play_again != 'y':
        print('\nThanks for playing! Bye Bye!!!')
        
        # Stops the main outer loop completely
        break

