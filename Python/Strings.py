Name = " AhSaN "

print(Name.lower()) # all letters in lower case 
# Expected Output: " ahsan "
# Actual Output:   " ahsan "

print(Name.upper()) # all letters in upper case 
# Expected Output: " AHSAN "
# Actual Output:   " AHSAN "

print(Name.title()) # first letter of each word in upper case, rest lower case
# Expected Output: " Ahsan "
# Actual Output:   " Ahsan "
# Reason: The leading space is ignored as whitespace, making "AhSaN" the first word. Its first letter "A" stays capitalized, but `.title()` forces all subsequent letters ("hSaN") into lowercase, resulting in "hsan".

print(Name.capitalize()) # capitalizes ONLY the very first character of the string, lowers the rest
# Expected Output: " ahsan "
# Actual Output:   " ahsan "
# Reason: The very first character is a space, which cannot be capitalized. Python then converts every single remaining character in the string to lowercase.

print(Name.swapcase()) # swaps the case of each letter 
# Expected Output: " aHsAn "
# Actual Output:   " aHsAn "
# Reason: The uppercase letters "A" and "S" become lowercase, and lowercase "h" and "n" become uppercase.

print(Name.strip()) # removes whitespace from both ends 
# Expected Output: "AhSaN"
# Actual Output:   "AhSaN"
# Reason: The leading and trailing spaces are entirely stripped away.

print(Name.lstrip()) # removes whitespace from the left end 
# Expected Output: "AhSaN "
# Actual Output:   "AhSaN "
# Reason: Only the whitespace on the left end is removed; the right trailing space remains.

print(Name.rstrip()) # removes whitespace from the right end 
# Expected Output: " AhSaN"
# Actual Output:   " AhSaN"
# Reason: Only the whitespace on the right end is removed; the left leading space remains.

print(Name.find("s")) # finds the index of the first occurrence of lowercase "s" 
# Expected Output: -1
# Actual Output:   -1
# Reason: Python string methods are strictly case-sensitive. The string contains an uppercase "S" at index 3, but lowercase "s" does not exist anywhere in the string, returning -1.

print(Name.replace("A", "a")) # replaces all occurrences of "A" with "a" 
# Expected Output: " ahSaN "
# Actual Output:   " ahSaN "
# Reason: The uppercase "A" is replaced with lowercase "a", while the other characters remain unchanged.

print(Name.split("h")) # splits the string at each occurrence of "h" 
# Expected Output: [' A', 'SaN ']
# Actual Output:   [' A', 'SaN ']
# Reason: The string is sliced at "h", preserving the surrounding spaces inside the resulting list elements.

print(Name.isalpha()) # checks if all characters are alphabetic 
# Expected Output: True
# Actual Output:   False
# Reason: The string contains spaces, which are structural whitespace characters, not alphabetic letters.

print(Name.isdigit()) # checks if all characters are digits 
# Expected Output: False
# Actual Output:   False
# Reason: The string contains alphabetic characters and spaces.

print(Name.islower()) # checks if all characters are lowercase 
# Expected Output: False
# Actual Output:   False
# Reason: The string contains uppercase letters ("A" and "S").

print(Name.isupper()) # checks if all characters are uppercase 
# Expected Output: False
# Actual Output:   False
# Reason: The string contains lowercase letters ("h" and "n").

print(Name.startswith("A")) # checks if the string starts with "A" 
# Expected Output: True
# Actual Output:   False
# Reason: The string literally starts with a space character `" "`, not the letter `"A"`.

print(Name.endswith("N")) # checks if the string ends with "N" 
# Expected Output: True
# Actual Output:   False
# Reason: The string ends with a trailing space character `" "`, not the letter `"N"`.

print(Name.count("a")) # counts the number of occurrences of lowercase "a" 
# Expected Output: 1
# Actual Output:   1
# Reason: There is exactly one lowercase "a" present in the string.

print(Name.center(10)) # centers the string within a field of width 10 
# Expected Output: "   AhSaN    "
# Actual Output:   "   AhSaN    "
# Reason: The original 7-character string is padded with 3 additional spaces (1 on the left, 2 on the right) to span exactly 10 characters.

print(Name.ljust(10)) # left-justifies the string within a field of width 10 
# Expected Output: " AhSaN    "
# Actual Output:   " AhSaN    "
# Reason: Keeps the original string on the left side and pads the remaining 3 slots with trailing spaces on the right.

print(Name.rjust(10)) # right-justifies the string within a field of width 10 
# Expected Output: "    AhSaN "
# Actual Output:   "    AhSaN "
# Reason: Shifts the original string to the right side and pads the first 3 slots with leading spaces on the left.

print(Name.zfill(10)) # pads the string with zeros on the left to fill a width of 10 
# Expected Output: "000 AhSaN "
# Actual Output:   "000 AhSaN "
# Reason: Prepends exactly 3 zeros to the left of the string to hit the total length constraint of 10.

print(Name.format()) # formats the string using the format method
# Expected Output: " AhSaN "
# Actual Output:   " AhSaN "
# Reason: Returns the string untouched because no replacement field brackets `{}` were passed.

print(Name.isalnum()) # checks if all characters are alphanumeric
# Expected Output: False
# Actual Output:   False
# Reason: The internal and external spaces break the alphanumeric rule (only letters and numbers allowed).

print(Name.isdecimal()) # checks if all characters are decimal digits
# Expected Output: False
# Actual Output:   False
# Reason: Contains zero numeric digits.

print(Name.isidentifier()) # checks if the string is a valid variable/identifier name
# Expected Output: False
# Actual Output:   False
# Reason: Python variables cannot contain spaces, nor can they start with a space.

print(Name.isprintable()) # checks if all characters are printable
# Expected Output: True
# Actual Output:   True
# Reason: Letters and standard blank spaces are fully visible, printable characters (unlike newline `\n` or tab `\t` characters).

print(Name.isspace()) # checks if all characters are whitespace
# Expected Output: False
# Actual Output:   False
# Reason: While it has spaces, it also contains alphanumeric text characters.

print(Name.istitle()) # checks if the string is in title case
# Expected Output: False
# Actual Output:   False
# Reason: For this string to be considered title case, it would need to match the output of `Name.title()`, which is `" Ahsan "`. Because it contains mixed uppercase letters inside the word (`"AhSaN"`), it fails.

print(Name.isnumeric()) # checks if all characters are numeric
# Expected Output: False
# Actual Output:   False
# Reason: Contains text and spacing characters.

print(Name.isascii()) # checks if all characters are standard ASCII
# Expected Output: True
# Actual Output:   True
# Reason: Every character in the string falls cleanly inside the standard 128-character ASCII table encoding.

print(Name.isprintable()) # checks if all characters are printable (Duplicate check)
# Expected Output: True
# Actual Output:   True
# Reason: Confirms again that no hidden, unprintable control sequences exist in the string.

print(Name.isidentifier()) # checks if the string is a valid identifier (Duplicate check)
# Expected Output: False
# Actual Output:   False
# Reason: Confirms again that a string wrapped in spaces cannot function as a legal Python variable name.


# Inputs 

name = input("Name: ") # Allows the user to type/write down their name
print("Hey there, " + name)


