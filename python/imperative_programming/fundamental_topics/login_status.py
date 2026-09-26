"""
Login status - a nested questionnaire branching on five yes/no answers.

Asks whether the user is a student, an admin, new, a regular student and
online, then decides what to print. Two deliberate defects are preserved and
pinned by tests: the predicates on lines 16 and 19 use truthiness where a
comparison to "T" is needed, so "Stop Lying" is unreachable and the elif
ignores is_new. The IndexError handling is a genuine repair - an empty answer
raised an uncaught IndexError that except ValueError could not catch.
"""

def get_boolean_answer(prompt):
    return input(prompt).strip()


def display_answers(is_student, is_admin, is_new, is_regular, is_online):
    print(f"Student: {is_student}")
    print(f"Admin: {is_admin}")
    print(f"Starting: {is_new}")
    print(f"Currently Studying: {is_regular}")
    print(f"Online: {is_online}")


def check_access_status(is_student, is_admin, is_new, is_regular, is_online):
    if is_online[0].upper() == "T":
        # Bug preserved: missing () on first operand, missing == "T" on first operand
        if is_student[0].upper and is_admin[0].upper == "T":
            print("Stop Lying, or you will be kicked out.")

        # Bug preserved: missing == "T" on first operand (is_new[0].upper() returns "T"/"F" - both truthy)
        elif is_new[0].upper() and is_regular[0].upper() == "T":
            choice = get_boolean_answer("Accident or Intented? (A/I) ")

            if choice[0].upper() == "A":
                print("No problem. Try Again.")

            elif choice[0].upper() == "I":
                print("Leave or we will suspend you permanently!")

            else:
                print("Stop Messing Around! What is your answer?")

        else:
            print("Welcome to our university!")

    else:
        print(f"{is_online}. You are offline. You are unable to access this.")


def run_login_check():
    try:
        is_student = get_boolean_answer("Are you a student? (True / False): ")
        is_admin = get_boolean_answer("Are you an admin? (True / False): ")
        is_new = get_boolean_answer("Are you starting university? (True / False): ")
        is_regular = get_boolean_answer("Are you a current university student? (True / False): ")
        is_online = get_boolean_answer("Are you in your university account? (True or False): ")

        display_answers(is_student, is_admin, is_new, is_regular, is_online)
        check_access_status(is_student, is_admin, is_new, is_regular, is_online)
    except (ValueError, IndexError):
        print("Please type within boolean logic. True or False.")


if __name__ == "__main__":
    run_login_check()