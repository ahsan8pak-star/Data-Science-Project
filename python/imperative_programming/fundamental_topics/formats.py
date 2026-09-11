# Format Specifiers
# {Value : flags}
# formats values based on the type of flags

price = 1234.56

print(f"Price 1: {price:.3f}") # Converts 3 decimal places 

# Output: 1234.560

print(f"Price 2: {price:.2g}") # Converts to 2 significant figures in scientific notation form 

# Output: 1.2e+03

print(f"Price 3: {price:.4}") # Converts to 4 significant figures in scientific notation form (round up the last digit)

# Expected Output: 1235
# Actual Output: 1.235e+03  
# Reason: Due to its large price value, it's under scientific notation.

print(f"Price 4: {price:010}") # Pads with zeros (0s) to width 10 (up to 10 value places) 

# Output: 0001234.56

print(f"Price 5: {price:010.3f}") # Pads with zeros (0s) to width 10 (up to 10 characters)
# 1 zero (0) is "removed" from the left due to 3 decimal places being converted within the 10 characters limit.

# Output: 001234.560 

print(f"Price 6: {price:.<10}") # Left justify, pad with dots (.) to width 10 (up to 10 characters) 

# Output: 1234.56...

print(f"Price 7: {price:.>10}") # Right justify, pad with dots (.) to width 10 (up to 10 characters) 

# Output: ...1234.56

print(f"Price 8: {price:.^10}") # Centre justify, pad with dots (.) to width 10 (up to 10 value places) 

# Output: .1234.56..

print(f"Price 9: {price:+.3f}") # Forces a sign (+/-) with 3 decimal places 

# Output: +1234.560

print(f"Price 10: {price:.=+10.2f}") # '=' places sign far left, pads dots to width 10, 2 decimals 

# Output: +..1234.56

print(f"Price 11: {price:}") # Default formatting (raw value output) 

# Output: 1234.56

print(f"Price 12: {price: }") # Includes a whitespace (an extra empty space)
# Output:  1234.56

print(f"Price 13: {price:,}") # Comma (,) separator for at least the thousands place (1000s) 

# Output: 1,234.56

