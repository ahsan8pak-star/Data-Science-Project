# Has its dedicated file to act as a import module 
# Reasons: Cleaner code structure and allows various attribites (variables) to be inputted

class Car:
    
    # Constructor
    def __init__(self, model, year, colour, for_sale):
        self.model = model
        self.year = year
        self.colour = colour
        self.for_sale = for_sale

    # Methods = "Actions" that objects can perform

    def drive(self):
        print(f"You are driving a {self.colour} {self.model}!")

    def stop(self):
        print(f"You finished driving a {self.colour} {self.model}.")

    def description(self):
        print(f"This is a {self.year} {self.colour} {self.model}")

        if self.for_sale == True:
            print("You can buy this car right now!")

        else:
            print("A priceless car, not worthy to be auctioned.")

