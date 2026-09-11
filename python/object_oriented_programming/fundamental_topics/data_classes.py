# Data Class = A special kind of class designed mostly for holding data, without writing plenty of boilerplate code for regular classes.
# They automatically generate: _init__, __repr__, __eq_ (Python 3.7+)

from dataclasses import dataclass, field # import abstract methods

@dataclass # abstract method decorator

# alternative to defining constructors i.e. boilerplate code for regular classes
class Person: # formatted into a dictionary (sets) of attributes (keys) and types (values)
    name: str
    age: int
    password: str = field(repr=False) # repr=False -> prevents the password from being printed when the object is printed
    is_student: bool = True

    def __post_init__(self): # acts as a setter -> allows for validation of attributes after the object is initialised
        if self.age < 0:
            raise ValueError("Age cannot be negative")

person1 = Person("Ahsan", 21, "A.I.M1ndset")
person2 = Person("Aiman", 19, "aimee6panda")

# Outputs in the following format: Person(name=[str], age=[int], is_student=[bool] -> True as default])
print(person1) 
print(person2)

print(person1 == person2) # similar to __eq__ method in magic_methods.py

