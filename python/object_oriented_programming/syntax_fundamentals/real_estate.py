# Property validation example
# Real Estate -> House, Flat, Apartment, Building, Mansion

class RealEstate:
    def __init__(self, name, price):
        self._name = name
        self._price = price

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, new_price):
        if new_price > 0:
            self._price = new_price
        else:
            print("Price must be greater than 0.")

    def description(self):
        return f"{self.name} is priced at £{self.price:,.2f}."


class House(RealEstate):
    def __init__(self, name, price, bedrooms):
        super().__init__(name, price)
        self.bedrooms = bedrooms

    def description(self):
        return f"{self.name}: {self.bedrooms} bedroom house for £{self.price:,.2f}."


class Flat(RealEstate):
    def __init__(self, name, price, floor_number):
        super().__init__(name, price)
        self.floor_number = floor_number

    def description(self):
        return f"{self.name}: Flat on floor {self.floor_number} for £{self.price:,.2f}."


class Apartment(RealEstate):
    def __init__(self, name, price, units):
        super().__init__(name, price)
        self.units = units

    def description(self):
        return f"{self.name}: {self.units} unit apartment for £{self.price:,.2f}."


class Building(RealEstate):
    def __init__(self, name, price, floors):
        super().__init__(name, price)
        self.floors = floors

    def description(self):
        return f"{self.name}: {self.floors}-storey building valued at £{self.price:,.2f}."


class Mansion(RealEstate):
    def __init__(self, name, price, pool):
        super().__init__(name, price)
        self.pool = pool

    def description(self):
        return f"{self.name}: Luxury mansion with {self.pool} for £{self.price:,.2f}."


properties = [
    House("Oakwood House", 450000, 4),
    Flat("Lakeside Flat", 240000, 8),
    Apartment("Harbor Apartments", 300000, 12),
    Building("City Tower", 1200000, 20),
    Mansion("Royal Crest", 2500000, "a private pool")
]

for property in properties:
    print(property.description())

