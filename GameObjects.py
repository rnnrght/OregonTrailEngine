
class Character:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.isSick = False

class Supply:
    def __init__(self, name, rate):
        self.name = name
        self.rate = rate
        self.amount = 0

class City:
    def __init__(self, name, distanceTo):
        self.name = name
        self.distanceTo = distanceTo

class Event:
    def __init__(self, name):
        self.name = name
	self.description = description
	self.options = options
	self.chances = chances
	self.goodEffects = goodEffects 
	self.badEffects = badEffects
