# Class Method = Allows operations related to the class itself
# Use (cls) as first parameter under @classmethod, representing the class itself
# Used for Class-Level Data -> Requires Access to the Class itself directly 

class Student:

    # Class Variables
    total = 0 
    overall_grade = 0

    def __init__(self, name, university, degree, grade):
        self.name = name
        self.university = university
        self.degree = degree
        self.grade = grade
        Student.total += 1
        Student.overall_grade += grade
        

    # Instance Method
    def details(self):
        return (
            f"\n--- {self.name} ---\n"
            f"University of: {self.university}\n"
            f"Qualification: {self.degree}\n"
            f"Grade: {self.grade}%\n"
        )

    # Class Methods
    @classmethod
    def student_total(cls):
        return f"Student Population: {cls.total}"

    @classmethod
    def average_grade(cls):
        if cls.total == 0:
            return "No Students. No Grade."

        else:
            return f"Average Grade: {(cls.overall_grade / cls.total):.2f}"

UoB = Student("Hamza Khan", "Birmingham", "BA Business Studies", 81)
UoM = Student("Ahmed Al-Farsi", "Manchester", "MSc Mechanical Engineering", 72)
UoR = Student("Ahsan Iqbal", "Reading", "BSc Computer Science", 75)
UoE = Student("Ilyas Ifzal", "Essex", "PhD Biochemistry in Pharmacy", 68)
UoS = Student("Bilal Ibn Hisham ", "Surrey", "BA Philiosphy", 73)

print(UoB.details())
print(UoM.details())
print(UoR.details())
print(UoE.details())
print(UoS.details())

# Python's Interpreter Executes Line-by-Line Code i.e. Top to Bottom Ascendingly
# Placing them at the bottom, allows class variables to be fully updated by their instances
print(Student.student_total())
print(Student.average_grade())

