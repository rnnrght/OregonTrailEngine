#!/usr/bin/python

from Character import *
import os

def clear():
    os.system( [ 'clear', 'cls' ][ os.name == 'nt' ] )


Characters = []
# Characters[0] = Main character

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

# Each Event has a name, problibility, and factors that effect the game

nameOfObstacle = "Dysentery"
obstacleStatus = "Calm"
# Obstacle to pass (I.E. the river, or zambies)
# Status holds the difficulty of passing

baseTravelRate = 100

travelRateFactor = 1.0

# Input Character Names

charName = raw_input("What is your main character's name?: ")
char = Character(charName)
Characters.append(char)
for i in range(2, 6):
    clear()
    print "Character " + str(i) + ":"
    charName = raw_input("What is this character's name?: ")
    char = Character(charName)
    Characters.append(char)

clear()


# Scavenge Time
