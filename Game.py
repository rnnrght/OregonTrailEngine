#!/usr/bin/python

from GameObjects import *
import os

def clearScreen():
    os.system( [ 'clear', 'cls' ][ os.name == 'nt' ] )


##### GAME VARIABLES #####

startScreen = (
"                    DYSENTERY TRAIL                    \n"
"In the year 20XX, the world succumbed to its poor diet.\n"
"   Will you and your group of survivors last in their  \n"
"                  journey for a cure?                  \n" )


baseTravelRate = 100
travelRateFactor = 1.0

baseEatRate = 50
eatRateFactor = 1.0

hoursToScavenge = 24

numCharacters = 5

nameOfObstacle = "Dysentery"
obstacleStatus = "Calm"
# Obstacle to pass (I.E. the river, or zambies)
# Status holds the difficulty of passing

##########################


Characters = []
# Characters[0] = Main character

# Each supply is constructed with its name, followed by the number that can be scavenged per hour
Supplies = []
Supplies.append(Supply("Food", 100))
Supplies.append(Supply("Ammunition", 100))
Supplies.append(Supply("Spare Parts", 100))
Supplies.append(Supply("Fuel", 100))
Supplies.append(Supply("Money", 100))
Supplies.append(Supply("Medicine", 100))
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

