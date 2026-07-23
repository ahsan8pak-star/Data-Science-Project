import random

# Dictionary instead of def case switch to ease of memory management and readability
dice_art = {
    1: ("┌─────────┐",
        "│         │",
        "│    ●    │",
        "│         │",
        "└─────────┘"),
    2: ("┌─────────┐",
        "│  ●      │",
        "│         │",
        "│      ●  │",
        "└─────────┘"),
    3: ("┌─────────┐",
        "│  ●      │",
        "│    ●    │",
        "│      ●  │",
        "└─────────┘"),
    4: ("┌─────────┐",
        "│  ●   ●  │",
        "│         │",
        "│  ●   ●  │",
        "└─────────┘"),
    5: ("┌─────────┐",
        "│  ●   ●  │",
        "│    ●    │",
        "│  ●   ●  │",
        "└─────────┘"),
    6: ("┌─────────┐",
        "│  ●   ●  │",
        "│  ●   ●  │",
        "│  ●   ●  │",
        "└─────────┘")
}


def main():
    
    while True: # Assumes the program running, hence becoming it all true

        # Initialise game states i.e. begin
        player_score = 0
        computer_score = 0

        # Randomly establish a target between 20 to 50 range
        target_score = random.randint(20, 50) # Both numbers are inclusive, meaning both are included -> random.randint(a, b)

        # Welcome Screen Box
        # Centre alignment (^) for desirable TUI
        print("==============================================")
        print(f"| {'DICE RACE':^42} |")
        print(f"| {f'FIRST PLAYER TO {target_score} POINTS WINS!':^42} |") 
        print("==============================================")

        # Turn-based gameplay loop
        while player_score < target_score and computer_score < target_score:
    
        # Display Current Board Standings
        # Centre alignment (^) for desirable TUI
        # Player centre alignment one less due to its extra whitepace
        print("\n==============================================")
        print(f"| {'CURRENT SCORE':^42} |") 
        print("==============================================")
        print(f"| {'YOU: ' + str(player_score):^19} | {'COMPUTER: ' + str(computer_score):^20} |") 
        print(f"| {f'TARGET GOAL: {target_score}':^42} |") 
        print("----------------------------------------------")

        # =========================================
        #               PLAYER TURN                
        # =========================================
        print("\nPLAYER TURN")
        input("Press Enter to shake and roll your dice...")

        # Fully randomised: decides to roll between 1 to 3 dice automatically
        num_of_dice = random.randint(1, 3) # randint -> both numbers are inclusive

        # Starting point i.e. about to take the first turn
        player_dice = [] 
        player_round_score = 0
        
        # Loop exactly the number of times decided by our random dice count
        # Use '_' for variable name due to the lack of tracking index numbers i.e. unecessary
        for _ in range(num_of_dice):

            roll = random.randint(1, 6) # 1 to 6 -> both inclusive
            player_dice.append(roll) # Adds the single result of that round made
            player_round_score += roll # Includes to accumalate the total round score

        player_score += player_round_score # Totalise all of the rounds previously including the current round completed.

        # HORIZONTAL TUI DISPLAY
        print("\nYOUR ROLL:")
        print("----------------------------------------------")

        for line in range(5): # 5 rows in 'dice_art' dictionary

            dice_line_string = "  ".join([dice_art.get(die)[line] for die in player_dice])
            # List Comprehension: Loops through every rolled value stored in 'player_dice'.
            # For each value, it fetches its 5-line art array from the 'dice_art' dictionary,
            # and extracts just the specific string row matching the current outer 'line' index loop.
            # "  ".join(...) glues these matching string rows together horizontally with 2 spaces in between.

            print(f"| {dice_line_string:^42} |") # Prints combined lines of dice faces, all centered aligned

        # Centre alignment (^) for desirable TUI
        print("----------------------------------------------")
        print(f"| {f'Round Total: +{player_round_score} (Rolled {num_of_dice} Di(c)e)':^42} |")
        print(f"| {f'Your New Score: {player_score}':^42} |")
        print("----------------------------------------------")

        # Immediate Win Check
        if player_score >= target_score:
            break

        # =========================================
        #              COMPUTER TURN               
        # =========================================
        print("\nCOMPUTER TURN")
        input("Press Enter to allow the Computer to roll...")
        
        # Computer also rolls a completely random handful of 1 to 3 dice
        comp_num_dice = random.randint(1, 3)
        computer_dice = []
        computer_round_score = 0

        # Comment made on lines 92 to 95 about Player Turn
        for _ in range(comp_num_dice):
            roll = random.randint(1, 6)
            computer_dice.append(roll)
            computer_round_score += roll

        computer_score += computer_round_score

        print("\nCOMPUTER'S ROLL:")
        print("----------------------------------------------")

        # Replicates the row-by-row horizontal ASCII rendering strategy for the computer's roll array
        for line in range(5):
            dice_line_string = "  ".join([dice_art.get(die)[line] for die in computer_dice])
            print(f"| {dice_line_string:^42} |")

        # Centre alignment (^) for desirable TUI
        print("----------------------------------------------")
        print(f"| {f'Round Total: +{computer_round_score} (Rolled {comp_num_dice} Di(c)e)':^42} |")
        print(f"| {f'Computer New Score: {computer_score}':^42} |")
        print("----------------------------------------------")

        # =========================================
        #                  WINNER               
        # =========================================
        print("\n==============================================")
        print(f"| {'GAME OVER':^42} |") # Centre alignment (^) for desirable TUI
        print("==============================================")

        if player_score >= target_score:
            victory_text = "CONGRATULATIONS! YOU WIN!"
            victory_score = player_score - computer_score
            victory_message = f"You won by {victory_score} point(s)!"
        else:
            victory_text = "Unlucky! The COMPUTER won!"
            victory_score = computer_score - player_score
            victory_message = f"You lost by {victory_score} point(s)!"

        print(f"| {victory_text:^42} |")
        print("----------------------------------------------")
        print(f"| {'FINAL SCORE':^42} |")
        print(f"| {f'YOU: {player_score}  |  COMPUTER: {computer_score}':^42} |")
        print("----------------------------------------------")
        print(f"| {victory_message:^42} |")
        print("==============================================")

        print()
        play_again = input("Do you want to play again? (y/n): ").strip().lower()
    
        # If they choose anything other than 'y' or 'yes', break the main loop
        if play_again != 'y' and play_again != 'yes':
            print("\n==============================================")
            print(f"| {'THANKS FOR PLAYING!':^42} |")
            print("==============================================\n")
            break

if __name__ == "__main__":
    main()

