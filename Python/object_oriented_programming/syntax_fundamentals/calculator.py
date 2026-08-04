# Calculator -> add, subtract, divide, multiply, power, square root

class Calculator:
    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def subtract(a, b):
        return a - b

    @staticmethod
    def divide(a, b):
        if b == 0:
            return "Cannot divide by zero."
        return a / b

    @staticmethod
    def multiply(a, b):
        return a * b

    @staticmethod
    def power(a, b):
        return a ** b

    @staticmethod
    def square_root(a):
        if a < 0:
            return "Impossible to calculate square root of a negative number."
        return a ** 0.5
    


print(Calculator.add(10, 5))
print(Calculator.subtract(10, 5))
print(Calculator.divide(20, 4))
print(Calculator.divide(10, 0))
print(Calculator.multiply(6, 7))
print(Calculator.power(2, 3))
print(Calculator.square_root(16))
print(Calculator.square_root(-4)) # return error message

