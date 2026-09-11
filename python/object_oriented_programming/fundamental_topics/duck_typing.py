# "Duck Typing" -> "Looks like a duck, acts like a duck, must be a duck"
# e.g. ducks quack, eat bread, and swim and float in water

class Animal:
    alive = True

class Cow(Animal):
    def speak(self):
        print("Moo!")

    def move(self):
        print("Walking")

    def eat(self):
        print("grass..")  

class Duck(Animal):
    def speak(self):
        print("QUACK!")

    def move(self):
        print("Swiming")

    def eat(self):
        print("bread...")

class Plane: # Vehicle != Animal
# 'def fly' has to be reused as the necessary attributes -> prevent AttributeError
# i.e. def fly(self) -> def speak, move and eat

    # Local Variable for its class to prevent 
    alive = False 

    def speak(self):
        print("FLY!!!")

    def move(self):
        print("FLY!!!")

    def eat(self):
        print("FLY!!!")

animals = [Duck(), Cow(), Plane()] # Ordering matters in this section

for animal in animals:
    print(f"Animal?: {animal.alive}")
    animal.speak()
    animal.eat()
    animal.move()

