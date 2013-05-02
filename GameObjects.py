
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

class Effect:
    def __init__(self, attribute, amount, message):
	self.attribute = attribute
	self.amount = amount
	self.message = message

class Event:
    def __init__(self, name, description, options, chances, goodEffects, badEffects):
        self.name = name #same as key
	self.description = description #event message
	self.options = options#array of options
	self.chances = chances#array of % chance of sucess
	self.goodEffects = goodEffects #array of good effects if success
	self.badEffects = badEffects #array of bad effects if fail
