# Inheritance = Allows a class to inherit attributes and methods from another class
# Helps with code reusability and extensibility 
# e.g. class Child(Parent)

class Animal:
    def __init__(self, name): # Constructor
        self.name = name

    def eat(self): # Methods
        print(f"{self.name} is eating right now.")

    def sleep(self):
        print(f"{self.name} is asleep. Do not disturb {self.name}")

    def play(self):
        print(f"{self.name} is playing. You can come and play with them.")

eating = Animal("A.I.M") 
sleeping = Animal("Doug")
playing = Animal("MeowMeow")

print(eating.name)
eating.eat()

print(sleeping.name)
sleeping.sleep()

print(playing.name)
playing.play()


class Dog(Animal):
    def speak(self):
        print("WOOF!")

    def walk(self):
        print("pat, pat, pat...")

class Cat(Animal):
    def speak(self):
        print("MEOW!")

    def walk(self):
            print("crawl, crawl, crawl...")

class Mouse(Animal):
    def speak(self):
        print("SQUEEK!")

    def walk(self):
            print("tiptoe, tiptoe, tiptoe...")

# Objects
dog = Dog("Scooby") # Dog -> WOOF!
cat = Cat("Garfield") # Cat -> MEOW!
mouse = Mouse("Mickey") # Mouse -> SQUEEK!

print(dog.name)
dog.speak()
dog.walk()

print(cat.name)
cat.speak()
cat.walk()

print(mouse.name)
mouse.speak()
mouse.walk()
