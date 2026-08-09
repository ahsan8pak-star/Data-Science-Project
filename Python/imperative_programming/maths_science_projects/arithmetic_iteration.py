from arithmetic_calculator import arithmetic

def generate_sequence(iterations, terms):
    # Generates a polynomial sequence based on user-provided coefficients.
    sequence = []
    coefficients = []
    degree = terms - 1
    
    print("\n<------------------------>")
    print("< SEQUENCE COEFFICIENTS  >")
    print("<------------------------>")

    # Get coefficients for the polynomial terms
    for n in range(terms):
        power = degree - n

        if power > 1:
            coefficient = float(input(f"Enter the coefficient for n^{power}: ").strip())

        elif power == 1:
            coefficient = float(input("Enter the coefficient for n: ").strip())

        else:
            coefficient = float(input("Enter the constant number: ").strip())

        coefficients.append(coefficient)
        
    # Calculate sequence values for n = 1 to iterations
    for n in range(1, iterations + 1):
        term_value = 0

        for i, coefficient in enumerate(coefficients):
            power = degree - i
            term_value += coefficient * (n ** power)

        sequence.append(term_value)
        
    return sequence

def arithmetic_iteration(first_num, op, sequence):
    # Applies the operation across the first number and the generated sequence.
    current_result = first_num
    step_results = []
    
    for value in sequence:
        current_result = arithmetic(current_result, op, value)
        step_results.append(current_result)
        
        # Stop iterating if a division by zero error string is returned
        if isinstance(current_result, str) and "Error" in current_result:
            break
            
    return current_result, step_results

if __name__ == "__main__":
    try:
        print("=======================")
        print(" ARITHMETIC ITERATION ")        
        print("=======================\n")
        print("<================>")
        print("<   MENU  GUIDE  >")
        print("<================>\n")
        print("  _______________________________________________________ ")
        print(" /                                                       \\ ")
        print(" | 1) + = addition        5) // = base / quotient        | ")
        print(" | 2) - = subtraction      6) % = remainder / modulus    | ") 
        print(" | 3) * = multiplication   7) ** = power / exponent      | ")
        print(" | 4) / = division         8) <ENTER> = Calculate result | ")
        print(" \\                                                       / ")
        print(" `````````````````````````````````````````````````````````")

        operation = input("Enter the operator: ").strip()
        iterations = input("Enter the number of iterations: ").strip()
        first_num = input("Enter the 1st number of the sequence: ").strip()
        num_terms = input("Enter the number of terms for the sequence: ").strip()
        
        if not first_num or not operation or not iterations or not num_terms:
            print("Missing input.\n<<< Exiting. >>>")
            exit()
            
        iterations = int(iterations)
        first_num = float(first_num)
        num_terms = int(num_terms)

        if iterations <= 0 or num_terms <= 0:
            print("Iterations and terms must be positive integers.")
            exit()
            
        sequence = generate_sequence(iterations, num_terms)
        print(f"\nCoefficient Sequence ('n' terms) of {iterations} iterations: {sequence}")
        
        final_result, all_steps = arithmetic_iteration(first_num, operation, sequence)
        print(f"\nMain Number Sequence List (with starting number: {first_num}): {all_steps}")

        result = f"Final Result: {final_result}"
        width = len(result) + 4  # Set standard terminal menu width
        border = "=" * width

        print(f"\n{border}")
        print(f"| {result:<{width - 4}} |") # due to the border and spaces i.e. "| " and " |"
        print(f"{border}")

    except ValueError:
        print("\nInvalid input. Please enter numeric values where required.")

