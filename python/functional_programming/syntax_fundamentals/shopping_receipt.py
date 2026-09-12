# Shopping Receipt -> applies map(), filter() and reduce() to a small shopping basket


from functools import reduce


def format_item(item):
    name, price, quantity = item
    line_total = price * quantity
    return f"{name}: ${line_total:.2f}"


def total_price(basket):
    return reduce(lambda total, item: total + item[1] * item[2], basket, 0)


def main():
    basket = [
        ("Apple", 0.50, 4),
        ("Bread", 1.20, 2),
        ("Milk", 1.05, 1),
    ]

    lines = map(format_item, basket)
    total = total_price(basket)

    print("-- Shopping Receipt --")
    for line in lines:
        print(line)
    print("-" * 20)
    print(f"Total: ${total:.2f}")


if __name__ == "__main__":
    main()