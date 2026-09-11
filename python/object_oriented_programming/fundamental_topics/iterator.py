# Iterator = An object that returns elements one at a time from a sequence (or data stream)
# and remembers its position between calls.

# A Python object is an iterator if it has:
# __iter__() → Returns the iterator object itself
# __next__() → Returns the next item in the sequence
# (raises StopIteration when there's no more items)

import random

class Dice:
    def __init__(self, rolls):
        self.rolls = rolls
        self.count = 0

    def __iter__(self): # Iterator method
        return self

    def __next__(self): # Next method to proceed after each iteration
        if self.count < self.rolls:
            self.count+=1
            return random.randint(1, 6)

        else:
            raise StopIteration

dice = Dice(3) # Prints 3 random numbers between 1 and 6

for die in dice:
    print(die)

