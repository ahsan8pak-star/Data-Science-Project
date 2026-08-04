# Payment -> Cash, Card, BankTransfer

class Payment:
    def process(self):
        raise NotImplementedError("Subclasses must implement process().")


class Cash(Payment):
    def __init__(self, amount):
        self.amount = amount

    def process(self):
        return f"Cash payment of £{self.amount:.2f} has been received."


class Card(Payment):
    def __init__(self, amount, card_number):
        self.amount = amount
        self.card_number = card_number

    def process(self):
        return f"Card payment of £{self.amount:.2f} processed with card ending {self.card_number[-4:]}."


class BankTransfer(Payment):
    def __init__(self, amount, account_number):
        self.amount = amount
        self.account_number = account_number

    def process(self):
        return f"Bank transfer of £{self.amount:.2f} sent from account number {self.account_number}."

class Cheque(Payment):
    def __init__(self, amount, cheque_number):
        self.amount = amount
        self.cheque_number = cheque_number

    def process(self):
        return f"Cheque payment of £{self.amount:.2f} processed with cheque number {self.cheque_number}."

payments = [
    Cash(25.00),
    Card(120.50, "1234567890123456"),
    BankTransfer(500.00, "987654321"),
    Cheque(100.00, "CHK001")
]

for payment in payments:
    print(payment.process())

