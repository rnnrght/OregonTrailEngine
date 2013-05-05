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

def Messages():
	clearScreen()
	print "Note: \\n represents a newline character and \\t represents a tab."
	print "Please type it exactly as you want to see it."
	messagesData = "startScreen~\n"
	messagesData += raw_input("What would you like the start screen to look like:\n")
	messagesData += '\n~\ngameOver~\n'
	messagesData += raw_input("What would you like the game over screen to look like:\n")
	messagesData += '\n~\nwinScreen~\n'
	messagesData += raw_input("What would you like the win screen to look like:\n")
	messagesData += '~\n'
	messages.write(messagesData)
	
def Event():

	attrList = 'food', 'ammunition', 'money', 'meds', 'sick', 'health'
	numAttr = 0
	for numAttr, attr in enumerate(attrList):
		if numAttr == 0:
			printString = str(numAttr+1) + ": " + attr
		else:
			printString += "\n" + str(numAttr+1) + ": " + attr
			
	printString += "\nWhich attribute would be modified by this choice: "
	
	moreEvents = True
	
	while(moreEvents == True):
		clearScreen()
		print "Note: Put a C, R, or T if you want the event to occur in the city, while        traveling or be a tree event, respectively."
		print "Example: CLookForItems: It occurs in the city and is called LookForItems"
		eventData = raw_input("What is the name and the type of the event: ")
		clearScreen()
		eventData += ':' + raw_input("Enter the text that is shown when the event is triggered:\n")
		clearScreen()
		choices = input("How many choices does the player have after this event is triggered: ")
		
		for i in range(0, choices):
			clearScreen()
			eventData += ':' + raw_input("What is the text displayed in the choice menu:\n")
			clearScreen()
			eventData += ':' + raw_input("What is the chance of this choice succeeding: ")
			
			clearScreen()
			numOfAttr = input("How many player attributes would this choice modify if succeeded: ")
			mods = []
			if numOfAttr == 0:
				eventData += ':nothing:0'
			else:
				for num in range(0, numOfAttr):
					clearScreen()
					choice = getNumber(printString, 1, numAttr+1) - 1
					
					if num == 0:
						eventData += ':' + attrList[choice]
					else:
						eventData += '/' + attrList[choice]
					mods.append(raw_input("How much would this attribute change: "))
			
			for num, mod in enumerate(mods):
				if num == 0:
					eventData += ':' + mod
				else:
					eventData += '/' + mod
			eventData += ':' + raw_input("What is text displayed for the success of this choice:\n")
			
			
			clearScreen()
			numOfAttr = input("How many player attributes would this choice modify if it failed: ")
			mods = []
			for num in range(0, numOfAttr):
				clearScreen()
				choice = getNumber(printString, 1, numAttr+1) - 1
				if num == 0:
					eventData += ':' + attrList[choice]
				else:
					eventData += '/' + attrList[choice]
				mods.append(raw_input("How much would this attribute change: "))
			
			for num, mod in enumerate(mods):
				if num == 0:
					eventData += ':' + mod
				else:
					eventData += '/' + mod
			eventData += ':' + raw_input("What is text displayed for the failure of this choice:\n")
		event.write(eventData)
		
		clearScreen()
		cont = raw_input("Would you like to add another event: y/n\n")
		
		if(cont == 'n'):
			moreEvents = False
 
def Cities():
	clearScreen()
	city = []
	distance = []
	numOfCities = input("How many cities will your game have: ")
	clearScreen()
	city.append(raw_input("Name of the first city: "))
	
	for i in range(1, numOfCities):
		clearScreen()
		city.append(raw_input("Name of the next city: "))
	
	clearScreen()
	distance.append(raw_input("Distance from the starting location to " + city[0] + ": "))
	cityData = city[0] + ':' + distance[0]
	
	for i in range(1, numOfCities):
		clearScreen()
		distance.append(raw_input("Distance from " + city[i-1] + " to " + city[i] + ": "))
		cityData += '\n' + city[i] + ':' + distance[i]
	cities.write(cityData)

# Main function starts here

i = 0
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
			continue
		else:
			os.mkdir(path)
			break
	os.chdir(path)
else:
	os.chdir(dirList[choice])
		
event = open('Event.dat', 'a+')
cities = open('Cities.dat', 'a+')
messages = open('Messages.dat', 'a+')
game = open('Game.dat', 'a+')
fileList = ['Event', 'Cities', 'Messages', 'Game']

clearScreen()	
printString = ''
for i,f in enumerate(fileList):
	if i == 0:
		printString += str(i+1) + ": " + f
	else:
		printString += "\n" + str(i+1) + ": " + f
	
printString += "\nWhich file would you like to modify: "	
choice = getNumber(printString, 1, i+1)

if choice == 1:
	Event()
	
elif choice == 2:
	Cities()
	
elif choice == 3:
	Messages()

elif choice == 4:
	Game()
	
	
	
	
	



	
