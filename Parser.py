from GameObjects import Effect
from GameObjects import Event
from GameObjects import City
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
			#Each line has the name of the event, its description, then a bunch of options.
			#Options are represented by a series of additional fields:
				#1. the text for the option
				#2. the chance of a good effect for the option
				#3. the resources affected by a good effect
				#4. the amounts of resource added by a good effect
				#5. text for the good effect
				#6. the resources affected by a bad effect
				#7. the amounts of resource added by a bad effect
				#8. text for the bad effect
		data = open("Event.dat", "r")
		self.eventDefs = {}
		for line in data:
			line = line.strip()
			if line == "": #again, skip blank lines
				continue
			rawEventData = line.split(":")
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
					newEventChances.append(int(rawEventData[i+1]))
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
				except ValueError:
					print "Warning: expected to be able to parse section of line in Event.dat to integer type. Line follows:"
					newEventOptions = []
					newEventChances = []
					newEventGoodEffects = []
					newEventBadEffects = []
					i=i+8
					continue
				i = i+8

			newEvent = Event(newEventName, newEventDescription, newEventOptions, newEventChances, newEventGoodEffects, newEventBadEffects)
			self.eventDefs[newEventName] = newEvent
		
		data.close()

		#Parse in cities.
		#Each city is defined on its own line by a name, a colon, then the distance to the next city.
		#So, for example:
			#Tokyo:400

		self.cities = []
		data = open("Cities.dat", "r")
		for line in data:
			line = line.strip()
			if line == "":
				continue
			rawCityData = line.split(":")
			try:
				self.cities.append(City(rawCityData[0], float(rawCityData[1])))
			except IndexError:
				print "Warning: problem reading line in Cities.dat: ", line
				continue
			except ValueError:
				print "Warning: could not convert distance to float: ", line
				continue

		data.close()

		#Parse in messages.
		#Each message is defined by:
		#A "name" for the message, followed by a tilde and a new line.
		#Then, the full text of the message, followed by a tilde.
		self.messages = {} 
		data = open("Messages.dat", "r").read()
		data = data.split("~")
		data = [item.strip('\n') for item in data]
		rawMessages = [item for item in data if item != ""]
		
		i = 0
		while i < len(rawMessages):
			try:
				self.messages[rawMessages[i].strip()] = rawMessages[i+1]
			except IndexError:
				print "Problem reading messages. Dump: "
				print rawMessages
			i = i+2
	

	def allAttributes(self):
		return self.gameParams
	
	def get(self, paramName):
		try:
			return self.gameParams[paramName]
		except KeyError:
			print "WARNING: REQUEST MADE FOR NON-EXISTENT PARAMETER \"", paramName, '"'
			return ""

	def getEventDefs(self):
		return self.eventDefs

	def getEvent(self):
		return self.eventDefs[random.choice(self.eventDefs.keys())]

	def getCities(self):
		return self.cities
	
	def getMessages(self):
		return self.messages

	def getMessage(self, key):
		try:
			return self.messages[key]
		except KeyError:
			print "WARNING: REQUEST MADE FOR NON-EXISTENT MESSAGE KEY \"", key, '"'
			return ""

if __name__ == '__main__' : #run this file directly for a quick self-test
	print "Parser self-test:"
	print "- constructing Parser object:"
	parser = Parser()

	print "- printing attributes dictionary:"
	print parser.allAttributes()

	print "\n"
	print "- printing results of get(\"ammoRescName\")"
	print parser.get("ammoRescName")
	print "- printing results of get(\"garbage\")"
	print parser.get("garbage")
	print "- printing results of get(\"fuelScavRate\")"
	print parser.get("fuelScavRate")

	print "- printing a random event"
	print parser.getEvent().name
	print parser.getEvent().description

	print "- printing city names"
	for city in parser.getCities():
		print city.name
		print city.distanceTo

	print "- dumping message dictionary"
	print parser.getMessages()
