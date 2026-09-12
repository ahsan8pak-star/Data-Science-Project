# Word Frequency -> applies sorted() with a key and a lambda to tally repeated words


def main():
    words = ["python", "java", "python", "kotlin", "java", "python", "go"]

    unique_words = {w for w in words}
    counts = [(word, words.count(word)) for word in unique_words]
    ranked = sorted(counts, key=lambda pair: (-pair[1], pair[0]))

    print("Words:", words)
    for word, count in ranked:
        print(f"{word}: {count}")


if __name__ == "__main__":
    main()