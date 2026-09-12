# Number Pipeline -> a basic filter -> map -> reduce data flow


from functools import reduce


def main():
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    evens = list(filter(lambda n: n % 2 == 0, numbers))
    squares = list(map(lambda n: n ** 2, evens))
    total = reduce(lambda a, b: a + b, squares)

    print("Numbers:", numbers)
    print("Evens:", evens)
    print("Squares of evens:", squares)
    print("Sum of squares:", total)


if __name__ == "__main__":
    main()