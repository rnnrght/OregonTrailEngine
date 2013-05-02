from GameObjects import Effect
from GameObjects import Event
import random

class Parser:
	def __init__(self):
		#Parse in basic game parameters
		#Each game parameter is on its own line.
		#Each line has the name of the attribute, then a colon, then the value.
		#For example:
		#partsRescName:flux capacitors
		#defines an attribute called "partsRescName" with the value "flux capacitors"
		data = open("Game.dat", "r")
		self.gameParams = {}
		for line in data:
			line = line.strip()
			if line == "":	 #skipping blank lines like this
				continue #lets us keep the data file more readable

			attribute = line.split(":")
			try:
				self.gameParams[attribute[0].strip()] = attribute[1].strip()
			except IndexError:
				self.gameParams[attribute[0].strip()] = ""
		data.close

		#Parse in event definitions.
		#Each event definition is on its own line.
		#Each line has the name of the event, its description, then a list of options.
		#Each options consist of three fields
		data = open("Event.dat", "r")
		self.eventDefs = {}
		for line in data:
			print line
			line = line.strip()
			if line == "": #again, skip blank lines
				continue
			rawEventData = line.split(":")
			print rawEventData
			newEventName = ""
			newEventDescription = ""
			newEventOptions = []
			newEventChances = []
			newEventGoodEffects = []
			newEventBadEffects = []
			try:
				newEventName = rawEventData[0]
				newEventDescription = rawEventData[1]
			except IndexError:
				print "Warning: error reading from Event.dat. Line follows:"
				print line
				continue
			i = 2
			while i < len(rawEventData):
				try:
					newEventOptions.append(rawEventData[i])
					newEventChances.append(rawEventData[i+1])
					newEventGoodEffects.append(Effect(rawEventData[i+2], rawEventData[i+3], rawEventData[i+4]))
					newEventBadEffects.append(Effect(rawEventData[i+5], rawEventData[i+6], rawEventData[i+7]))
				except IndexError:
					print "Warning: error reading options in Event.dat. Line follows:"
					print line
					newEventOptions = []
					newEventChances = []
					newEventGoodEffects = []
					newEventBadEffects = []
					i = i+8
					continue
				i = i+8

			newEvent = Event(newEventName, newEventDescription, newEventOptions, newEventChances, newEventGoodEffects, newEventBadEffects)
			self.eventDefs[newEventName] = newEvent
		
		data.close()

	def allAttributes(self):
		return self.gameParams
	
	def get(self, paramName):
		try:
			return self.gameParams[paramName]
		except KeyError:
			return ""

	def getEventDefs(self):
		return self.eventDefs

	def getEvent(self):
		return self.eventDefs[random.choice(self.eventDefs.keys())]
		

if __name__ == '__main__' : #run this file directly for a quick self-test
	print "Parser self-test:"
	print "- constructing Parser object:"
	parser = Parser()

	print "- printing attributes dictionary:"
	print parser.allAttributes()

	print "\n\n"
	print "- printing results of get(\"ammoRescName\")"
	print parser.get("ammoRescName")
	print "- printing results of get(\"garbage\")"
	print parser.get("garbage")
	print "- printing results of get(\"fuelScavRate\")"
	print parser.get("fuelScavRate")

	print "- printing a random event"
	print parser.getEvent().name
	print parser.getEvent().description
