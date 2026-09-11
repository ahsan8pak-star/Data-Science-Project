class Person:

    def __init__(self, name, age, is_talking):
        self.name = name
        self.age = age
        self.is_talking = is_talking
    
    def talk(self):
        
        if self.is_talking == True:
            print(f"{self.name} is speaking right now.")

        elif self.age >= 20:
            print(f"{self.name}. You may start after the first speech.")

        else:
            print(f"{self.name}, wait for the other person's turn.")

        