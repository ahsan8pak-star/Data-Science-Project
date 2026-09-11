# Nested Classes = Class within a class

# class Outer:
#     class Inner:

# Allows logical closely related group classes
# Encapsulates private details irrelavent to the outer class
# Keeps namesspaces clean -> reduces naming conflicts

class Company:
    print("\nCompanies Sells Products") # Test company class before employee class run

    class Employee:
        def __init__(self, e_name, e_role, e_depart = None):
            self.e_name = e_name
            self.e_role = e_role
            self.e_depart = e_depart

        def employee_details(self):
            if self.e_depart:    
                return f"{self.e_name} : {self.e_role} -> {self.e_depart}"
            else:
                return f"{self.e_name} : {self.e_role}"

    # Outside Employee Class
    def __init__(self, c_name, c_type):
        self.c_name = c_name
        self.c_type = c_type
        self.employees = [] # employee details via names and roles in a list

    def add_employee(self, e_name, e_role, e_depart = None):
        new_employee = self.Employee(e_name, e_role, e_depart)
        self.employees.append(new_employee)

    def employee_list(self): # for loop to iterate the list
        return [employee.employee_details() for employee in self.employees]

    def __str__(self): # converts object memory address into string 
        return f"{self.c_name} | {self.c_type}"


class Organisation:
    print("\nOrganisations Sells Services\n")

    class Employee:

        def __init__(self, e_name, e_role, e_depart = None):
            self.e_name = e_name
            self.e_role = e_role
            self.e_depart = e_depart

        def employee_details(self):
            if self.e_depart:    
                return f"{self.e_name} : {self.e_role} -> {self.e_depart}"
            else:
                return f"{self.e_name} : {self.e_role}"
            
    def __init__(self, o_name, o_type):
        self.o_name = o_name
        self.o_type = o_type
        self.employees = []

    def add_employee(self, e_name, e_role, e_depart = None):
        new_employee = self.Employee(e_name, e_role, e_depart)
        self.employees.append(new_employee)

    def employee_list(self):
        return [employee.employee_details() for employee in self.employees]

    def __str__(self):
        return f"{self.o_name} | {self.o_type}"

# Company Inputs
company = Company("Tesco", "Profit")
company.add_employee("Mark Sterling", "CEO")
company.add_employee("John Dickenson", "COO")
company.add_employee("Olivia Elizabeth", "Manager", "Bakery")

print(company)

# list of (f)ormatted strings
employee_list = company.employee_list()
c_name_header = f" {company.c_name} "

# Use for loop to find max character length
max_len = len(c_name_header)  # Start top header length as baseline
for employee in employee_list:
    if len(employee) > max_len:
        max_len = len(employee)


# Total box width including '| ' and ' |' (4 characters total)
total_width = max_len + 4

# Print formatted box
print(f"\n{c_name_header:-^{total_width}}")
for employee in employee_list:
    print(f"| {employee:<{max_len}} |")
print("-" * total_width) # Dynamic bottom border matching total_width

print("\n" + "=" * 45 + "\n") # Line seperator via TUI Display

# Organisation Inputs
organisation = Organisation("NHS", "Non-Profit")
organisation.add_employee("Emily Karen", "Nurse", "Midwife")
organisation.add_employee("Bob Middleton", "Doctor", "A&E")
organisation.add_employee("Thomas Edward", "Researcher", "Laboratory")

print(f"{organisation}")

employee_list = organisation.employee_list()
o_name_header = f" {organisation.o_name} "

max_content_len = len(o_name_header)
for employee in employee_list:
    if len(employee) > max_content_len:
        max_content_len = len(employee)

total_width = max_content_len + 4

print(f"\n{o_name_header:-^{total_width}}")
for employee in employee_list:
    print(f"| {employee:<{max_content_len}} |")
print("-" * total_width)

