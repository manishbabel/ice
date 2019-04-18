
class Order:
    def __init__(self, name, price, quantity):
        self._name = name
        self.price = price
        self._quantity = quantity  # (1)

    @property
    def quantity1(self):
        return self._quantity

    @quantity1.setter
    def quantity1(self, value):
        if value < 0:
            raise ValueError('Cannot be negative.')
        self._quantity = value  # (2)

apple_order = Order('apple', 1, 10)
apple_order._quantity = -10
