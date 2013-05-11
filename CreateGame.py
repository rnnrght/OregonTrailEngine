#!/usr/bin/python

import os
import sys
import string

def clearScreen():
    os.system( [ 'clear', 'cls' ][ os.name == 'nt' ] )

def getNumber(menu, min, max, dontInclude = []):
    isGood = True
    while True:
        clearScreen()
        if isGood == False:
            print "ERROR: Input a valid number\n"
            isGood = True
        string = raw_input(menu)
        if string == "":
            isGood = False
            continue
        for char in string:
            if ord(char) < 48 or ord(char) > 57:
                isGood = False
                break

        if isGood:
            num = int(string)
            if num >= min and num <= max and num not in dontInclude:
                break
        isGood = False
    return num

# This function creates and writes all the data to the Game.dat file
def Game():
	gameData = ''
	gameTuple = "base travel rate", "base eating rate", "number of hours to scavenge", "number of  characters in your party", "chance to get sick", "health at which you can get sick", "health lost when sick", "health lost with the 'no meal' option", "health lost with the 'small meal' option", "health lost with the 'skimpy meal' option", "health lost with 'fast travel' option", "health lost with 'grueling travel' option", "disease name", "distance unit", "chance of an event", "food rate when scavenging", "ammunition rate when scavenging", "money rate when scavenging", "medicine rate when scavenging", "food unit", "ammunition unit", "currency unit", "medicine unit", "health gained when a med kit is used", "chance to cure when a med kit is used", "chance to heal when a med kit is used"

	gameDataTuple = "baseTravelRate:", "\nbaseEatRate:", "\nhoursToScavenge:", "\nnumCharacters:", "\nsickChance:", "\nhealthForSickRoll:", "\nlostHealthSick:", "\nlostHealthNoMeal:", "\nlostHealthSmallMeal:", "\nlostHealthSkimpyMeal:", "\nlostHealthFastTravel:", "\nlostHealthGruelingTravel:", "\ndiseaseName:", "\ndistanceUnit:", "\neventChance:", "\nfoodName:", "\nammunitionName:", "\nmoneyName:", "\nmedicineName:", "\nfoodRate:", "\nammunitionRate:", "\nmoneyRate:", "\nmedicineRate:", "\nfoodUnit:", "\nammunitionUnit:", "\nmoneyUnit:", "\nmedicineUnit:", "\nhealthPerHeal:", "\nchanceToCure:", "\nchanceToHeal:"

	for i, data in enumerate(gameDataTuple):
		clearScreen()
		gameData += data
		if i > 18 and i < 14:
			gameData += raw_input("What is the " + gameTuple[i] + ": ")
	game.write(gameData)

def messageScreen(screenType):
	screenMessage = ''
	if screenType == 1:
		screen = " start screen "
	elif screenType == 2:
		screen = " game over screen "
	elif screenType == 3:
		screen = " win screen "
		
	print "Note: Hit enter to go to the next line. Once you go to the next line you cannot go back."
	print "2nd Note: Hit enter twoce to finish the message"
	print "What would you like the" + screen + "to look like:\n"
	while True:
		line = raw_input()
		if screenMessage.strip() == '':
			break
		screenMessage += line
		
	return screenMessage

# This function creates and writes messages to the Messages .dat file
def Messages():
	clearScreen()
	
	messagesData = "startScreen~\n"
	messagesData += messageScreen(1)

	messagesData += '\n~\ngameOver~\n'
	messagesData += messageScreen(2)
	
	messagesData += '\n~\nwinScreen~\n'
	messagesData += messageScreen(3)
	messagesData += '~\n'
	
	messages = open("Messages.dat", 'w')
	messages.write(messagesData)
	messages.close()

def modMessages():
	clearScreen()
	print "Note: \\n represents a newline character and \\t represents a tab."
	print "The current screens are:"

# This is one of the helper functions for the Event method. 
# It shortens the code for creating the attributes and values modified for the choices
def eventAttr(eventDataList, SuccFail):
	modAttr = []
	modVal = []
	SuccFailList = [' failed: ', ' succeeded: ']
	attrList = ['1: Food', '2: Ammunition', '3: Money', '4: Meds', '5: Sick', '6: Health']
	attrTuple = 'food', 'ammunition', 'money', 'meds', 'sick', 'health'
	numOfAttr = 0
	
	clearScreen()
	print "Note: If it triggers a tree event, put 1."
	numOfAttr = input("How many player attributes would this choice modify if it" + SuccFailList[SuccFail])
			
	if numOfAttr == 0:
		eventDataList.append('nothing:0')
				
	elif numOfAttr == 1:
		clearScreen()
		printString = '\n'.join(attrList)
		printString += "\n7: Tree Event"
		printString += "\nWhich attribute would be modified by this choice or is there a tree event: "
		choice = getNumber(printString, 1, 7) - 1
		if choice == 6:
			Event(2)
			eventDataList.append('0')
		else:
			eventDataList.append(attrTuple[choice])
			eventDataList.append(raw_input("How much would this attribute change: "))
					
	else:
		printString = '\n'.join(attrList)
		printString += "\nWhich attribute would be modified by this choice: "
		
		for num in range(0, numOfAttr):
			clearScreen()
			choice = getNumber(printString, 1, 6) - 1
				
			modAttr.append(attrTuple[choice])
			modVal.append(raw_input("How much would this attribute change: "))
			clearScreen()
		eventDataList.append('/'.join(modAttr))
		eventDataList.append('/'.join(modVal))
	return eventDataList

# This function creates and add events to the Event.dat file
def Event(EventType):
	moreEvents = True

	while moreEvents == True:
		eventData = ''
		eventDataList = []
		clearScreen()
		
		if EventType == 1:
			print "Note: Put a C or R if you want the event to occur in the city or while traveling, respectively."
			print "Example: CLookForItems: It occurs in the city and is called LookForItems"
			eventDataList.append(raw_input("What is the name and the type of the event: "))
		else:
			eventDataList.append('\nT' + raw_input("What is the name of the tree event: "))

		clearScreen()
		eventDataList.append(raw_input("Enter the text that is shown when the event is triggered:\n"))
		
		clearScreen()
		choices = input("How many choices does the player have after this event is triggered: ")

		for i in range(0, choices):
			clearScreen()
			eventDataList.append(raw_input("What is the text displayed in the choice menu:\n"))
			
			clearScreen()
			eventDataList.append(raw_input("What is the chance of this choice succeeding: "))
			eventDataList = eventAttr(eventDataList, 1)
			eventDataList.append(raw_input("What is the text displayed for the success of this choice:\n"))

			clearScreen()
			eventDataList = eventAttr(eventDataList, 0)
			eventDataList.append(raw_input("What is text displayed for the failure of this choice:\n"))
		
		eventData = ':'.join(eventDataList)
		event = open("Event.dat", 'a')
		event.write(eventData)
		event.close()

		clearScreen()
		if EventType == 1:
			cont = raw_input("Would you like to add another event: y/n\n")
		else:		
			return eventDataList[0]
		if(cont == 'n'):
			moreEvents = False

# This function allows to add or delete events form the Event.dat file		
def modEvent():
	while True:
		printString = "1: Add events\n2: Delete events\n3: Exit\nWhat would you like to do: "	
		choice = getNumber(printString, 1, 3)
		if choice == 1:
			Event(1)
		elif choice == 2:
			eventFile = []
			deleteList = []
			events = open("Event.dat", 'r')
			for eventLine in events:
				eventFile.append(eventLine)
				deleteList.append(eventLine.split(':')[0])
				
			for i, element in enumerate(deleteList):
				deleteList[i] = str(i+1) + ': ' + element
			
			printString = '\n'.join(deleteList)
			printString += "\nWhich event would you like to delete: "
			choice = getNumber(printString, 1, i+1) - 1
			eventFile.pop(choice)
			eventData = '\n'.join(eventFile)
			events = open("Event.dat", 'w')
			events.write(eventData)
			events.close()
		elif choice == 3:
			break
			
# This is function that is called to add cities when a new directory is created
def Cities():
	cities = open('Cities.txt', 'w')
	city = []
	distance = []
	numOfCities = ''

	while not numOfCities.isdigit():
		numOfCities = raw_input("How many cities would you like to add: ")
		clearScreen()
		if not numOfCities.isdigit():
			print "INVALID INPUT: PLEASE INPUT A NUMERICAL VALUE\n"

	numOfCities = int(numOfCities)
	city.append(raw_input("Name of the first city: "))

	for i in range(1, numOfCities):
		clearScreen()
		print '\n'.join(city)
		city.append(raw_input("Name of the next city: "))

	clearScreen()
	distance.append('')
	while not distance[0].isdigit():
		distance[0] = raw_input("Distance from the starting location to " + city[0] + ": ")
		clearScreen()
		if not distance[0].isdigit():
			print "INVALID INPUT: PLEASE INPUT A NUMERICAL VALUE\n"

	cityData = city[0] + ':' + distance[0]

	for i in range(1, numOfCities):
		clearScreen()
		distance.append('')
		while not distance[i].isdigit():
			distance[i] = raw_input("Distance from " + city[i-1] + " to " + city[i] + ": ")
			clearScreen()
			if not distance[i].isdigit():
				print "INVALID INPUT: PLEASE INPUT A NUMERICAL VALUE\n"

		cityData += '\n' + city[i] + ':' + distance[i]

	cities.write(cityData)
	cities.close()


# This is the function that is called when the user wants to modify an existing city file
def modCities():
	while True:

		clearScreen()
		cityList = []
		printString = '1: Add cities\n2: Delete cities\n3: Exit\nWhat would you like to do: '
		choice = getNumber(printString, 1, 3)
		cities = open('Cities.txt', 'r')
		cityList = cities.readlines()
		cities.close()
		i = 0

		while choice == 1:
			clearScreen()
			printString = ''
			for i, city in enumerate(cityList):
				printString += str(i+1) + ': ' + city
			printString += str(i+2) + ': Add a city at the end of the list'
			printString += "\nWhere would you like to add the city: "

			print "Note: It takes that index and pushes that current index farther down the list."

			index = getNumber(printString, 1, i+2) - 1
			city = raw_input("What is the name of the city: ") + ':'
			clearScreen()

			distance = ''
			while not distance.isdigit():
				distance = raw_input("What is the distance until the next city is reached: ")
				clearScreen()
				print "INVALID INPUT: PLEASE INPUT A NUMERICAL VALUE\n"

			city += distance + '\n'
			cityList.insert(index, city)
			clearScreen()
			if raw_input("Would you like to add another city: y/n\n") == 'n':
				break

		while choice == 2:
			printString = ''

			for i, city in enumerate(cityList):
				printString += str(i+1) + ': ' + city

			clearScreen()
			printString = printString.strip('\n')

			printString += "\nWhich line would you like to delete: "
			choice = getNumber(printString, 1, i+1)	- 1
			cityList.pop(choice)
			clearScreen()
			if raw_input("Do you want to delete another line: y/n\n") == 'n':
				break

		if choice == 3:
			break
		city = ''.join(cityList)

		cities = open('Cities.txt', 'w')
		cities.write(city)
		cities.close()



# Main function starts here

i = 0
new = False
printString = "Modify a directory"
dirList = os.listdir("gameData")

for i, direc in enumerate(dirList):
	printString += "\n\t" + str(i+1) + ": " + direc


printString += "\n\t" + str(i+2) +  ": " + "Create a new directory"
printString += "\nWhat would you like to do: "
choice = getNumber(printString, 1, i+2) - 1

os.chdir("gameData")
clearScreen()

if choice == i + 1:
	while True:
		path = raw_input("What is the name of the directory: ")
		if os.path.isdir(path):
			clearScreen()
			print "ERROR: THAT DIRECTORY ALREADY EXISTS\n"
			continue
		else:
			os.mkdir(path)
			break
	os.chdir(path)
	new = True
else:
	os.chdir(dirList[choice])

fileList = ['Event', 'Cities', 'Messages', 'Game', 'Exit']

clearScreen()
printString = ''
for i,f in enumerate(fileList):
	printString += "\n" + str(i+1) + ": " + f

printString = printString.strip('\n')
printString += "\nWhich file would you like to modify: "

while True:
	clearScreen()
	choice = getNumber(printString, 1, i+1)

	if new == True:
		if choice == 1:
			event = open("Event.dat", 'w')
			event.close()
			Event(1)
		elif choice == 2:
			Cities()
		elif choice == 3:
			Messages()
		elif choice == 4:
			Game()
		elif choice == 5:
			break

	else:
		if choice == 1:
			modEvent()
		elif choice == 2:
			modCities()
		elif choice == 3:
			modMessages()
		elif choice == 4:
			modGame()
		elif choice == 5:
			break
