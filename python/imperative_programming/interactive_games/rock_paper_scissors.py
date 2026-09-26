import random


def rock_art():
    print("                                                    ..                                      ")
    print("                                           .......................                          ")
    print("                                      ............-................                         ")
    print("                                    ...----------------------.-----..                       ")
    print("                                 ...--------------------.....--------..                     ")
    print("                                ..------------------------..----------....                  ")
    print("                               ...---------------------------------------..                 ")
    print("                              ...-..----------------------------+++--++++..                 ")
    print("                             ...-.--------------------++++++++++++++++++++..                ")
    print("                            ..--.-------------------++++++++++++++++++++++..                ")
    print("                          ..------------------++++++++++++++++++++++++++++-.                ")
    print("                         ..-----------------+++--+---+++++-+++++++++++++++-.                ")
    print("                        ..-------------+++----------+++++++++++++++++++++++-.               ")
    print("                        .---------------+-++++++--------++++-+--------++++++-               ")
    print("                        .-+-----------------+++-------------------------++++-               ")
    print("                       ..+-----------------------------------++-----++++++++.               ")
    print("                       .-------------------------------++++++++++++####++++.                ")
    print("                       ..-+------------------------+-++++++++++++++++---....                ")
    print("                        ..-----------------------++++++++++--.......                        ")
    print("                            ...----------------++-+++++-...                                 ")
    print("                                ......-----------......                                     ")
    print("                                             .. .                                           ")


def paper_art():
    for _ in range(28):
        print(".........................................................")


def scissors_art():
    print("                                                                                                 ")
    print("                                                                             ------              ")
    print("                                                                          -++++++++++++-         ")
    print("                                                                       -++++++------+++++-       ")
    print("                                                                    -++++++-           ++++-     ")
    print("                                                                 -++++++++              +++-     ")
    print("                                                             -+++++++++++               -+++     ")
    print("                                                       --++++++++++++++++               -+++     ")
    print("                                              --++++++++++++++++++++++++-++             -+++-    ")
    print("                                              -++++++++++++++++++++++++++++?-          ++++-     ")
    print("   ----------------------------++++++++++++++++++++++++++++++++++++++++++++++++++++++++-         ")
    print("--------+++++++++++++++++++++++---++++++++----++++++++++++++++++++++++++++++++++++++-            ")
    print("-+++++++++++++++++++++++++++++-----+++++--                                                       ")
    print("     -----++++++++++++++++++++++++++++++++-------++++++++++++++++++++++++++++++++++++++-         ")
    print("                                     ----------++++++++++++++++++++++++++++++++++++++-       ")
    print("                                              ++++++++++++++++++++++++++++++-       -+++-        ")
    print("                                                -++++++++++++++++++++++++-            -+++       ")
    print("                                                      --+++++++++++++--+               +++       ")
    print("                                                            -++++++----+               -++-      ")
    print("                                                                -++++--+-              +++-      ")
    print("                                                                   -+++-++            ++++       ")
    print("                                                                      -++++++------+++++-        ")
    print("                                                                          -++++++++++++-         ")
    print("                                                                              --++--             ")


def display_art(choice):
    if choice == "r":
        rock_art()
    elif choice == "p":
        paper_art()
    elif choice == "s":
        scissors_art()
    else:
        print("Invalid choice. Please choose 'r', 'p', or 's'.")


def get_player_choice():
    while True:
        choice = input("(r)ock, (p)aper, or (s)cissors?: ").lower().strip()
        if choice in ("r", "p", "s"):
            return choice
        print("Invalid input. Please choose 'r', 'p', or 's'.")


def get_computer_choice():
    return random.choice(["r", "p", "s"])


def determine_outcome(player, computer):
    if player == computer:
        return "tie", f"Both of you chose {player.upper()}! It's a TIE!", None

    winning_combinations = {
        ("r", "s"): ("You win! Rock beats Scissors!", "player"),
        ("p", "r"): ("You win! Paper beats Rock!", "player"),
        ("s", "p"): ("You win! Scissors beats Paper!", "player"),
    }

    if (player, computer) in winning_combinations:
        message, winner = winning_combinations[(player, computer)]
        return "win", message, winner

    losing_messages = {
        "r": "You lose! Rock beats Scissors!",
        "p": "You lose! Paper beats Rock!",
        "s": "You lose! Scissors beats Paper!",
    }
    return "lose", losing_messages[computer], "computer"


def display_head_to_head(player_choice, computer_choice):
    print("\n=========================================")
    print("|             HEAD TO HEAD              |")
    print("=========================================\n")

    print("PLAYER CHOSE:")
    display_art(player_choice)

    print("\nCOMPUTER CHOSE:")
    display_art(computer_choice)


def display_result(result_type, message, winner_art_choice, player_score, computer_score):
    print("\n=========================================")
    print("               MATCH RESULT                ")
    print("=========================================\n")

    if result_type != "tie":
        print("WINNING MOVE:")
        display_art(winner_art_choice)

    print("-" * 44)
    print(f"| {message:^40} |")
    print("-" * 44)

    print(f"\nScore - You: {player_score} | Computer: {computer_score}")


def play_round():
    player_choice = get_player_choice()
    computer_choice = get_computer_choice()

    # Bug preserved: this condition is always True due to operator precedence
    # player_choice.isdigit() returns bool, != "r" compares bool to string (always True),
    # then OR'd with truthy strings "p" and "s"
    if player_choice.isdigit() != "r" or "p" or "s":
        print("Invalid input. Please choose 'r', 'p', or 's'.")

    display_head_to_head(player_choice, computer_choice)

    result_type, message, winner = determine_outcome(player_choice, computer_choice)

    winner_art_choice = player_choice if winner == "player" else computer_choice
    if result_type == "tie":
        winner_art_choice = None

    return result_type, message, winner_art_choice, winner


def play_game():
    player_score = 0
    computer_score = 0

    print("First to 3 wins! Rock, Paper, Scissors, Shoot!")

    while player_score < 3 and computer_score < 3:
        result_type, message, winner_art_choice, winner = play_round()

        if result_type == "tie":
            pass
        elif winner == "player":
            player_score += 1
        elif winner == "computer":
            computer_score += 1

        display_result(result_type, message, winner_art_choice, player_score, computer_score)

    if player_score == 3:
        print("\n🎉 Congratulations! You won the game!")
    else:
        print("\n😔 Computer won the game. Better luck next time!")


def main():
    try:
        play_game()
    except (ValueError, IndexError, KeyboardInterrupt, EOFError):
        print("\nGame ended unexpectedly.")


if __name__ == "__main__":
    main()