#!/usr/bin/python

from GameObjects import *
import os
import random

##### VARIOUS FUNCTIONS #####
def handleEvent(event):
    clearScreen()
    dontInclude = []
    toPrint = event.description + "\n" + "Do you...\n"
    for i, option in enumerate(event.options):
        canDo=True
        for goodAtt, badAtt, goodAmt, badAmt in zip(event.goodEffects.attribute,event.badEffects.attribute, event.goodEffects.amount, event.badEffects.amount):
            for j, att in enumerate("food","ammunition","money","meds"):
                if goodAtt == att and goodAmt + Supplies[j] < 0:
                    canDo=False
                elif badAtt == att and badAmt + Supllies[j] < 0:
                    canDo=False
        if canDo:
            toPrint += str(i+1)+": "+event.options + "\n"
        else:
            dontInclude.append(i+1)
            toPrint += str(i+1)+": Cannot choose, not enough supplies.\n"

    choice = getNumber(toPrint + "Enter your choice: ",1,i+1, dontInclude) -1
    x = random.randint(1,100)
    if x <= enumerate(Characters)*event.chances(choice):
        castEffect(event.goodEffects(choice))
    else:
        castEffect(event.badEffects(choice))

def castEffect(effect):
    for att, amt in zip(effect.attribute,effect.amount):
        supplyEffected=False
        for j, checkAtt in enumerate("food","ammunition","money","meds"):
            if att == checkAtt:
                Supplies[j]+=amt
                supplyEffected=True
        if att == "health":
            if amt > 0:
                notFullChars = [character for character in Characters if character.health != 100]
                char = random.choice(notFullChars)
            else:
                char = random.choice(Characters)
            char.health+=amt
        elif att == "sick":
            if amt == 0:
                sickChars = [character for character in Characters if character.isSick]
                if len(sickChars)>0:
                    char = random.choice(sickChars)
                    char.isSick=False
            else:
                healthyChars = [character for character in Characters if not character.isSick]
                if len(healthyChars)>0:
                    char = random.choice(healthyChars)
                    char.isSick=True
        elif att == "nothing" or supplyEffect:
            pass
        else:
            print "ERROR: BAD DATA - fix your event attributes"
    print effect.message+"\n"

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

def clearScreen():
    os.system( [ 'clear', 'cls' ][ os.name == 'nt' ] )

def getStatus():
    global currentCity, distanceUnit, Supplies, diseaseName
    city = Cities[currentCity]

    string = "TRAVELLING\n\n" + "Heading to: " +  city.name + "\nDistance: " +  str(city.distanceTo) + " " + distanceUnit + "\n\n"
    string += "Pace of travel: " + pace[0] + "\nFood per meal: " + meal[0] + "\n\n"

    for supply in Supplies:
        string += supply.name + ": " + str(supply.amount) + " " + supply.unit + '\n'

    string += "\n"

    for character in Characters:
        string += character.name + ": \n"
        string += "- Health: " + str(character.health) + '\n'
        if character.isSick:
            string += "- Has " + diseaseName + '\n'
        string += "\n"
    return string

def travelLoop():
    global currentCity, Supplies, baseEatRate, Characters, baseTravelRate, pace, meal, win
    global mainCharacter, running, sickChance, healthForSickRoll, lostHealthSick, lostHealthNoMeal
    global lostHealthSmallMeal, lostHealthSkimpyMeal, lostHealthFastTravel, lostHealthGruelingTravel
    city = Cities[currentCity]

    # Loop until city is reached
    while city.distanceTo > 0:
        string = getStatus()
        string += "1. Continue\n2. Travel Options\nWhat will you do?: "
        choice = getNumber(string, 1, 2)
        if choice == 2:
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
    string =  "TRAVEL OPTIONS\n\nTravel rate: " + pace[0] + "\n1. Normal pace"
    string += "\n2. Fast pace\n3. Grueling pace\n\nMeal amount: " + meal[0]
    string += "\n4. Normal meal\n5. Small meal\n6. Skimpy meal\n\n7. Heal party member\n8. Done"
    string += "\n\nWhat would you like to do?: "
    choice = getNumber(string, 1, 8)
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
    string = "HEAL A PARTY MEMBER\n\nYou have: " + str(Supplies[3].amount) + " medicine\n\n"

    for i, character in enumerate(Characters):
        string += str(i+1) + ". Heal" + character.name + ": \n"
        string += "- Health: " + str(character.health) + '\n'
        if character.isSick:
            string += "- Has " + diseaseName + '\n'
        string += "\n"

    string += str(i+2) + ". Go Back\n\nWhat would you like to do?: "

    choice = getNumber(string, 1, len(Characters) + 1) - 1

    if choice >= 0 and choice < len(Characters):
        if Supplies[3].amount == 0:
            clearScreen()
            raw_input("You do not have enough medicine!")
            return
        Characters[choice].isSick = False
        Characters[choice].health += 25
        if Characters[choice].health > 100:
            Characters[choice].health = 100
        Supplies[3].amount -= 1
        healMember()
    elif choice == len(Characters):
        return
    else:
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

currentCity = 0 # NOT PARSEABLE

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
Supplies.append(Supply("Food", 125, "pounds"))
Supplies.append(Supply("Ammunition", 20, "rounds"))
Supplies.append(Supply("Money", 50, "dollars"))
Supplies.append(Supply("Medicine", 1, "medkits"))

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
    string = "You have " + str(hoursToScavenge) + " hours to scavenge for supplies:\n"
    for i, supply in enumerate(Supplies):
        string += str(i+1) + ". Scavenge for " + supply.name + ": " + str(supply.amount) + " " + supply.unit + '\n'
    string += str(i+2) + ". Go on Adventure\nWhat do you want to do?: "
    keyPressed = getNumber(string, 1, len(Supplies)+1) - 1
    if keyPressed == i+1:
        break
    else:
        clearScreen()
        supplyName = Supplies[keyPressed].name
        rate = Supplies[keyPressed].rate
        amount = Supplies[keyPressed].amount
        unit = Supplies[keyPressed].unit
        time = hoursToScavenge + amount / rate
        string = "You have " + str(time) + " hours to scavenge\n\n"
        string += "You can scavenge " + supplyName + " at a rate of " + str(rate) + " " + unit + " per houri\n"
        string += "How many hours will you spend scavenging " + supplyName + "?: "
        hours = getNumber(string, 0, time)
        hoursBefore = Supplies[keyPressed].amount / Supplies[keyPressed].rate
        hoursToScavenge -= (hours - hoursBefore)
        Supplies[keyPressed].amount = Supplies[keyPressed].rate * hours

# Begin Adventure

while running and currentCity < len(Cities):
    travelLoop()

clearScreen()

if win:
    print winScreen
else:
    print gameOver
