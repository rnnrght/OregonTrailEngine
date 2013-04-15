#!/usr/bin/python

FILENAME = "game.dat"

gameinfo = []

for line in FILENAME.open():
    gameinfo.append(line)
FILENAME.close()
