#!/usr/bin/python

from GameObjects import *
import sys
import os
import random
from Parser import *

##### VARIOUS FUNCTIONS #####
def handleEvent(event):
    clearScreen()
    dontInclude = [] #index for options the player cannot choose
    #display supplies before event
    toPrint = "Supplies:\n"
    for supply in Supplies:
        toPrint += supply.name + ": " + str(supply.amount) + " " + supply.unit + '\n'

    toPrint += "\n"+event.description + "\nDo you...\n"
    i=0
    badSupplies = {}

    #iterate through all options and filter based on if possible
    for i, option in enumerate(event.options):
        canDo=True
        for goodAtt, goodAmt in zip(event.goodEffects[i].attribute,event.goodEffects[i].amount):
            for k, att in enumerate(("food","ammunition","money","meds")):
                #check if player has enough supplies to do the good effect
                #ie: ammo cost, money cost, etc
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
    #chance increases based on how many people are alive
    #if chance is 60%, first alive gets 60, next alive get 60% of the remain 40, and so on
    for i in range(len(Characters)):
        chance+= (1-chance) * event.chances[choice] / 100.0
    #if they succesful did the event (pass chance roll)
    if x <= chance * 100.0:
        castEffect(event.goodEffects[choice])
    else:#failed the chance roll
        castEffect(event.badEffects[choice])

def castEffect(effect):
    returnStuff = []
    doEvent=False
    for att, amt in zip(effect.attribute,effect.amount):
        supplyEffected=False
        #check for changes against the base 3 supplies and has error check for going negative
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
        #for tree events, att will equal the key of another event
        if att in [event for event in Events]:
            doEvent=True
        else:
            if att == "health":
                if amt > 0:
                    #dont heal full or recently killed character
                    notFullChars = [character for character in Characters if character.health != 100 and character.health>0]
                    if len(notFullChars)>0:
                        char = random.choice(notFullChars)#randomly heal a valid character
                        returnStuff.append(char.name + " has gained " + str(amt) + " health.\n")
                        char.health+=amt
                        if char.health>100:#dont go over 100 health
                            char.health=100
                else:
                    notDeadChars = [character for character in Characters if character.health >0]
                    if len(notDeadChars)> 0:
                        char = random.choice(notDeadChars)#random hurt and alive character
                        returnStuff.append(char.name + " has lost " + str(amt*-1) + " health.\n")
                        char.health+=amt
            elif att == "sick":
                if amt == 0:
                    sickChars = [character for character in Characters if character.isSick]
                    if len(sickChars)>0:
                        char = random.choice(sickChars)#only cure sick
                        char.isSick=False
                        returnStuff.append(char.name + " has been cured!\n")
                else:
                    healthyChars = [character for character in Characters if not character.isSick]
                    if len(healthyChars)>0:
                        char = random.choice(healthyChars)#only make healthy sick
                        char.isSick=True
                        returnStuff.append(char.name + " has caught " + diseaseName + "!\n")
            elif att == "nothing" or supplyEffected:
                pass
            else:#debugging message
                print "ERROR: BAD DATA - fix your event attributes"
        clearScreen()
    print effect.message
    raw_input(''.join(returnStuff))
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

def confirmExit():
    clearScreen()
    while 1:
        choice = raw_input("Are you sure you would like to leave? (y/n): ")
        if choice == 'y':
            clearScreen()
            print "Thank you for playing"
            sys.exit(0)
        elif choice == 'n':
            return
        else:
            clearScreen()
            print "ERROR: input a valid option\n"

def travelLoop():
    global currentCity, Supplies, baseEatRate, Characters, baseTravelRate, pace, meal, win, eventChance
    global mainCharacter, running, sickChance, healthForSickRoll, lostHealthSick, lostHealthNoMeal, datfiles
    global lostHealthSmallMeal, lostHealthSkimpyMeal, lostHealthFastTravel, lostHealthGruelingTravel
    city = Cities[currentCity]

    # Loop until city is reached
    while city.distanceTo > 0:
        string = getStatus()
        string += "1. Continue\n2. Travel Options\n3. Exit game\nWhat will you do?: "
        choice = getNumber(string, 1, 3)
        if choice == 2:
            travelOptions()
            continue
        elif choice == 3:
            confirmExit()
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
                raw_input(Characters[i].name + " has died!")
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
    global Characters, Supplies, healthPerHeal, chanceToCure, chanceToHeal
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
            raw_input("You do not have enough " + Supplies[3].unit + "!")
            return

        if Characters[choice].isSick:
            if random.randint(1,100) <= chanceToCure:
                Characters[choice].isSick = False
            else:
                clearScreen()
                raw_input("Heal failure!")
        else:
            if random.randint(1,100) <= chanceToHeal:
                Characters[choice].health += 25
            else:
                clearScreen()
                raw_input("Heal failure!")
        if Characters[choice].health > 100:
            Characters[choice].health = 100
        Supplies[3].amount -= 1
        healMember()
    elif choice == len(Characters):
        return
    else:
        healMember()

##### PROGRAM EXECUTION STARTS #####

printString = "Which Game would you like to play?"
i = 0
new = False
dirList = os.listdir("gameData")

for i, direc in enumerate(dirList):
	printString += "\n\t" + str(i+1) + ": " + direc

printString += "\nWhat would you like to do: "
choice = getNumber(printString, 1, i+1) - 1

path = "gameData/" + dirList[choice]

###### GAME VARIABLES #####

meal = ("normal", 1.0)
pace = ("normal", 1.0)
running = True
currentCity = 0
win = True
Supplies = []
Characters = []

##### VARIABLES TO PARSE #####

datfiles = Parser(path)
startScreen = datfiles.getMessage("startScreen")
gameOver = datfiles.getMessage("gameOver")
winScreen = datfiles.getMessage("winScreen")
baseTravelRate = int(datfiles.get("baseTravelRate"))
baseEatRate = int(datfiles.get("baseEatRate"))
hoursToScavenge = int(datfiles.get("hoursToScavenge"))
numCharacters = int(datfiles.get("numCharacters"))
chanceToCure = int(datfiles.get("chanceToCure"))
chanceToHeal = int(datfiles.get("chanceToHeal"))
healthPerHeal = int(datfiles.get("healthPerHeal"))
sickChance = int(datfiles.get("sickChance"))
healthForSickRoll = int(datfiles.get("healthForSickRoll"))
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
Cities = datfiles.getCities()
Events = datfiles.getEventDefs()
Supplies.append(Supply(foodName, foodRate, foodUnit))
Supplies.append(Supply(ammunitionName, ammunitionRate, ammunitionUnit))
Supplies.append(Supply(moneyName, moneyRate, moneyUnit))
Supplies.append(Supply(medicineName, medicineRate, medicineUnit))

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
    if running and currentCity != len(Cities):
        clearScreen()
        raw_input("You have arrived at "+Cities[currentCity-1].name+".\n"+ str(Cities[currentCity].distanceTo)+" "+distanceUnit+" to "+Cities[currentCity].name+".")
        event = datfiles.getTypeEvent("C")
        handleEvent(event)

clearScreen()

if win:
    print winScreen
else:
    print gameOver
