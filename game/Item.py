class Item:
    def __init__(self,name,price):
        self.name=name
        self.price=price

    def __eq__(self, other):
        if isinstance(other, Item):
            return self.name == other.name
        return False
