class Order:

    total_revenue = 0 
    total_orders = 0

    def __init__(self, name, type, amount, cost):
        self.name = name
        self.type = type
        self.amount = amount
        self.cost = cost
        Order.total_orders += 1
        Order.total_revenue += (self.cost * self.amount)
        

    # Instance Method
    def details(self):
        return (
            f"\n--- {self.name} ---\n"
            f"Type: {self.type}\n"
            f"Amount: {self.amount}\n"
            f"Cost: £{self.cost:.2f}\n"
        )

    # Class Methods
    @classmethod
    def overall_stats(cls):
        return f"Total Orders: {cls.total_orders}"

    @classmethod
    def average_cost(cls):
        if cls.total_orders == 0:
            return "No Orders. No Costs."

        else:
            return f"Average Cost: £{(cls.total_revenue / cls.total_orders):.2f}"

bread = Order("Sourdough Bread", "Bakery", 2, 2.50)
milk = Order("Whole Milk", "Dairy", 3, 1.20)
eggs = Order("Free-Range Eggs", "Dairy", 1, 3.00)
butter = Order("Unsalted Butter", "Dairy", 2, 2.20)
flour = Order("Plain Flour", "Pantry", 5, 1.50)

print(bread.details())
print(milk.details())
print(eggs.details())
print(butter.details())
print(flour.details())

print("\n--- Overall Stats ---")

print(Order.overall_stats())
print(Order.average_cost())

