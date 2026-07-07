"""
Monoalphabetic Substitution Cipher / Random Substitution Cipher Encryption

Unlike a standard Caesar Cipher (which shifts indices by a fixed numeric offset),
this program creates a random substitution cipher. It creates a completely randomized 
mapping array ('key') where every unique character points to a shuffled counterpart.

"""

import random
import string

# Creates main sequence containing spaces, punctuations, digits, and letters
chars = " " + string.punctuation + string.digits + string.ascii_letters 
chars = list(chars) 

# Create an identical copy of the character pool and randomly scramble it to act as our cipher key
key = chars.copy() 
random.shuffle(key) 

# ENCRYPT
plain_text = input("Enter a message to encrypt: ")
cipher_text = "" 

for letter in plain_text:

    # Checks the input character existance in the tracked list to avoid ValueErrors
    if letter in chars:
        index = chars.index(letter) # Finds the position / index of the character / item (in the alphabet)
        cipher_text += key[index] # Swaps out the character at the exact same position in the scrambled key
    else:
        cipher_text += letter # Fallback: leaves unknown characters (like tabs/newlines) untouched

print(f"Original Message : {plain_text}")
print(f"Encrypted Message: {cipher_text}\n")

# DECRYPT
cipher_input = input("Enter a message to decrypt: ")
decrypted_text = "" 

for letter in cipher_input:

    # Reverse lookup strategy
    if letter in key:
        index = key.index(letter) # Finds the location of the scrambled character in the key array
        decrypted_text += chars[index] # Extract its original matching value from the alphabet system
    else:
        decrypted_text += letter

print(f"Encrypted Input  : {cipher_input}")
print(f"Decrypted Message: {decrypted_text}")