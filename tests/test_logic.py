"""
Tests for every script under Python/Logic&AlgorithmicGames/.

These are small interactive terminal games. Where a script relies on
`random`, we patch it via run_script(..., patches=[...]) so the games become
fully deterministic and finish in one pass instead of looping forever.
"""

from unittest.mock import patch

import pytest

from tests.conftest import run_script

FOLDER = "logical_games"


# ---------------------------------------------------------------------------
# grade_boundary_calculator.py
# ---------------------------------------------------------------------------
class TestGradeBoundaryCalculator:
    FILE = f"{FOLDER}/grade_boundary_calculator.py"

    @pytest.mark.parametrize(
        "score, expected_phrase",
        [
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
            ("5", "SERIOUSLY?! THAT LOW?!!"),
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
        # No try/except in this script, so int(grade) on bad input propagates.
        with pytest.raises(ValueError):
            run_script(self.FILE, inputs=["not-a-number"])


# ---------------------------------------------------------------------------
# haiku_madlibs.py
# ---------------------------------------------------------------------------
class TestHaikuMadlibs:
    FILE = f"{FOLDER}/haiku_madlibs.py"

    def test_all_three_verses_built_from_input(self):
        # random.choice always picks the *first* template of whichever list
        # it's given, making the whole script deterministic.
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
        # first verse-1 template capitalises only the determiner (d1) and
        # pronoun (p1), not the adjective
        assert "The silent pine," in out


# ---------------------------------------------------------------------------
# login_status.py
# ---------------------------------------------------------------------------
class TestLoginStatus:
    FILE = f"{FOLDER}/login_status.py"

    def test_echoes_back_all_five_answers(self):
        # is_regular="False" avoids the (buggy) elif branch below, which
        # would otherwise demand a 6th "choice" answer - see
        # test_regular_student_online_accident_choice for that path.
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

    def test_empty_online_answer_raises_uncaught_index_error(self):
        # is_online[0] on an empty string raises IndexError, which this
        # script's `except ValueError:` does not catch.
        inputs = ["True", "False", "False", "True", ""]
        with pytest.raises(IndexError):
            run_script(self.FILE, inputs=inputs)


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
        # Any guess that isn't correct costs an attempt, so a single round
        # can only ever afford exactly 10 wrong guesses before "Unlucky"
        # ends the game - use all 10 (alternating low/high) purely to
        # observe both hint messages without needing a second round.
        fixed_answer = patch("random.randint", return_value=50)
        wrong_guesses = ["10", "90", "20", "80", "30", "70", "40", "60", "15", "85"]
        _, out = run_script(self.FILE, inputs=wrong_guesses, patches=[fixed_answer])
        assert "Guess higher" in out
        assert "Guess lower" in out
        assert "Unlucky. It was 50." in out

    def test_running_out_of_attempts_reveals_answer(self):
        fixed_answer = patch("random.randint", return_value=50)
        wrong_guesses = [str(n) for n in range(1, 11)]  # 10 wrong attempts
        _, out = run_script(self.FILE, inputs=wrong_guesses, patches=[fixed_answer])
        assert "Unlucky. It was 50." in out


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
        answers = ["A", "A", "B", "B", "A"]  # deliberately all incorrect
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


# ---------------------------------------------------------------------------
# word_guessing_game.py
# ---------------------------------------------------------------------------
class TestWordGuessingGame:
    FILE = f"{FOLDER}/word_guessing_game.py"

    def test_win_by_guessing_all_letters(self):
        fixed_word = patch("random.choice", return_value="java")
        inputs = ["j", "a", "v", "n"]  # letters, then decline to replay
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
        wrong_guesses = list("zxqwrtybcdfg")[:10]  # 10 letters not in "lua"
        inputs = wrong_guesses + ["n"]
        _, out = run_script(self.FILE, inputs=inputs, patches=[fixed_word])
        assert "You've run out of attempts! The word was: lua" in out

    def test_playing_again_starts_a_new_round(self):
        fixed_word = patch("random.choice", return_value="lua")
        inputs = ["l", "u", "a", "y", "l", "u", "a", "n"]
        _, out = run_script(self.FILE, inputs=inputs, patches=[fixed_word])
        assert out.count("Congratulations!!! You guessed the word: lua") == 2

