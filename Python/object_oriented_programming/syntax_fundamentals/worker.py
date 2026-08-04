class Worker():
    def __init__(self, name, position):
        self.name = name
        self.position = position

    def work(self):
        return f"{self.name} is working as a {self.position}."

class Manager(Worker):
    def __init__(self, name, position, department):
        super().__init__(name, position)
        self.department = department

    def manage(self):
        return f"{self.name} is managing the {self.department} department."

class Developer(Worker):
    def __init__(self, name, position, programming_language):
        super().__init__(name, position)
        self.programming_language = programming_language

    def code(self):
        return f"{self.name} is coding in {self.programming_language}."

class Designer(Worker):
    def __init__(self, name, position, design_tool):
        super().__init__(name, position)
        self.design_tool = design_tool

    def design(self):
        return f"{self.name} is designing using {self.design_tool}."

class Intern(Worker):
    def __init__(self, name, position, mentor):
        super().__init__(name, position)
        self.mentor = mentor

    def learn(self):
        return f"{self.name} is learning from {self.mentor}."

class Writer(Worker):
    def __init__(self, name, position, genre):
        super().__init__(name, position)
        self.genre = genre

    def write(self):
        return f"{self.name} is writing in the {self.genre} genre."

company = [
    Manager("Alice", "Manager", "Engineering"), 
    Developer("Bob", "Developer", "Python"), 
    Designer("Charlie", "Designer", "Figma"),
    Writer("Eve", "Writer", "Fiction"), 
    Intern("David", "Intern", "Eve")
    ]

for worker in company:
    print("\n==================================")
    print(worker.work())

    match worker:
        case Manager():
            print(worker.manage())

        case Developer():
            print(worker.code())

        case Designer():
            print(worker.design())

        case Intern():
            print(worker.learn())

        case Writer():
            print(worker.write())

        case _:
            print("Unknown Worker Type.")

    print("==================================\n")

