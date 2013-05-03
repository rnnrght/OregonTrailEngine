#!/usr/bin/python

from GameObjects import *
import os
import random
from Parser import *

##### VARIOUS FUNCTIONS #####
def handleEvent(event):
    clearScreen()
    dontInclude = []
    toPrint = "Supplies:\n"
    for supply in Supplies:
        toPrint += supply.name + ": " + str(supply.amount) + " " + supply.unit + '\n'

    toPrint += "\n"+event.description + "\nDo you...\n"
    i=0
    badSupplies = {}

    for i, option in enumerate(event.options):
        canDo=True
        for goodAtt, goodAmt in zip(event.goodEffects[i].attribute,event.goodEffects[i].amount):
            for k, att in enumerate(("food","ammunition","money","meds")):
                if goodAtt == att and goodAmt + Supplies[k].amount < 0:
                    canDo = False
                    badSupplies[Supplies[k].name] = True

        if canDo:
            toPrint += str(i+1)+": "+option + "\n"
        else:
            dontInclude.append(i+1)
            toPrint += str(i+1)+": Cannot choose, not enough "
            includeComma = False
            for supplyName in badSupplies:
                if includeComma:
                    toPrint += ", "
                includeComma = True
                toPrint += supplyName
            toPrint += "\n"

    choice = getNumber(toPrint + "Enter your choice: ", 1, i+1, dontInclude) - 1
    x = random.randint(1, 100)
    chance = 0.0
    for i in range(len(Characters)):
        chance+= (1-chance) * event.chances[choice] / 100.0
    if x <= chance * 100.0:
        castEffect(event.goodEffects[choice])
    else:
        castEffect(event.badEffects[choice])

def castEffect(effect):
    returnStuff = []
    doEvent=False
    for att, amt in zip(effect.attribute,effect.amount):
        supplyEffected=False
        for j, checkAtt in enumerate(("food", "ammunition", "money", "meds")):
            if att == checkAtt:
                Supplies[j].amount+=amt
                if amt>0:
                    returnStuff.append("Gained "+str(amt)+" "+checkAtt+".\n")
                else:
                    returnStuff.append("Lost "+str(amt*-1)+" "+checkAtt+".\n")
                if Supplies[j].amount<0:
                    Supplies[j].amount=0
                    returnStuff.append("Ran out of " + checkAtt + "!\n")
                supplyEffected=True
        if att in [event for event in Events]:
            doEvent=True
        else:
            if att == "health":
                if amt > 0:
                    notFullChars = [character for character in Characters if character.health != 100 and character.health>0]
                    char = random.choice(notFullChars)
                    returnStuff.append(char.name + " has gained " + str(amt) + " health.\n")
                else:
                    notDeadChars = [character for character in Characters if character.health >0]
                    char = random.choice(notDeadChars)
                    returnStuff.append(char.name + " has lost " + str(amt*-1) + " health.\n")
                char.health+=amt
            elif att == "sick":
                if amt == 0:
                    sickChars = [character for character in Characters if character.isSick]
                    if len(sickChars)>0:
                        char = random.choice(sickChars)
                        char.isSick=False
                        returnStuff.append(char.name + " has been cured!\n")
                else:
                    healthyChars = [character for character in Characters if not character.isSick]
                    if len(healthyChars)>0:
                        char = random.choice(healthyChars)
                        char.isSick=True
                        returnStuff.append(char.name + " has caught " + diseaseName + "!\n")
            elif att == "nothing" or supplyEffected:
                pass
            else:
                print "ERROR: BAD DATA - fix your event attributes"
        clearScreen()
    print effect.message
    print ''.join(returnStuff)
    raw_input()
    #check for chained/tree events
    if doEvent:
        handleEvent(Events[att])

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
    global currentCity, Supplies, baseEatRate, Characters, baseTravelRate, pace, meal, win, eventChance
    global mainCharacter, running, sickChance, healthForSickRoll, lostHealthSick, lostHealthNoMeal, datfiles
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

        # HANDLE EVENTS
        if city.distanceTo > 0:
            if random.randint(1,100) <= eventChance:
                clearScreen()
                raw_input("EVENT OCCURED!")
                event = datfiles.getTypeEvent("R")
                handleEvent(event)

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
    global Characters, Supplies
    clearScreen()
    string = "HEAL A PARTY MEMBER\n\nYou have: " + str(Supplies[3].amount) + ' ' + Supplies[3].unit + "\n\n"

    for i, character in enumerate(Characters):
        string += str(i+1) + ". Heal " + character.name + ": \n"
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

datfiles = Parser()

startScreen = datfiles.getMessage("startScreen")

gameOver = datfiles.getMessage("gameOver")

winScreen = datfiles.getMessage("winScreen")

# Units that are travelled per travel cycle
baseTravelRate = int(datfiles.get("baseTravelRate"))

# Units eaten per travel cycle
baseEatRate = int(datfiles.get("baseEatRate"))

hoursToScavenge = int(datfiles.get("hoursToScavenge"))

numCharacters = int(datfiles.get("numCharacters"))


sickChance = int(datfiles.get("sickChance"))
healthForSickRoll = int(datfiles.get("healthForSickRoll")) # Health below which characters can get sick
lostHealthSick = int(datfiles.get("lostHealthSick"))
lostHealthNoMeal = int(datfiles.get("lostHealthNoMeal"))
lostHealthSmallMeal = int(datfiles.get("lostHealthSmallMeal"))
lostHealthSkimpyMeal = int(datfiles.get("lostHealthSkimpyMeal"))
lostHealthFastTravel = int(datfiles.get("lostHealthFastTravel"))
lostHealthGruelingTravel = int(datfiles.get("lostHealthGruelingTravel"))
diseaseName = datfiles.get("diseaseName")

eventChance = int(datfiles.get("eventChance"))

distanceUnit = datfiles.get("distanceUnit")

foodName = datfiles.get("foodName")
ammunitionName = datfiles.get("ammunitionName")
moneyName = datfiles.get("moneyName")
medicineName = datfiles.get("medicineName")
foodRate = int(datfiles.get("foodRate"))
ammunitionRate = int(datfiles.get("ammunitionRate"))
moneyRate = int(datfiles.get("moneyRate"))
medicineRate = int(datfiles.get("medicineRate"))
foodUnit = datfiles.get("foodUnit")
ammunitionUnit = datfiles.get("ammunitionUnit")
moneyUnit = datfiles.get("moneyUnit")
medicineUnit = datfiles.get("medicineUnit")

# All of the supply types: first arg is name, second is number gatherable per hour
Supplies.append(Supply(foodName, foodRate, foodUnit))
Supplies.append(Supply(ammunitionName, ammunitionRate, ammunitionUnit))
Supplies.append(Supply(moneyName, moneyRate, moneyUnit))
Supplies.append(Supply(medicineName, medicineRate, medicineUnit))

Cities = datfiles.getCities()
Events = datfiles.getEventDefs()
meal = ("normal", 1.0) # NOT PARSEABLE
pace = ("normal", 1.0) # NOT PARSEABLE
running = True # NOT PARSEABLE
currentCity = 0 # NOT PARSEABLE
win = True # NOT PARSEABLE

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
        string += "You can scavenge " + supplyName + " at a rate of " + str(rate) + " " + unit + " per hour\n"
        string += "How many hours will you spend scavenging " + supplyName + "?: "
        hours = getNumber(string, 0, time)
        hoursBefore = Supplies[keyPressed].amount / Supplies[keyPressed].rate
        hoursToScavenge -= (hours - hoursBefore)
        Supplies[keyPressed].amount = Supplies[keyPressed].rate * hours

# Begin Adventure

while running and currentCity < len(Cities):
    travelLoop()

    # City event
    if currentCity != len(Cities):
        pass

clearScreen()

if win:
    print winScreen
else:
    print gameOver
