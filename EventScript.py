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
	gameTuple = "base travel rate", "base eating rate", "number of hours to scavenge", "number of  characters in your party", "chance to get sick", "health at which you can get sick", "health lost when sick", "health lost with the 'no meal' option", "health lost with the 'small meal' option", "health lost with the 'skimpy meal' option", "health lost with 'fast travel' option", "health lost with 'grueling travel' option", "disease name", "distance unit", "chance of an event", "food name", "ammunition name", "currency name", "medicine name",  "food rate when scavenging", "ammunition rate when scavenging", "money rate when scavenging", "medicine rate when scavenging", "food unit", "ammunition unit", "currency unit", "medicine unit", "health gained when a med kit is used", "chance to cure when a med kit is used", "chance to heal when a med kit is used"
	
	gameDataTuple = "baseTravelRate:", "\nbaseEatRate:", "\nhoursToScavenge:", "\nnumCharacters:", "\nsickChance:", "\nhealthForSickRoll:", "\nlostHealthSick:", "\nlostHealthNoMeal:", "\nlostHealthSmallMeal:", "\nlostHealthSkimpyMeal:", "\nlostHealthFastTravel:", "\nlostHealthGruelingTravel:", "\ndiseaseName:", "\ndistanceUnit:", "\neventChance:", "\nfoodName:", "\nammunitionName:", "\nmoneyName:", "\nmedicineName:", "\nfoodRate:", "\nammunitionRate:", "\nmoneyRate:", "\nmedicineRate:", "\nfoodUnit:", "\nammunitionUnit:", "\nmoneyUnit:", "\nmedicineUnit:", "\nhealthPerHeal:", "\nchanceToCure:", "\nchanceToHeal:"
	
	for i, option in enumerate(gameTuple):
		clearScreen()
		gameData += gameDataTuple[i] + raw_input("What is the " + option + ": ")
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
	eventType = raw_input("Would you like the event to be a ")
 
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

else:
	print "That number is not one of the options."
	
	
	
	
	



	
