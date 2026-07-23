# Multi Level Inheritance = Inherits Parent class from another Parent
# Parent C <- Parent B <- Parent A

# GrandParent i.e. the main Parent
class Animal: # Parent A
    def __init__(self, name):
        self.name = name

    def eat(self):
        print(f"{self.name} is eating right now.")

    def sleep(self):
        print(f"{self.name} is sleeping at the moment.")

# Parent(Grandparent)
class Prey(Animal): # Parent B
    def flee(self):
        print(f"{self.name} is fleeing from its predators.")

class Predator(Animal): # Parent B 
    def hunt(self):
        print(f"{self.name} is hunting its prey.")

# Child(Parent)
class Rabbit(Prey): # Parent C
    print("This is a Rabbit")

class Hawk(Predator): # Parent C
    print("This is a Hawk")

class Fish(Prey, Predator): # Parent C
    print("This is a Fish")

rabbit = Rabbit("Bugs")
hawk = Hawk("Tony")
fish_main = Fish("Nemo")
fish_spare = Fish("Dory")

# Parent C Variable. Parent A Function
rabbit.eat() 
hawk.sleep()

# Parent C Variable. Parent B Function
rabbit.flee()
hawk.hunt()

# Fish is both prey and predator 
fish_main.flee()
fish_spare.hunt()

