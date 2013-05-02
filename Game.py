#!/usr/bin/python

from GameObjects import *
import os
import random

##### VARIOUS FUNCTIONS #####

def clearScreen():
    os.system( [ 'clear', 'cls' ][ os.name == 'nt' ] )

def displayStatus():
    clearScreen()
    global currentCity, distanceUnit, Supplies, diseaseName
    city = Cities[currentCity]

    print "TRAVELLING\n"
    print "Heading to: " +  city.name
    print "Distance: " +  str(city.distanceTo) + " " + distanceUnit + "\n"
    print "Pace of travel: " + pace[0]
    print "Food per meal: " + meal[0] + "\n"

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
    global currentCity, Supplies, baseEatRate, Characters, baseTravelRate, pace, meal, win
    global mainCharacter, running, sickChance, healthForSickRoll, lostHealthSick, lostHealthNoMeal
    global lostHealthSmallMeal, lostHealthSkimpyMeal, lostHealthFastTravel, lostHealthGruelingTravel
    city = Cities[currentCity]

    # Loop until city is reached
    while city.distanceTo > 0:
        displayStatus()
        choice = raw_input("1. Continue\n2. Travel Options\n")
        if choice == "2":
            travelOptions()
            continue

        if pace[0] == "fast":
            for character in Characters:
                character.health -= lostHealthFastTravel
        elif pace[0] == "grueling":
            for character in Characters:
                character.health -= lostHealthGruelingTravel

        # Travel a little to the city
        city.distanceTo -= baseTravelRate * pace[1]

        # Eat the supplies, or subtract health
        if Supplies[0].amount != 0:
            if meal[0] == "small":
                for character in Characters:
                    character.health -= lostHealthSmallMeal
            elif meal[0] == "skimpy":
                for character in Characters:
                    character.health -= lostHealthSkimpyMeal
            Supplies[0].amount -= baseEatRate * meal[1] * len(Characters)
        else:
            for character in Characters:
                character.health -= lostHealthNoMeal
        if Supplies[0].amount < 0:
            Supplies[0].amount = 0

        # Handle sick character, and perfom sickness rolls
        for character in Characters:
            if character.isSick:
                character.health -= lostHealthSick
            elif character.health < healthForSickRoll:
                if random.randint(1,100) <= sickChance:
                    character.isSick = True
                    clearScreen()
                    raw_input(character.name + " has gotten sick!")

        # Check for character death
        i = 0
        while i < len(Characters):
            if Characters[i].health <= 0:
                clearScreen()
                raw_input(Characters[i].name + "has died!")
                Characters.pop(i)
                i -= 1
            i += 1

        # If main character died, game over
        if len(Characters) == 0 or Characters[0] != mainCharacter:
            running = False
            win = False
            return

    currentCity += 1

def travelOptions():
    clearScreen()
    global pace, meal
    print "TRAVEL OPTIONS\n"
    print "Travel rate: " + pace[0]
    print "1. Normal pace"
    print "2. Fast pace"
    print "3. Grueling pace\n"
    print "Meal amount: " + meal[0]
    print "4. Normal meal"
    print "5. Small meal"
    print "6. Skimpy meal\n"
    print "7. Heal party member\n"
    print "8. Done"
    choice = input("What would you like to do?: ")
    if choice == 1:
        pace = ("normal", 1.0)
    elif choice == 2:
        pace = ("fast", 1.25)
    elif choice == 3:
        pace = ("grueling", 1.5)
    elif choice == 4:
        meal = ("normal", 1.0)
    elif choice == 5:
        meal = ("small", .75)
    elif choice == 6:
        meal = ("skimpy", 0.5)
    elif choice == 7:
        healMember()
    elif choice == 8:
        return
    travelOptions()

def healMember():
    global Characters
    global Supplies
    clearScreen()
    print "HEAL A PART MEMBER\n"
    print "You have: " + str(Supplies[3].amount) + " medicine\n"

    for i, character in enumerate(Characters):
        print str(i+1) + ". Heal" + character.name + ": "
        print "- Health: " + str(character.health)
        if character.isSick:
            print "- Has " + diseaseName
        print ""

    print str(i+2) + ". Go Back"

    choice = input("What would you like to do?: ") - 1
    if Supplies[3].amount == 0:
        clearScreen()
        raw_input("You do not have enough medicine!")
        choice = len(Characters)

    if choice >= 0 and choice < len(Characters):
        Characters[choice].isSick = False
        Characters[choice].health += 25
        if Characters[choice].health > 100:
            Characters[choice].health = 100
        Supplies[3].amount -= 1
        healMember()

Characters = []
# Characters[0] = Main character

# Each supply is constructed with its name, followed by the number that can be scavenged per hour
Supplies = []
# Each supply has a name, and the number of remaining units

# Supplies[0] = Food
# Supplies[1] = Ammunition
# Supplies[2] = Monies
# Supplies[3] = Meds

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

gameOver = (
"                       GAME OVER                       \n"
"Your entire crew now has a horrendous case of dysentery\n"
"                      Way to go...                     \n" )

winScreen = (
"                   CONGRATULATIONS                     \n"
"You have made it to your destination with great resolve\n"
"    You have escaped from the clutches of dysentery      " )

# Units that are travelled per travel cycle
baseTravelRate = 100
pace = ("normal", 1.0) # NOT PARSEABLE

# Units eaten per travel cycle
baseEatRate = 20
meal = ("normal", 1.0) # NOT PARSEABLE

hoursToScavenge = 24

numCharacters = 3

currentCity = 0

sickChance = 15
healthForSickRoll = 50 # Health below which characters can get sick
lostHealthSick = 5
lostHealthNoMeal = 5
lostHealthSmallMeal = 1
lostHealthSkimpyMeal = 3
lostHealthFastTravel = 1
lostHealthGruelingTravel = 3
diseaseName = "dysentery"

distanceUnit = "miles"

running = True # NOT PARSEABLE

win = True # NOT PARSEABLE

# All of the supply types: first arg is name, second is number gatherable per hour
Supplies.append(Supply("Food", 125))
Supplies.append(Supply("Ammunition", 20))
Supplies.append(Supply("Money", 50))
Supplies.append(Supply("Medicine", 1))

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
mainCharacter = Character(charName)
Characters.append(mainCharacter)
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

while running and currentCity < len(Cities):
    travelLoop()

clearScreen()

if win:
    print winScreen
else:
    print gameOver
