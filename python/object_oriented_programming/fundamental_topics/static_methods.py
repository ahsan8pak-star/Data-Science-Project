# Static Methods = Methods belonging to classes rather than objects (instance)
# Usually used for general utility functions

# Main uses between two types of methods:
# Instance Methods = Operations on class instances (objects)
# Static Methods = Utility Functions, not accessing class data

# For Instance Methods:
# Go to nested_classes.py on lines 19 - 23, 
# lines 35 - 39, lines 52 - 56 and lines 67 - 71

class Employee:

    def __init__(self, name, job_role):
        self.name = name
        self.job_role = job_role

    # Instance Method
    def get_info(self):
        return f"{self.name} : {self.job_role}"

    @staticmethod
    def valid_job_role(job_role):
        valid_job_role = ["Manager", "Janitor", "Chef", "Waiter", "Assistant", "Owner", "Co-Founder"]
        # 'in' checks list membership
        # use '==' (not 'is') for string equality
        # 'is' checks object identity (same memory location)
        return job_role in valid_job_role 
    

manager = Employee("Alice", "Manager")
janitor = Employee("Bob", "Janitor")
chef = Employee("Charlie", "Chef")
waiter = Employee("David", "Waiter")
assistant = Employee("Eve", "Assistant")
owner = Employee("Frank", "Owner")
co_founder = Employee("Grace", "Co-Founder")

print(manager.get_info())
print(janitor.get_info())
print(chef.get_info())
print(waiter.get_info())
print(assistant.get_info())
print(owner.get_info())
print(co_founder.get_info())

within_list = Employee.valid_job_role("Cook")
another_valid_option = Employee.valid_job_role("Chef")

print(f"Cook in Staff? {within_list}")
print(f"Chef in Staff? {another_valid_option}")

