# Worker + Student = PartTimeEmployee 
# Worker + Graduate = FullTimeEmployee

class Worker:
    def __init__(self, name, role):
        self.name = name
        self.role = role

    def worker_info(self):
        return f"{self.name} works as a {self.role}."


class Student:
    def __init__(self, name, course):
        self.name = name
        self.course = course

    def student_info(self):
        return f"{self.name} is studying {self.course}."


class Graduate:
    def __init__(self, name, degree):
        self.name = name
        self.degree = degree

    def graduate_info(self):
        return f"{self.name} graduated with a {self.degree} degree."


class PartTimeEmployee(Worker, Student):
    def __init__(self, name, role, course, hours_per_week):
        Worker.__init__(self, name, role)
        Student.__init__(self, name, course)
        self.hours_per_week = hours_per_week

    def contract_info(self):
        return (
            f"{self.worker_info()}\n"
            f"{self.student_info()}\n"
            f"Working hours: {self.hours_per_week} hours per week."
        )


class FullTimeEmployee(Worker, Graduate):
    def __init__(self, name, role, degree, department):
        Worker.__init__(self, name, role)
        Graduate.__init__(self, name, degree)
        self.department = department

    def contract_info(self):
        return (
            f"{self.worker_info()}\n"
            f"{self.graduate_info()}\n"
            f"Assigned department: {self.department}."
        )


part_time = PartTimeEmployee(
    name = "Sophia",
    role = "Support Assistant",
    course = "Business Management",
    hours_per_week = 20
)


full_time = FullTimeEmployee(
    name = "Daniel",
    role = "Software Engineer",
    degree = "Computer Science",
    department = "Engineering"
)


print(part_time.contract_info())
print("\n" + "-" * 40)
print(full_time.contract_info())

