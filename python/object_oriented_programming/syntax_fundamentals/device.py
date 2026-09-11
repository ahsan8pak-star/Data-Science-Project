from abc import ABC, abstractmethod 

class Device(ABC):
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model

    @abstractmethod
    def turn_on(self):
        pass

    @abstractmethod
    def turn_off(self):
        pass

class Phone(Device):
    def __init__(self, brand, model, number):
        super().__init__(brand, model)
        self.number = number

    def phone_number(self):
        return f"The phone number is {self.number}."

    def turn_on(self):
        print(f"The {self.brand} {self.model} phone is turning on.")

    def turn_off(self):
        print(f"The {self.brand} {self.model} phone is turning off.")

class Laptop(Device):
    def __init__(self, brand, model, screen_size):
        super().__init__(brand, model)
        self.screen_size = screen_size

    def screen_size_info(self):
        return f"The screen size is {self.screen_size}."

    def turn_on(self):
        print(f"The {self.brand} {self.model} laptop is turning on.")

    def turn_off(self):
        print(f"The {self.brand} {self.model} laptop is turning off.")

class Tablet(Device):
    def __init__(self, brand, model, storage):
        super().__init__(brand, model)
        self.storage = storage

    def storage_info(self):
        return f"The storage capacity is {self.storage}."

    def turn_on(self):
        print(f"The {self.brand} {self.model} tablet is turning on.")

    def turn_off(self):
        print(f"The {self.brand} {self.model} tablet is turning off.")

phone = Phone("Apple", "IPhone XR", "123-456-7890")
laptop = Laptop("Dell", "XPS 15", "15.6 inches")
tablet = Tablet("Samsung", "Galaxy Tab S7", "128GB")

print(phone.phone_number())
print(laptop.screen_size_info())
print(tablet.storage_info())

print("================================") # TUI Line Separator

phone.turn_on()
laptop.turn_on()
tablet.turn_on()

print("================================")

phone.turn_off()
laptop.turn_off()
tablet.turn_off()

