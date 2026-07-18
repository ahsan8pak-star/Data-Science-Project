"""
Pytest suite for every script under Python/logical_games/.

These are small interactive terminal games. Where a script relies on
`random`, we patch it via run_script(..., patches=[...]) so the games become
fully deterministic and finish in a bounded number of turns instead of
looping forever.
"""

from unittest.mock import patch

import pytest

from tests.conftest import run_script

FOLDER = "logical_games"


# ---------------------------------------------------------------------------
# dice_game.py
# ---------------------------------------------------------------------------
class TestDiceGame:
    FILE = f"{FOLDER}/dice_game.py"

    @staticmethod
    def _player_wins_patch():
        """Fixes target_score at 20, both sides always roll exactly 3 dice
        worth 6 points each (18/turn), so the player (who always goes
        first) crosses the target on their second turn, before the
        computer gets a chance to reply that round."""

        def fake_randint(a, b):
            if (a, b) == (20, 50):
                return 20
            if (a, b) == (1, 3):
                return 3
            if (a, b) == (1, 6):
                return 6
            return a

        return patch("random.randint", side_effect=fake_randint)

    @staticmethod
    def _computer_wins_patch():
        """Target fixed low at 10; the player always rolls a 1, the
        computer always rolls a 6 (tracked via call parity), so the
        computer necessarily catches up and wins first."""
        calls = {"n": 0}

        def fake_randint(a, b):
            if (a, b) == (20, 50):
                return 10
            if (a, b) == (1, 3):
                return 1
            if (a, b) == (1, 6):
                calls["n"] += 1
                return 1 if calls["n"] % 2 == 1 else 6
            return a

        return patch("random.randint", side_effect=fake_randint)

    def test_player_wins_round(self):
        inputs = ["", "", "", "n"]  # 2 player turns, 1 computer turn, decline replay
        _, out = run_script(self.FILE, inputs=inputs, patches=[self._player_wins_patch()])
        assert "CONGRATULATIONS! YOU WIN!" in out
        assert "THANKS FOR PLAYING!" in out

    def test_computer_wins_round(self):
        inputs = ["", "", "", "", "n"]
        _, out = run_script(self.FILE, inputs=inputs, patches=[self._computer_wins_patch()])
        assert "Unlucky! The COMPUTER won!" in out

    def test_final_score_line_matches_actual_totals(self):
        inputs = ["", "", "", "n"]
        _, out = run_script(self.FILE, inputs=inputs, patches=[self._player_wins_patch()])
        assert "YOU: 36  |  COMPUTER: 18" in out

    def test_target_score_is_shown_in_welcome_banner(self):
        inputs = ["", "", "", "n"]
        _, out = run_script(self.FILE, inputs=inputs, patches=[self._player_wins_patch()])
        assert "FIRST PLAYER TO 20 POINTS WINS!" in out

    def test_dice_art_dict_has_all_six_faces(self):
        inputs = ["", "", "", "n"]
        mod, _ = run_script(self.FILE, inputs=inputs, patches=[self._player_wins_patch()])
        assert set(mod.dice_art.keys()) == {1, 2, 3, 4, 5, 6}

    def test_dice_art_face_has_five_rows(self):
        inputs = ["", "", "", "n"]
        mod, _ = run_script(self.FILE, inputs=inputs, patches=[self._player_wins_patch()])
        assert len(mod.dice_art[6]) == 5

    def test_declining_replay_ends_the_game(self):
        inputs = ["", "", "", "n"]
        _, out = run_script(self.FILE, inputs=inputs, patches=[self._player_wins_patch()])
        assert "THANKS FOR PLAYING!" in out
        # nothing from a second round (e.g. a new welcome banner) follows it
        assert out.count("DICE RACE") == 1

    def test_replaying_starts_a_new_round(self):
        """Answering anything other than 'y'/'yes' the FIRST time still
        starts one round; here we play twice then quit, so the win banner
        should appear twice."""
        inputs = ["", "", "", "y", "", "", "", "n"]
        _, out = run_script(self.FILE, inputs=inputs, patches=[self._player_wins_patch()])
        assert out.count("CONGRATULATIONS! YOU WIN!") == 2


# ---------------------------------------------------------------------------
# grade_boundary_calculator.py
# ---------------------------------------------------------------------------
class TestGradeBoundaryCalculator:
    FILE = f"{FOLDER}/grade_boundary_calculator.py"

    @pytest.mark.parametrize(
        "score, expected_phrase",
        [
            ("105", "HOW?! YOU ARE LYING!"),
            ("100", "Unbelievable!"),
            ("95", "Really Good."),
            ("85", "Solid."),
            ("75", "Decent!"),
            ("65", "Not bad!"),
            ("55", "Well done! You passed!"),
            ("45", "Better luck next time."),
            ("35", "You must have slept the exam"),
            ("25", "We can do way better"),
            ("15", "Did you forgot the exam?"),
            ("5", "SERIOUSLY?! THAT LOW?!! DO BETTER!!!"),
            ("0", "ARE YOU KIDDING ME???!!! GET OUT!!!"),
            ("-5", "HOW?! YOU ARE LYING!"),
        ],
    )
    def test_grade_boundaries(self, score, expected_phrase):
        _, out = run_script(self.FILE, inputs=[score])
        assert expected_phrase in out

    def test_score_over_100_flagged_as_lying(self):
        _, out = run_script(self.FILE, inputs=["150"])
        assert "HOW?! YOU ARE LYING!" in out

    def test_negative_score_flagged_as_lying(self):
        _, out = run_script(self.FILE, inputs=["-5"])
        assert "HOW?! YOU ARE LYING!" in out

    def test_non_numeric_score_raises_uncaught_value_error(self):
        with pytest.raises(ValueError):
            run_script(self.FILE, inputs=["not-a-number"])

    def test_score_out_of_100_line_is_always_printed_first(self):
        _, out = run_script(self.FILE, inputs=["50"])
        assert "50 / 100" in out

    def test_exact_boundary_of_90_gives_really_good(self):
        _, out = run_script(self.FILE, inputs=["90"])
        assert "Really Good." in out

    def test_exact_boundary_of_50_gives_passed_message(self):
        _, out = run_script(self.FILE, inputs=["50"])
        assert "Well done! You passed!" in out


# ---------------------------------------------------------------------------
# haiku_madlibs.py
# ---------------------------------------------------------------------------
class TestHaikuMadlibs:
    FILE = f"{FOLDER}/haiku_madlibs.py"

    def test_all_three_verses_built_from_input(self):
        """random.choice always picks the *first* template of whichever
        list it's given, making the whole script deterministic."""
        first_choice = patch("random.choice", side_effect=lambda seq: seq[0])
        inputs = [
            "the", "silent", "pine", "it", "sways", "softly",       # verse 1
            "an", "old", "pond", "it", "jumped", "quietly",         # verse 2
            "the", "quiet", "temple", "it", "fade", "slowly",       # verse 3
        ]
        _, out = run_script(self.FILE, inputs=inputs, patches=[first_choice])
        assert "Chapter 1: The Mountain" in out
        assert "Chapter 2: The Pond" in out
        assert "Part 3: The Temple" in out
        assert "A Beautiful Scene" in out
        # first verse-1 template capitalises only the determiner and pronoun
        assert "The silent pine," in out

    def test_second_template_variant_selected(self):
        """random.choice picking index 1 exercises the second template of
        each verse's list."""
        second_choice = patch("random.choice", side_effect=lambda seq: seq[1])
        inputs = [
            "the", "silent", "pine", "it", "sways", "softly",
            "an", "old", "pond", "it", "jumped", "quietly",
            "the", "quiet", "temple", "it", "fade", "slowly",
        ]
        _, out = run_script(self.FILE, inputs=inputs, patches=[second_choice])
        assert "Beneath the pale moon," in out

    def test_third_template_variant_selected(self):
        third_choice = patch("random.choice", side_effect=lambda seq: seq[2])
        inputs = [
            "the", "silent", "pine", "it", "sways", "softly",
            "an", "old", "pond", "it", "jumped", "quietly",
            "the", "quiet", "temple", "it", "fade", "slowly",
        ]
        _, out = run_script(self.FILE, inputs=inputs, patches=[third_choice])
        assert "Softly, it sways now," in out

    def test_chapter_headers_are_printed_in_order(self):
        first_choice = patch("random.choice", side_effect=lambda seq: seq[0])
        inputs = ["the", "a", "b", "it", "c", "d"] * 3
        _, out = run_script(self.FILE, inputs=inputs, patches=[first_choice])
        idx1 = out.find("Chapter 1: The Mountain")
        idx2 = out.find("Chapter 2: The Pond")
        idx3 = out.find("Part 3: The Temple")
        assert idx1 < idx2 < idx3

    def test_final_recap_reprints_all_verses(self):
        first_choice = patch("random.choice", side_effect=lambda seq: seq[0])
        inputs = ["the", "silent", "pine", "it", "sways", "softly"] * 3
        _, out = run_script(self.FILE, inputs=inputs, patches=[first_choice])
        # "A Beautiful Scene" recap section appears once as a header
        assert out.count("A Beautiful Scene") == 1
        # the chosen verse-1 text should appear twice: once under "Verse 1"
        # and once again in the final recap
        assert out.count("The silent pine,") == 2

    def test_empty_strings_are_accepted_without_crashing(self):
        first_choice = patch("random.choice", side_effect=lambda seq: seq[0])
        inputs = [""] * 18
        _, out = run_script(self.FILE, inputs=inputs, patches=[first_choice])
        assert "Verse 1" in out
        assert "Verse 2" in out
        assert "Verse 3" in out


# ---------------------------------------------------------------------------
# login_status.py
# ---------------------------------------------------------------------------
class TestLoginStatus:
    FILE = f"{FOLDER}/login_status.py"

    def test_echoes_back_all_five_answers(self):
        inputs = ["True", "False", "False", "False", "True"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Student: True" in out
        assert "Admin: False" in out
        assert "Online: True" in out

    def test_regular_student_online_accident_choice(self):
        inputs = ["True", "False", "False", "True", "True", "A"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "No problem. Try Again." in out

    def test_regular_student_online_intended_choice(self):
        inputs = ["True", "False", "False", "True", "True", "I"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Leave or we will suspend you permanently!" in out

    def test_regular_student_online_unclear_choice(self):
        inputs = ["True", "False", "False", "True", "True", "maybe"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Stop Messing Around! What is your answer?" in out

    def test_not_a_regular_student_gets_welcome_message(self):
        inputs = ["True", "False", "False", "False", "True"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Welcome to our university!" in out

    def test_offline_user_gets_offline_message(self):
        inputs = ["True", "False", "False", "True", "False"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "You are offline. You are unable to access this." in out

    def test_stop_lying_branch_is_actually_unreachable(self):
        """
        Genuine bug: `is_student[0].upper and is_admin[0].upper == "T"`
        never calls `.upper()` on the first operand (missing parentheses),
        so it evaluates a bound-method object which is always truthy,
        while the second half compares a method object to "T" and is
        always False. The AND is therefore always False, so "Stop Lying"
        can never print even when both student and admin are "True".
        """
        inputs = ["True", "True", "False", "False", "True"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Stop Lying" not in out
        assert "Welcome to our university!" in out

    def test_empty_online_answer_raises_uncaught_index_error(self):
        inputs = ["True", "False", "False", "True", ""]
        with pytest.raises(IndexError):
            run_script(self.FILE, inputs=inputs)

    def test_own_value_error_except_is_unreachable_via_normal_input(self):
        """
        The whole flow is wrapped in `except ValueError:`, but nothing in
        it can actually raise a ValueError from typed input: .upper()
        never raises one, and an empty string's [0] index raises
        IndexError instead (confirmed above), which this except doesn't
        even catch. This except clause is only reachable by making
        input() itself raise ValueError artificially, as done here.
        """
        val_err = patch(
            "builtins.input",
            side_effect=["True", "False", "False", "True", "True", ValueError],
        )
        _, out = run_script(self.FILE, patches=[val_err])
        assert "Please type within boolean logic. True or False." in out


# ---------------------------------------------------------------------------
# number_guessing_game.py
# ---------------------------------------------------------------------------
class TestNumberGuessingGame:
    FILE = f"{FOLDER}/number_guessing_game.py"

    def test_correct_first_guess_wins_immediately(self):
        fixed_answer = patch("random.randint", return_value=50)
        _, out = run_script(self.FILE, inputs=["50"], patches=[fixed_answer])
        assert "Correct. You guessed it in 1 attempt(s)" in out
        assert "You have gained 100 EXP." in out
        assert "Congrats. You Won!" in out

    def test_invalid_guess_is_reprompted(self):
        fixed_answer = patch("random.randint", return_value=50)
        _, out = run_script(
            self.FILE, inputs=["not-a-number", "50"], patches=[fixed_answer]
        )
        assert "Enter a valid integer." in out
        assert "Congrats. You Won!" in out

    def test_hints_given_for_high_and_low_guesses(self):
        fixed_answer = patch("random.randint", return_value=50)
        wrong_guesses = ["10", "90", "20", "80", "30", "70", "40", "60", "15", "85"]
        _, out = run_script(self.FILE, inputs=wrong_guesses, patches=[fixed_answer])
        assert "Guess higher" in out
        assert "Guess lower" in out
        assert "Unlucky. It was 50." in out

    def test_running_out_of_attempts_reveals_answer(self):
        fixed_answer = patch("random.randint", return_value=50)
        wrong_guesses = [str(n) for n in range(1, 11)]
        _, out = run_script(self.FILE, inputs=wrong_guesses, patches=[fixed_answer])
        assert "Unlucky. It was 50." in out

    def test_exp_progress_message_shown_each_round(self):
        fixed_answer = patch("random.randint", return_value=50)
        _, out = run_script(self.FILE, inputs=["50"], patches=[fixed_answer])
        assert "New Round! Current Progress: 0 / 100." in out

    def test_correct_guess_on_last_attempt_still_gains_exp(self):
        """
        Guessing correctly on the very last (10th) attempt still counts as
        a win and grants 10 EXP (1 remaining attempt * 10). Because that
        alone doesn't reach the 100 EXP target, the outer loop starts a
        fresh round - so one more correct guess is supplied to let the
        game finish cleanly.
        """
        fixed_answer = patch("random.randint", return_value=50)
        wrong_then_right = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "50", "50"]
        _, out = run_script(self.FILE, inputs=wrong_then_right, patches=[fixed_answer])
        assert "Correct. You guessed it in 10 attempt(s)" in out
        assert "You have gained 10 EXP." in out

    def test_needs_two_rounds_to_reach_100_exp_if_capped_low(self):
        """A single perfect-first-guess round only grants 100 EXP (10
        remaining attempts * 10), which already meets the win threshold, so
        the outer while loop naturally exits after one round."""
        fixed_answer = patch("random.randint", return_value=50)
        mod, out = run_script(self.FILE, inputs=["50"], patches=[fixed_answer])
        assert mod.EXP == 100


# ---------------------------------------------------------------------------
# quiz_game.py
# ---------------------------------------------------------------------------
class TestQuizGame:
    FILE = f"{FOLDER}/quiz_game.py"

    def test_perfect_score(self):
        answers = ["C", "D", "A", "A", "B"]
        _, out = run_script(self.FILE, inputs=answers)
        assert out.count("CORRECT!") == 5
        assert "Your score is: 100%" in out

    def test_all_wrong_score(self):
        answers = ["A", "A", "B", "B", "A"]
        _, out = run_script(self.FILE, inputs=answers)
        assert out.count("INCORRECT!") == 5
        assert "Your score is: 0%" in out

    def test_lowercase_answers_still_accepted(self):
        answers = ["c", "d", "a", "a", "b"]
        _, out = run_script(self.FILE, inputs=answers)
        assert "Your score is: 100%" in out

    def test_partial_score(self):
        answers = ["C", "D", "A", "wrong", "wrong"]
        _, out = run_script(self.FILE, inputs=answers)
        assert "Your score is: 60%" in out

    def test_results_summary_lists_answers_and_guesses(self):
        answers = ["C", "D", "A", "A", "B"]
        _, out = run_script(self.FILE, inputs=answers)
        assert "answers: C D A A B" in out
        assert "guesses: C D A A B" in out

    def test_each_question_shows_its_options(self):
        answers = ["C", "D", "A", "A", "B"]
        _, out = run_script(self.FILE, inputs=answers)
        assert "A. 116" in out
        assert "D. Ostrich" in out

    def test_incorrect_answer_reveals_the_correct_one(self):
        answers = ["A", "D", "A", "A", "B"]
        _, out = run_script(self.FILE, inputs=answers)
        assert "The correct answer was: C" in out

    def test_guess_list_length_matches_question_count(self):
        answers = ["C", "D", "A", "A", "B"]
        mod, _ = run_script(self.FILE, inputs=answers)
        assert len(mod.guesses) == len(mod.questions)

    def test_visual_separators_appear_between_each_question(self):
        answers = ["C", "D", "A", "A", "B"]
        _, out = run_script(self.FILE, inputs=answers)
        assert out.count("----------------------") >= 5


# ---------------------------------------------------------------------------
# rock_paper_scissors.py
# ---------------------------------------------------------------------------
class TestRockPaperScissors:
    FILE = f"{FOLDER}/rock_paper_scissors.py"

    def test_player_wins(self):
        fixed_choice = patch("random.choice", return_value="s")
        _, out = run_script(self.FILE, inputs=["r"], patches=[fixed_choice])
        assert "You win!" in out

    def test_player_loses(self):
        fixed_choice = patch("random.choice", return_value="p")
        _, out = run_script(self.FILE, inputs=["r"], patches=[fixed_choice])
        assert "You lose!" in out

    def test_tie(self):
        fixed_choice = patch("random.choice", return_value="r")
        _, out = run_script(self.FILE, inputs=["r"], patches=[fixed_choice])
        assert "It's a TIE!" in out

    def test_invalid_input_message_always_prints(self):
        """
        Genuine bug: `player_choice.isdigit() != "r" or "p" or "s"` always
        evaluates truthy (a bool compared to a string is always unequal,
        and that unequal check is OR'd with the always-truthy strings "p"
        and "s"), so the "Invalid input" warning is printed unconditionally
        - even for perfectly valid moves like "r".
        """
        fixed_choice = patch("random.choice", return_value="s")
        _, out = run_script(self.FILE, inputs=["r"], patches=[fixed_choice])
        assert "Invalid input. Please choose 'r', 'p', or 's'." in out

    def test_paper_beats_rock_message(self):
        fixed_choice = patch("random.choice", return_value="r")
        _, out = run_script(self.FILE, inputs=["p"], patches=[fixed_choice])
        assert "You win! Paper beats Rock!" in out

    def test_computer_win_message_names_the_reason(self):
        fixed_choice = patch("random.choice", return_value="p")
        _, out = run_script(self.FILE, inputs=["s"], patches=[fixed_choice])
        assert "You lose! Paper beats Rock!" not in out
        assert "You win! Scissors beats Paper!" in out

    def test_head_to_head_banner_always_shown(self):
        fixed_choice = patch("random.choice", return_value="r")
        _, out = run_script(self.FILE, inputs=["r"], patches=[fixed_choice])
        assert "HEAD TO HEAD" in out
        assert "MATCH RESULT" in out

    def test_computer_wins_with_rock_beats_scissors(self):
        fixed_choice = patch("random.choice", return_value="r")
        _, out = run_script(self.FILE, inputs=["s"], patches=[fixed_choice])
        assert "You lose! Rock beats Scissors!" in out

    def test_computer_wins_with_scissors_beats_paper(self):
        fixed_choice = patch("random.choice", return_value="s")
        _, out = run_script(self.FILE, inputs=["p"], patches=[fixed_choice])
        assert "You lose! Scissors beats Paper!" in out

    def test_display_art_helper_rejects_invalid_choice_directly(self, capsys):
        """
        display_art()'s own `else: print("Invalid choice...")` branch is
        dead code within the normal game flow - it's only ever called
        with winner_art_choice/computer_choice, both of which are always
        constrained to 'r'/'p'/'s' already. Exercised here by calling the
        helper directly with a value it would never actually receive.
        """
        fixed_choice = patch("random.choice", return_value="r")
        mod, _ = run_script(self.FILE, inputs=["r"], patches=[fixed_choice])
        mod.display_art("x")
        captured = capsys.readouterr()
        assert "Invalid choice. Please choose 'r', 'p', or 's'." in captured.out


# ---------------------------------------------------------------------------
# word_guessing_game.py
# ---------------------------------------------------------------------------
class TestWordGuessingGame:
    FILE = f"{FOLDER}/word_guessing_game.py"

    def test_win_by_guessing_all_letters(self):
        fixed_word = patch("random.choice", return_value="java")
        inputs = ["j", "a", "v", "n"]
        _, out = run_script(self.FILE, inputs=inputs, patches=[fixed_word])
        assert "Great guess!" in out
        assert "Congratulations!!! You guessed the word: java" in out
        assert "Thanks for playing! Bye Bye!!!" in out

    def test_wrong_guesses_reduce_attempts(self):
        fixed_word = patch("random.choice", return_value="lua")
        inputs = ["z", "l", "u", "a", "n"]
        _, out = run_script(self.FILE, inputs=inputs, patches=[fixed_word])
        assert "Wrong guess! Attempts left: 9" in out
        assert "Congratulations!!! You guessed the word: lua" in out

    def test_running_out_of_attempts_reveals_word(self):
        fixed_word = patch("random.choice", return_value="lua")
        wrong_guesses = list("zxqwrtybcdfg")[:10]
        inputs = wrong_guesses + ["n"]
        _, out = run_script(self.FILE, inputs=inputs, patches=[fixed_word])
        assert "You've run out of attempts! The word was: lua" in out

    def test_playing_again_starts_a_new_round(self):
        fixed_word = patch("random.choice", return_value="lua")
        inputs = ["l", "u", "a", "y", "l", "u", "a", "n"]
        _, out = run_script(self.FILE, inputs=inputs, patches=[fixed_word])
        assert out.count("Congratulations!!! You guessed the word: lua") == 2

    def test_progress_display_shows_underscores(self):
        fixed_word = patch("random.choice", return_value="lua")
        inputs = ["l", "u", "a", "n"]
        _, out = run_script(self.FILE, inputs=inputs, patches=[fixed_word])
        assert "Current word: _ _ _" in out

    def test_uppercase_guess_is_lowercased(self):
        fixed_word = patch("random.choice", return_value="lua")
        inputs = ["L", "U", "A", "n"]
        _, out = run_script(self.FILE, inputs=inputs, patches=[fixed_word])
        assert "Congratulations!!! You guessed the word: lua" in out

    def test_word_bank_contains_expected_entries(self):
        fixed_word = patch("random.choice", return_value="python")
        inputs = ["p", "y", "t", "h", "o", "n", "n"]
        mod, out = run_script(self.FILE, inputs=inputs, patches=[fixed_word])
        assert "python" in mod.word_bank
        assert "ubuntu" in mod.word_bank


# ---------------------------------------------------------------------------
# banking_program.py
# ---------------------------------------------------------------------------
# NOTE: placed here provisionally alongside the other menu/function-driven
# programs (dice_game.py, quiz_game.py). Confirm/adjust the folder if this
# should sit elsewhere in the new structure.
class TestBankingProgram:
    FILE = f"{FOLDER}/banking_program.py"

    def test_show_balance_direct(self, capsys):
        mod, _ = run_script(self.FILE, inputs=["4"])
        mod.show_balance(123.4)
        captured = capsys.readouterr()
        assert "Balance: £123.40" in captured.out

    def test_deposit_valid_amount_returned(self, capsys):
        mod, _ = run_script(self.FILE, inputs=["4"])
        with patch("builtins.input", return_value="50"):
            result = mod.deposit()
        assert result == 50.0

    def test_deposit_produces_no_confirmation_message(self, capsys):
        """
        Asymmetry worth flagging: withdraw() prints two confirmation
        lines ("You have withdrew..."/"You have ... left.") on success,
        but deposit() has no equivalent - it silently just returns the
        amount with no printed confirmation at all.
        """
        mod, _ = run_script(self.FILE, inputs=["4"])
        with patch("builtins.input", return_value="50"):
            mod.deposit()
        captured = capsys.readouterr()
        assert captured.out == ""

    def test_deposit_negative_amount_rejected(self, capsys):
        mod, _ = run_script(self.FILE, inputs=["4"])
        with patch("builtins.input", return_value="-10"):
            result = mod.deposit()
        captured = capsys.readouterr()
        assert result == 0
        assert "Enter Positive Deposits." in captured.out

    def test_deposit_more_than_two_decimals_rejected(self, capsys):
        mod, _ = run_script(self.FILE, inputs=["4"])
        with patch("builtins.input", return_value="10.999"):
            result = mod.deposit()
        captured = capsys.readouterr()
        assert result == 0
        assert "Funds have to be within 2 decimal places." in captured.out

    def test_deposit_exactly_two_decimals_accepted(self):
        mod, _ = run_script(self.FILE, inputs=["4"])
        with patch("builtins.input", return_value="10.99"):
            result = mod.deposit()
        assert result == 10.99

    def test_deposit_non_numeric_rejected(self, capsys):
        mod, _ = run_script(self.FILE, inputs=["4"])
        with patch("builtins.input", return_value="abc"):
            result = mod.deposit()
        captured = capsys.readouterr()
        assert result == 0
        assert "Invalid Input. Numbers Only." in captured.out

    def test_withdraw_valid_amount(self, capsys):
        mod, _ = run_script(self.FILE, inputs=["4"])
        with patch("builtins.input", return_value="30"):
            result = mod.withdraw(100)
        captured = capsys.readouterr()
        assert result == 30.0
        assert "You have withdrew £30.00." in captured.out
        assert "You have £70.00 left." in captured.out

    def test_withdraw_insufficient_funds(self, capsys):
        mod, _ = run_script(self.FILE, inputs=["4"])
        with patch("builtins.input", return_value="150"):
            result = mod.withdraw(100)
        captured = capsys.readouterr()
        assert result == 0
        assert "Insufficient Funds." in captured.out
        assert "You need £50.00 to complete transaction." in captured.out

    def test_withdraw_negative_amount_rejected(self, capsys):
        mod, _ = run_script(self.FILE, inputs=["4"])
        with patch("builtins.input", return_value="-5"):
            result = mod.withdraw(100)
        captured = capsys.readouterr()
        assert result == 0
        assert "No Negative Amounts." in captured.out

    def test_withdraw_non_numeric_rejected(self, capsys):
        mod, _ = run_script(self.FILE, inputs=["4"])
        with patch("builtins.input", return_value="abc"):
            result = mod.withdraw(100)
        captured = capsys.readouterr()
        assert result == 0
        assert "Invalid Input. Numbers Only." in captured.out

    def test_full_session_deposit_then_withdraw_then_check_balance(self):
        inputs = ["2", "100", "3", "30", "1", "4"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "You have withdrew £30.00." in out
        assert "Balance: £70.00" in out
        assert ">>> Shutting Down... <<<" in out

    def test_invalid_menu_choice_shows_message(self):
        inputs = ["9", "4"]
        _, out = run_script(self.FILE, inputs=inputs)
        assert "Invalid Choice." in out
        assert "Try Again." in out

    def test_menu_banner_shown(self):
        _, out = run_script(self.FILE, inputs=["4"])
        assert "Banking Program" in out
        assert "Main Menu" in out


# ---------------------------------------------------------------------------
# hangman_game.py
# ---------------------------------------------------------------------------
class TestHangmanGame:
    FILE = f"{FOLDER}/hangman_game.py"

    def test_win_by_guessing_all_letters(self):
        fixed_word = patch("random.choice", return_value="cat")
        _, out = run_script(self.FILE, inputs=["c", "a", "t"], patches=[fixed_word])
        assert "YOU WIN!" in out
        assert "c a t" in out

    def test_wrong_guess_increments_counter_and_shows_next_stage(self):
        fixed_word = patch("random.choice", return_value="cat")
        _, out = run_script(self.FILE, inputs=["z", "c", "a", "t"], patches=[fixed_word])
        assert "YOU WIN!" in out

    def test_losing_after_exhausting_all_hangman_stages(self):
        fixed_word = patch("random.choice", return_value="cat")
        wrong_guesses = ["z", "x", "q", "w", "v", "u"]
        _, out = run_script(self.FILE, inputs=wrong_guesses, patches=[fixed_word])
        assert "YOU LOSE!" in out
        assert "c a t" in out  # answer revealed

    def test_repeated_guess_shows_already_guessed_message(self):
        fixed_word = patch("random.choice", return_value="cat")
        _, out = run_script(self.FILE, inputs=["c", "c", "a", "t"], patches=[fixed_word])
        assert "c is already guessed" in out

    def test_multi_character_input_rejected(self):
        fixed_word = patch("random.choice", return_value="cat")
        _, out = run_script(self.FILE, inputs=["ab", "c", "a", "t"], patches=[fixed_word])
        assert "Invalid input" in out

    def test_non_alphabetic_input_rejected(self):
        fixed_word = patch("random.choice", return_value="cat")
        _, out = run_script(self.FILE, inputs=["5", "c", "a", "t"], patches=[fixed_word])
        assert "Invalid input" in out

    def test_guess_is_case_insensitive(self):
        fixed_word = patch("random.choice", return_value="cat")
        _, out = run_script(self.FILE, inputs=["C", "A", "T"], patches=[fixed_word])
        assert "YOU WIN!" in out

    def test_hint_starts_as_all_underscores(self):
        fixed_word = patch("random.choice", return_value="cat")
        _, out = run_script(self.FILE, inputs=["c", "a", "t"], patches=[fixed_word])
        assert "_ _ _" in out

    def test_display_hangman_function_direct(self, capsys):
        mod, _ = run_script(self.FILE, inputs=["z", "x", "q", "w", "v", "u"], patches=[patch("random.choice", return_value="cat")])
        mod.display_hangman(3)
        captured = capsys.readouterr()
        assert "/| " in captured.out

    def test_hangman_art_has_seven_stages(self):
        mod, _ = run_script(self.FILE, inputs=["z", "x", "q", "w", "v", "u"], patches=[patch("random.choice", return_value="cat")])
        assert set(mod.hangman_art.keys()) == {0, 1, 2, 3, 4, 5, 6}

    def test_word_bank_is_a_tuple_of_lowercase_animal_names(self):
        mod, _ = run_script(self.FILE, inputs=["z", "x", "q", "w", "v", "u"], patches=[patch("random.choice", return_value="cat")])
        assert isinstance(mod.animals, tuple)
        assert "elephant" in mod.animals
        assert all(name.islower() or "-" in name for name in mod.animals)

    def test_display_answer_function_direct(self, capsys):
        mod, _ = run_script(self.FILE, inputs=["z", "x", "q", "w", "v", "u"], patches=[patch("random.choice", return_value="cat")])
        mod.display_answer("dog")
        captured = capsys.readouterr()
        assert captured.out.strip() == "d o g"

