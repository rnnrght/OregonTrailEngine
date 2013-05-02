#!/usr/bin/python

from GameObjects import *
import os

##### VARIOUS FUNCTIONS #####

def clearScreen():
    os.system( [ 'clear', 'cls' ][ os.name == 'nt' ] )

def displayStatus():
    clearScreen()
    global currentCity
    global distanceUnit
    global Supplies
    global diseaseName
    city = Cities[currentCity]

    print "Heading to: " +  city.name
    print "Distance: " +  str(city.distanceTo) + " " + distanceUnit + "\n"
    print "Pace of travel: " + pace
    print "Food per meal: " + meal + "\n"

    for supply in Supplies:
        print supply.name + ": " + str(supply.amount)

    print ""

    for character in Characters:
        print character.name + ": "
        print "- Health: " + str(character.health)
        if character.isSick:
            print "- Has " + diseaseName
        print ""

def travelLoop():
    global currentCity
    global Supplies
    global baseEatRate
    global baseTravelRate
    global pace
    global meal
    city = Cities[currentCity]
    while city.distanceTo > 0:
        displayStatus()
        if pace == "normal":
            travelRateFactor = 1.0
        elif pace == "fast":
            travelRateFactor = 1.25
        elif pace == "grueling":
            travelRateFactor = 1.5

        if meal == "normal":
            eatRateFactor = 1.0
        elif meal == "small":
            eatRateFactor = .75
        elif meal == "skimpy":
            eatRateFactor = 0.5

        city.distanceTo -= baseTravelRate * travelRateFactor
        Supplies[0].amount -= baseEatRate * eatRateFactor * len(Characters)
        choice = raw_input("1. Continue\n2. Travel Options\n")
        if choice == "2":
            travelOptions()
    currentCity += 1

def travelOptions():
    clearScreen()
    global pace
    global meal
    print "Travel rate:"
    print "1. Normal pace"
    print "2. Fast pace"
    print "3. Grueling pace\n"
    print "Meal amount:"
    print "4. Normal meal"
    print "5. Small meal"
    print "6. Skimpy meal\n"
    print "7. Done"
    choice = input("What would you like to do?: ")
    if choice == 1:
        pace = "normal"
    elif choice == 2:
        pace = "fast"
    elif choice == 3:
        pace = "grueling"
    elif choice == 4:
        meal = "normal"
    elif choice == 5:
        meal = "small"
    elif choice == 6:
        meal = "skimpy"
    elif choice == 7:
        return
    travelOptions()

Characters = []
# Characters[0] = Main character

# Each supply is constructed with its name, followed by the number that can be scavenged per hour
Supplies = []
# Each supply has a name, and the number of remaining units

# Supplies[0] = Food
# Supplies[1] = Ammunition
# Supplies[2] = Spare Parts
# Supplies[3] = Fuel
# Supplies[4] = Monies
# Supplies[5] = Meds

Cities = []
# Each city has a name, distance to next city

Events = []

# Each Event has a name, probibility, and factors that effect the game


##### VARIABLES TO PARSE #####

startScreen = (
"                    DYSENTERY TRAIL                    \n"
"In the year 20XX, the world succumbed to its poor diet.\n"
"   Will you and your group of survivors last in their  \n"
"                  journey for a cure?                  \n" )


# Units that are travelled per travel cycle
baseTravelRate = 100
pace = "normal" # NOT PARSEABLE

# Units eaten per travel cycle
baseEatRate = 20
meal = "normal" # NOT PARSEABLE

hoursToScavenge = 24

numCharacters = 3

currentCity = 0

diseaseName = "dysentery"

distanceUnit = "miles"

# All of the supply types: first arg is name, second is number gatherable per hour
Supplies.append(Supply("Food", 100))
Supplies.append(Supply("Ammunition", 100))
Supplies.append(Supply("Spare Parts", 100))
Supplies.append(Supply("Fuel", 100))
Supplies.append(Supply("Money", 100))
Supplies.append(Supply("Medicine", 100))

# All of the cities: first arg is name, second is number of distance units to it
Cities.append(City("Tokyo", 350.0))
Cities.append(City("New York", 350.0))
Cities.append(City("Toronto", 450.0))
Cities.append(City("Vienna", 400.0))
Cities.append(City("Richmond", 250.0))
Cities.append(City("San Fransisco", 500.0))
Cities.append(City("Tenochtitlan", 450.0))
Cities.append(City("Redmond", 400.0))
Cities.append(City("Troy", 150.0))
Cities.append(City("Gary", 550.0))

nameOfObstacle = "Dysentery"
obstacleStatus = "Calm"
# Obstacle to pass (I.E. the river, or zambies)
# Status holds the difficulty of passing

##########################


##### GAME EXECUTION STARTS #####

clearScreen()
print startScreen

raw_input("Press Enter to Continue...")
clearScreen()

# Input Character Names

charName = raw_input("What is your main character's name?: ")
char = Character(charName)
Characters.append(char)
for i in range(2, numCharacters+1):
    clearScreen()
    print "Character " + str(i) + ":"
    charName = raw_input("What is this character's name?: ")
    char = Character(charName)
    Characters.append(char)


# Scavenge Time

while True:
    clearScreen()
    print "You have " + str(hoursToScavenge) + " hours to scavenge for supplies:"
    for i, supply in enumerate(Supplies):
        print str(i+1) + ". Scavenge for " + supply.name + ": " + str(supply.amount)
    print str(i+2) + ". Go on Adventure\n"
    keyPressed = input("What do you want to do?: ") - 1
    if keyPressed == i+1:
        if hoursToScavenge >= 0:
            break
        else:
            clearScreen()
            print "You have spent to many hours scavenging"
            raw_input("Please make sure that your number of hours left is >= 0")
    elif keyPressed >= 0 and keyPressed <= i:
        clearScreen()
        print "You have " + str(hoursToScavenge) + " hours to scavenge\n"
        supplyName = Supplies[keyPressed].name
        rate = Supplies[keyPressed].rate
        print "You can scavenge " + supplyName + " at a rate of " + str(rate) + " per hour"
        hours = input ("How many hours will you spend scavenging " + supplyName + "?: ")
        hoursBefore = Supplies[keyPressed].amount / Supplies[keyPressed].rate
        hoursToScavenge -= (hours - hoursBefore)
        Supplies[keyPressed].amount = Supplies[keyPressed].rate * hours
    else:
        clearScreen()
        raw_input("Please input a valid response...")

# Begin Adventure

while currentCity < len(Cities):
    travelLoop()

clearScreen()

print "GAME OVER"
