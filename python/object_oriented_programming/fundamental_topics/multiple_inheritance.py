# Multiple Inheritance = A Single Child Class Inherits Multiple (more than 2) Parent Classes
# Child C -> Parent A & B

class Father: # Parent A
    def __init__(self, father_name, father_age):
        self.father_name = father_name
        self.father_age = father_age

    def father_info(self):
        print(f"\nFather: {self.father_name}")
        print(f"Age: {self.father_age}")

class Mother: # Parent B
    def __init__(self, mother_name, mother_age):
        self.mother_name = mother_name
        self.mother_age = mother_age

    def mother_info(self):
        print(f"\nMother: {self.mother_name}")
        print(f"Age: {self.mother_age}")


# Son inherits from BOTH Father and Mother
class Son(Father, Mother): # Child C -> Parent A & B
    def __init__(self, son_name, son_age):
        self.son_name = son_name
        self.son_age = son_age

    def son_info(self):
        print(f"\nSon: {self.son_name}")
        print(f"Age: {self.son_age}")


# Daughter also inherits from BOTH Father and Mother
class Daughter(Father, Mother): # Child D -> Parent A & B
    def __init__(self, daughter_name, daughter_age):
        self.daughter_name = daughter_name
        self.daughter_age = daughter_age

    def daughter_info(self):
        print(f"\nDaughter: {self.daughter_name}")
        print(f"Age: {self.daughter_age}")


# Instantiating and Testing
son_member = Son(son_name = "Leo", son_age = 15) # The ordering DOESN'T MATTER in the CHILD Class

# This ordering MATTERS i.e. HOW it's Called.
son_member.son_info() # Variable [Class.variable(s)] . Method() 


daughter_member = Daughter(daughter_name = "Mia", daughter_age = 12)
daughter_member.daughter_info()

father_member = Father(father_name = "Arthur", father_age = 45)
father_member.father_info()

mother_member = Mother(mother_name = "Elena", mother_age = 43)
mother_member.mother_info()

