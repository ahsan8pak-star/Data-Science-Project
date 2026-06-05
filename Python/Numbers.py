import math # Investigate more at https://docs.python.org/3/library/math.html


a = 1 # Integer
b = 1.1 # Float
c = 1 + 2j # Complex number - 1 + 2i, where i is the imaginary unit 
d = 1e-3 # Scientific notation for 0.001
e = 0b1010 # Binary representation for 10
f = 0o12 # Octal representation for 10
g = 0xA # Hexadecimal representation for 10
h = 1_000_000 # Underscores for readability, equivalent to 1000000
i = 0.000_001 # Underscores in float, equivalent to 0.000001

print(type(a)) # Integer

print(a)

print(type(b)) # Float

print(b)

print(type(c)) # Complex

print(c)

print(type(d)) # Float

print(d)

print(type(e)) # Float

print(e)

print(type(f)) # Float

print(f)

print(type(g)) # Float

print(g)

print(type(h)) # Float

print(h)

print(type(i)) # Float

print(i)

# Reason for these outputs:
# type() can only determine float, int, and complex types of numbers
# Meaning all these numbers are either int or float based on their value, not their representation.


# Basic arithmetic operations with numbers

x = 10
y = 3

print(x + y) # Addition

print(x - y) # Subtraction

print(x * y) # Multiplication

print(x / y) # Division (returns a float)

print(x // y) # Floor division (returns an integer as the quotient/base)

print(x % y) # Modulus (returns the remainder)

print(x ** y) # Exponentiation (x raised to the power of y)

print(-x) # Negation (returns the negative of x)

print(+x) # Unary plus (returns x unchanged)

print(abs(-x)) # Absolute value (returns the non-negative value of x)

print(pow(x, y)) # Power function (equivalent to x ** y)

print(divmod(x, y)) # Returns a tuple of (x // y, x % y)

print(round(3.14159, 2)) # Rounds the number to 2 decimal places

print(int(3.7)) # Converts a float to an integer (truncates the decimal part)

print(float(10)) # Converts an integer to a float

print(complex(1, 2)) # Creates a complex number with real part 1 and imaginary part 2

print(round(2.71828)) # Rounds the number to the nearest integer


# Using the math module for more advanced mathematical operations


print(math.sqrt(16)) # Square root of 16

print(math.sin(math.pi / 2)) # Sine of 90 degrees (pi/2 radians)

print(math.cos(0))  # Cosine of 0 degrees (0 radians)

print(math.tan(math.pi / 4)) # Tangent of 45 degrees (pi/4 radians)

print(math.log(1)) # Natural logarithm of 1 (returns 0)

print(math.exp(1)) # Exponential function of 1 (returns e)

print(math.factorial(5)) # Factorial of 5 (returns 120)

print(math.gcd(48, 18)) # Greatest common divisor of 48 and 18 (returns 6)

print(math.lcm(12, 15)) # Least common multiple of 12 and 15 (returns 60)

print(math.pi) # Value of pi (approximately 3.14159)

print(math.e) # Value of e (approximately 2.71828)

print(math.inf) # Represents positive infinity

print(math.nan) # Represents "Not a Number" (NaN)

print(math.isfinite(1)) # Checks if the number is finite (returns True)

print(math.isinf(math.inf)) # Checks if the number is infinite (returns True)

print(math.isnan(math.nan)) # Checks if the number is NaN (returns True)

print(math.ceil(2.3)) # Rounds a number up to the nearest integer (returns 3)

print(math.floor(2.7)) # Rounds a number down to the nearest integer (returns 2)

print(math.trunc(2.9)) # Truncates the decimal part and returns the integer part (returns 2)

print(math.copysign(1, -1)) # Returns a float with the magnitude of the first argument and the sign of the second argument (returns -1.0)

print(math.fabs(-5)) # Absolute value of a float (returns 5.0)

print(math.frexp(8)) # Returns the mantissa and exponent of a number (returns (0.5, 4))

print(math.ldexp(0.5, 4)) # Returns the result of multiplying the mantissa by 2 raised to the power of the exponent (returns 8.0)

print(math.modf(3.14)) # Returns the fractional and integer parts of a number (returns (0.14000000000000012, 3.0))

print(math.remainder(10, 3)) # Returns the remainder of the division of x by y (returns 1.0)

print(math.sin(math.radians(30))) # Sine of 30 degrees (converts degrees to radians first, returns 0.5)

print(math.cos(math.radians(60))) # Cosine of 60 degrees (converts degrees to radians first, returns 0.5)

print(math.tan(math.radians(45))) # Tangent of 45 degrees (converts degrees to radians first, returns 1.0)

print(math.hypot(3, 4)) # Returns the Euclidean norm, sqrt(x*x + y*y) (returns 5.0)

print(math.degrees(math.pi)) # Converts radians to degrees (returns 180.0)

print(math.radians(180)) # Converts degrees to radians (returns 3.14159)

print(math.gamma(5)) # Gamma function of 5 (returns 24.0, which is equivalent to factorial(4))

print(math.lgamma(5)) # Logarithm of the absolute value of the gamma function of 5 (returns approximately 3.17805)

print(math.isclose(0.1 + 0.2, 0.3)) # Checks if two values are close to each other (returns True)

print(math.nextafter(1.0, 2.0)) # Returns the next floating-point value after x towards y (returns 1.0000000000000002)


# Comparison operators for numbers

print(x == y) # Equality (returns False)
print(x != y) # Inequality (returns True)
print(x > y) # Greater than (returns True)
print(x < y) # Less than (returns False)
print(x >= y) # Greater than or equal to (returns True)
print(x <= y) # Less than or equal to (returns False)

# Logical operators for numbers (using the results of comparison operators)
print(x > 5 and y < 5) # Logical AND (returns True)
print(x > 5 or y < 5) # Logical OR (returns True)
print(not (x > 5)) # Logical NOT (returns False)