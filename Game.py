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

while hoursToScavenge != 0:
    for supply in Supplies:

        hours = hoursToScavenge+1
        while hours > hoursToScavenge:
            clearScreen()
            print "You have " + str(hoursToScavenge) + " hours to scavenge for supplies\n"
            print "You can scavenge " + str(supply.rate) + " " + supply.name + " per hour"
            hours = input("How many hours will you scavenge for " + supply.name + "?: ")
        hoursToScavenge -= hours
        supply.amount += supply.rate * hours
        if hoursToScavenge == 0:
            break


# Begin Adventure
