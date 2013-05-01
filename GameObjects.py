
class Character:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.sick = False

class Supply:
    def __init__(self, name, rate):
        self.name = name
        self.rate = rate
        self.amount = 0
