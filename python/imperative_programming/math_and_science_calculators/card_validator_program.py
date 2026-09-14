"""
Test Credit Card Account Numbers
American Express 378282246310005
American Express 371449635398431
American Express Corporate 378734493671000
Australian Bankcard 5610591081018250
Diners Club 30569309025904
Diners Club 38520000023237
Discover 6011111111111117
Discover 6011000990139424
JCB 3530111333300000
JCB 3566002020360505
MasterCard 5555555555554444
MasterCard 5105105105105100
Visa 4111111111111111
Visa 401288888888188

Information of the card validator program:

1. Remove any '-' or ' '
2. Add all digits in the odd places from right to left
3. Double every second digit from right to left:
[ If result is a two-digit number, ]
[ add the two-digit number together to get a single digit. ]
4. Sum the totals of steps 2 & 3
5. If sum is divisible by 10, the card # is valid
"""

def validate(card_num):
    # Initialise counters INSIDE the function
    sum_odd_digits = 0
    sum_even_digits = 0
    
    # Step 1: Reverse the number layout
    reversed_card = card_num[::-1]

    # Step 2: Add digits in odd places
    for x in reversed_card[::2]: # Start at index 0 in every 2 indexs
        sum_odd_digits += int(x)

    # Step 3: Double every second digit
    for x in reversed_card[1::2]: # Index 1 (2nd digit) at evert 2 indexs
        x = int(x) * 2
        
        if x >= 10: # If Double Digit Number
            sum_even_digits += (1 + (x % 10)) # add its own digits together
            # e.g. 14 -> 1 + 4 = 5

        else: # if x <= 9
            sum_even_digits += x

    # Step 4: Sum totals
    total = sum_odd_digits + sum_even_digits

    # Step 5: Check divisibility
    # Returning a boolean makes this function reusable for other scripts
    return total % 10 == 0


if __name__ == "__main__":

    # Step 1: Get and clean the input
    user_card = input("Enter your card #: ")
    clean_card = user_card.replace("-", "").replace(" ", "")
    
    # Run the validation
    if validate(clean_card):
        print("VALID")

    else:
        print("INVALID")

