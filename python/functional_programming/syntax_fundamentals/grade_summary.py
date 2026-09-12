# Grade Summary -> applies filter(), reduce() and any()/all() to student results


from functools import reduce


def pass_grade(score):
    return score >= 40


def average(scores):
    return reduce(lambda a, b: a + b, scores) / len(scores)


def main():
    scores = [45, 62, 78, 91, 33, 58]

    passed = list(filter(pass_grade, scores))
    failed = list(filter(lambda s: not pass_grade(s), scores))

    print("Scores:", scores)
    print("Passed:", passed)
    print("Failed:", failed)
    print("Average:", round(average(scores), 2))
    print("Everyone passed?", all(pass_grade(s) for s in scores))


if __name__ == "__main__":
    main()