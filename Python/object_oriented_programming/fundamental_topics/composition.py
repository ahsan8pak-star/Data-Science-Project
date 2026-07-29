# Composition = The composed object owns its components
# Can't exist independently (always dependent) -> "owns-a" relationship

class Engine: # Component object (Part)
    def __init__(self, horse_power):
        self.horse_power = horse_power

class Wheel: # Component object (Another Part)
    def __init__(self, size):
        self.size = size

class Car: # Composite Object (Composition Starts)
    def __init__(self, brand, model, horse_power, wheel_size):
        self.brand = brand
        self.model = model
        self.engine = Engine(horse_power) # Instantiating component object directly (Composition)
        self.wheels = [Wheel(wheel_size) for wheel in range(4)] # Car must have 4 wheels

    def display_car(self): # Accesses component data via [ self . 'Child_Object' . 'Child_Attribute' ]
        return f"{self.brand} {self.model}: {self.engine.horse_power}hp | {self.wheels[0].size}in"

car1 = Car(
    brand = "BMW", 
    model = "M3 GTR", 
    horse_power = 550, 
    wheel_size = 19
)

print(car1.display_car())

car2 = Car(
    brand = "Chevrolet", 
    model = "Corvette Z06", 
    horse_power = 670, 
    wheel_size = 20
)

print(car2.display_car())

