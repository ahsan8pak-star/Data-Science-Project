class School:
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.students = []

    def add_student(self, student):
        self.students.append(student)

    def list_students(self):
        return [f"{student.name}, Age: {student.age}" for student in self.students]

    def remove_student(self, student):
        if student in self.students:
            self.students.remove(student)

class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

school = School("Greenwood High", "123 Main St")

student1 = Student("Alice", 15)
student2 = Student("Bob", 16)
student3 = Student("Charlie", 14)

school.add_student(student1)
school.add_student(student2)
school.add_student(student3)

print(school.name)
print(school.address)
print("-" * 30)  # Line Separator for School name and its students below

for student in school.list_students():
    print(student)

