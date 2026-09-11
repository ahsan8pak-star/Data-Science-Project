# Lambda function = A small anonymous function for a one time use ('throw away' function)
# They take any number of arguments, but have only 1 expression
# Helps keep the namespace clean and is useful with higher-order functions
# -> 'sort()', 'map()', 'filter()', 'reduce()' 
# -> example methods of functional programming
# lambda parameters: expression

double = lambda x: x * 2
halved = lambda x: x / 2 
add = lambda x, y: x + y
subtract = lambda x, y: x - y
multiply = lambda x, y: x * y
divide = lambda x, y: x / y
base = lambda x, y: x // y
remainder = lambda x, y: x % y
max_value = lambda x, y: x if x > y else y
min_value = lambda x, y: x if x < y else y
full_name = lambda first, last: first + " " + last
is_even = lambda x: x % 2 == 0
is_odd = lambda x: x % 2 == 1
age_check = lambda age: True if age >= 18 else False

print(double(2))
print(halved(4))
print(add(3, 4))
print(subtract(5, 2))
print(multiply(6, 7))
print(divide(24, 8))
print(base(7, 3))
print(remainder(8, 5))
print(max_value(6, 7))
print(min_value(9, 8))
print(full_name("Ahsan", "Iqbal"))
print(is_even(5))
print(is_odd(6))
print(age_check(21))
print(age_check(18))
print(age_check(16))

