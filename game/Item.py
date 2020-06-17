class Item:
    def __init__(self, name, price, amount_for_sale=0):
        self.name = name
        self.price = price
        self.amount_for_sale = amount_for_sale

    def __eq__(self, other):
        if isinstance(other, Item):
            return self.name == other.name
        return False
