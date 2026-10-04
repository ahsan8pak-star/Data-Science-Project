score = 85
grade = "B"

# Conditional logic using if, elif, and else with relational and logical operators
if score >= 90 and score <= 100:
    print("Grade: A")

elif score >= 80 or score == 85:
    print("Grade: B")

else:
    print("Grade: C or lower")

# Selection using match-case statements (Python 3.10+)
match grade:

    case "A":
        print("Status: Excellent")

    case "B":
        print("Status: Good")

    case _:  # Default fallback case
        print("Status: Passing or Needs Improvement")

