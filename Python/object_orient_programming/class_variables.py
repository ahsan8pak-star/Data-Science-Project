# Class Variables = Global variable i.e. shared amongst all class instances

# Defined outside the constructor
# Allows to share data amongst all subjects created from that class

class Student:

    university = "Reading" # class variable == global variable
    num_students = 0 # Initialise class variable

    def __init__(self, name, age):
        self.name = name
        self.age = age
        Student.num_students += 1 # Increment for every object passed

    def level(self):

        years = 21 - self.age

        if student1.university == student2.university == student3.university:
            
            if self.age >= 21:
                print(f"Congratulations {self.name}, you are now graduating.")
        
            else:
                print(f"Continue studying {self.name}, just {years} year(s) left.")
        else:
            print("All students must be at the same university to do this.")

student1 = Student("Ahsan", 21)
student2 = Student("Hamza", 20)
student3 = Student("Yahya", 19)

student1.level()
student2.level()
student3.level()

print(f"University of {Student.university}") # Class.class variable
print(f"{Student.num_students}")

