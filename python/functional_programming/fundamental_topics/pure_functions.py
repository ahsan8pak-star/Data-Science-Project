# Pure function = Always returns the same output for the same input,
# and never changes anything outside itself (no side effects).


# Pure: same inputs always produce the same result
def add_tax(price, rate):
    return price + (price * rate)


print("add_tax(10, 0.2):", add_tax(10, 0.2))
print("add_tax(10, 0.2):", add_tax(10, 0.2))  # same input -> same output

# Pure: arithmetic only on its own arguments
def total_cost(prices):
    return sum(prices)


print("total_cost([5, 10, 15]):", total_cost([5, 10, 15]))

# Impure: depends on a value outside the function
calls = 0

def next_number():
    global calls
    calls += 1
    return calls


print("next_number():", next_number())
print("next_number():", next_number())  # same "no input" but different output