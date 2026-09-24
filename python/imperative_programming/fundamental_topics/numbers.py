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


# Integer bit methods

bit_num = 196

print(bit_num.bit_count()) # Counts the number of 1-bits in the binary representation of the integer (returns 3 as 196 = 0b11000100)

print(bit_num.bit_length()) # Returns the number of bits needed to represent the integer in binary, excluding the sign and leading zeros (returns 8)

big_endian = bit_num.to_bytes(2, byteorder="big") # Converts the integer to a fixed number of bytes using big-endian byte order (returns b'\x00\xc4')

print(big_endian)

round_trip = int.from_bytes(big_endian, byteorder="big") # Converts bytes back to an integer using big-endian byte order (returns 196)

print(round_trip)

from_bytes_literal = int.from_bytes(b"\xff", byteorder="big") # Bytes from a literal can also be converted back to an integer (returns 255)

print(from_bytes_literal)

need_two_bytes = (256).to_bytes(2, "big") # Values above 255 need more than one byte (returns b'\x01\x00')

print(need_two_bytes)


# Decimal for exact decimal arithmetic

from decimal import Decimal, getcontext, localcontext

exact_sum = Decimal("0.1") + Decimal("0.2") # Exact decimal addition (returns 0.3, unlike 0.1 + 0.2 which gives 0.30000000000000004)

print(exact_sum)

exact_division = Decimal(10) / Decimal(3) # Exact division to the current context precision (returns 3.333333333333333333333333333)

print(exact_division)

print(getcontext().prec) # Shows the current precision for the thread's context (returns 28)

getcontext().prec = 6 # Changes the precision for the current context

print(Decimal(1) / Decimal(7)) # With precision set to 6 this returns 0.142857

getcontext().prec = 28 # Restores the default precision

scale_compare = Decimal("1.1") == Decimal("1.10") # Decimal values are equal even when their scale differs (returns True)

print(scale_compare)

with localcontext() as ctx: # Temporarily changes the context for this block only
    ctx.prec = 4 # Sets the precision to 4 within the block
    print(Decimal(1) / Decimal(3)) # Returns 0.3333 inside the block

print(Decimal(1) / Decimal(3)) # Outside the block the precision is back to 28 (returns 0.3333333333333333333333333333)


# More math module functions

print(math.fmod(13, 6)) # Modulo following C's fmod semantics (returns 1.0)

accurate_sum = math.fsum([0.1, 0.1, 0.1]) # Accurate floating-point sum (returns 0.3 rather than 0.30000000000000004)

print(accurate_sum)

print(math.pow(2, 10)) # Raises 2 to the power 10, always returning a float (returns 1024.0)

print(math.prod([1, 2, 3, 4])) # Multiplies all values in an iterable together (returns 24)

print(math.prod(range(1, 6))) # prod accepts any iterable including a range (returns 120)

print(math.comb(5, 2)) # Number of ways to choose 2 items from 5 without order (returns 10)

print(math.perm(5, 2)) # Number of ways to arrange 2 items chosen from 5 (returns 20)

print(math.perm(7, 7)) # Arranging all 7 items in order (returns 5040)# Integer bit methods

num = 204

print(num.bit_count()) # Counts the number of 1-bits in the binary representation of the integer (returns 3 as 204 = 0b11001100)

print(num.bit_length()) # Returns the number of bits needed to represent the integer in binary, excluding the sign and leading zeros (returns 8)

big_int = 1024

print(big_int.to_bytes(2, byteorder="big")) # Converts the integer to a fixed number of bytes using big-endian byte order (returns b'\x04\x00')

print(int.from_bytes(b"\x04\x00", byteorder="big")) # Converts bytes back to an integer using big-endian byte order (returns 1024)

print((255).to_bytes(1, byteorder="big")) # A single byte can hold values from 0 to 255 (returns b'\xff')

print(int.from_bytes(b"\xff", byteorder="big")) # Converts a single byte back to an integer (returns 255)

print((1).to_bytes(1, byteorder="big")) # Minimal 1 byte for small values (returns b'\x01')


# Decimal module for exact decimal arithmetic

from decimal import Decimal, getcontext, localcontext

print(Decimal("0.1") + Decimal("0.2")) # Exact decimal addition showing 0.3 (avoids the 0.1 + 0.2 == 0.30000000000000004 float quirk)

print(Decimal("1.5") * Decimal("2.2")) # Exact decimal multiplication showing 3.30

print(Decimal(10) / Decimal(3)) # Exact decimal division to 28 significant digits by default

getcontext().prec = 6 # Sets the current thread's precision context to 6 significant digits

print(Decimal(1) / Decimal(3)) # Shows 0.333333 with precision 6

getcontext().prec = 28 # Restores the default precision context of 28 significant digits

with localcontext() as ctx: # Temporarily changes the precision for the duration of this block only
    ctx.prec = 4 # Sets the local precision context to 4 significant digits
    print(Decimal(2) / Decimal(3)) # Shows 0.6667 within the block

print(Decimal(2) / Decimal(3)) # Outside the block the default context (28 digits) returns 0.6666666666666666666666666667


# More math module functions

print(math.fmod(13, 4)) # Floating-point remainder of 13/4 retaining the sign of the dividend (returns 1.0)

print(math.fsum([0.1, 0.1, 0.1])) # Accurate floating-point sum avoiding rounding drift (returns 0.3)

print(math.pow(2, 10)) # Raises 2 to the power 10 always returning a float (returns 1024.0)

print(math.prod([1, 2, 3, 4])) # Multiplies all elements of an iterable together (returns 24)

print(math.comb(5, 2)) # Number of ways to choose 2 items from 5 without regard to order (returns 10)

print(math.perm(5, 2)) # Number of ways to arrange 2 items selected from 5 (returns 20)

print(math.prod(range(1, 6))) # prod works on iterables (returns 120)


# Bytes and hex - the binary twins of text

sample_text = "Ahsan" # A string ready to be stored or transmitted as raw bytes

as_bytes = sample_text.encode("utf-8") # Encodes the text into its UTF-8 bytes (returns b'Ahsan')

print(as_bytes)

back_to_text = as_bytes.decode("utf-8") # Decodes the same bytes back into the original string (returns Ahsan)

print(back_to_text)

hex_view = as_bytes.hex() # Renders each byte as two lowercase hex digits (returns 416873616e)

print(hex_view)

rebuilt_bytes = bytes.fromhex(hex_view) # Parses the hex string back into the original bytes (returns b'Ahsan')

print(rebuilt_bytes)

capital_hex = as_bytes.hex().upper() # A common display form showing all hex digits in capitals (returns 416873616E)

print(capital_hex)


# End of numbers.py - basic number handling, arithmetic, math module, integer bit methods, Decimal for exact calculations and bytes/hex conversion


