try:
    from python.imperative_programming.maths_science_projects.arithmetic_calculator import arithmetic

except ImportError:
    from arithmetic_calculator import arithmetic


def get_number(prompt):
    user_input = input(prompt).strip()

    try:
        return int(user_input)  # keeps "8" as a clean int, not 8.0

    except ValueError:
        return float(user_input)  # falls back to float for "8.5" etc.


def format_result(op, result):
    if op == "/":
        return f"{result:.2f}"  # division always shows 2 decimal places

    if isinstance(result, float) and result.is_integer():
        return str(int(result))  # e.g. 14.0 -> "14", not "14.0"

    if isinstance(result, float):
        return f"{result:.2f}"

    return str(result)


def calculate():
    try:
        print("\n========================")
        print(" ARITHMETIC EXPERSSIONS ")        
        print("========================\n")
        print("<================>")
        print("<  MENU   GUIDE  >")
        print("<================>\n")
        print("  _______________________________________________________ ")
        print(" /                                                       \\ ")
        print(" | 1) + = Addition         5) // = Base / Quotient       | ")
        print(" | 2) - = Subtraction      6) % = Remainder / Modulus    | ") 
        print(" | 3) * = Multiplication   7) ** = Power / Exponent      | ")
        print(" | 4) / = Division         8) <ENTER> = Continue         | ")
        print(" \\                                                      / ")
        print("  ``````````````````````````````````````````````````````` \n")

        num1 = get_number("Enter first number: ")
        num2 = get_number("\nEnter second number: ")

        operators = ["+", "-", "*", "/", "%", "//", "**"]

        print("\n===========")
        print("  RESULTS  ") 
        print("===========\n")

        for op in operators:
            result = arithmetic(num1, op, num2)
            print(f"{num1} {op} {num2} = {format_result(op, result)}")

    except ValueError:
        print("Invalid input. Please enter numeric values only.")


if __name__ == "__main__":
    calculate()

