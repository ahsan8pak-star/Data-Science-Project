questions = ("How many elements are in the periodic table?: ",
             "Which animal lays the largest eggs?: ",
             "What is the most abundant gas in Earth's atmosphere?: ",
             "How many bones are in the human body?: ",
             "Which planet in the solar system is the hottest?: ")

options = (("A. 116", "B. 117", "C. 118", "D. 119"),
           ("A. Whale", "B. Crocodile", "C. Elephant", "D. Ostrich"),
           ("A. Nitrogen", "B. Oxygen", "C. Carbon-Dioxide", "D. Hydrogen"),
           ("A. 206", "B. 207", "C. 208", "D. 209"),
           ("A. Mercury", "B. Venus", "C. Earth", "D. Mars"))

answers = ("C", "D", "A", "A", "B") # Correct options

# starting point
guesses = [] 
score = 0
question_num = 0

for question in questions:
    print("----------------------") # Provides a visual separation between questions
    print(question)
    for option in options[question_num]: # Print each option for each question asked chronologically
        print(option)

    guess = input("Enter (A, B, C, D): ").upper()
    guesses.append(guess)
    if guess == answers[question_num]: # If their guess is the correct answer
        score += 1
        print("CORRECT!")
    else:
        print("INCORRECT!")
        print(f"The correct answer was: {answers[question_num]}")
    question_num += 1

print("----------------------")
print("       RESULTS        ")
print("----------------------")

print("answers: ", end="") # already a space after the colon so ( end=" " ) is not needed.
for answer in answers:
    print(answer, end=" ") # separates the answers with an empty space (whitespace)
print()

print("guesses: ", end="")
for guess in guesses:
    print(guess, end=" ")
print()

score = int(score / len(questions) * 100) # provides the percentage score
print(f"Your score is: {score}%") 

