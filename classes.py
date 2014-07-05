#!/usr/bin/env python3

import pickle

class Pers():
    #If name is '' - show main menu screen
    name = ''
    #Unique ID of the place which is loaded by World class
    place = 'introIntroduction'

    #Characteristics
    experience = 0
    level = 1
    maxhp = 20

    #Dynamic characteristics
    hp = maxhp

    #The time (in minutes, +10 per turn)
    time = 0

    #Statistics
    strokes = 0

    #All kind of items, even money
    items = [
        '_2_PocketKnife',
        '_10_Gold'
    ]

    def save(self):
        with open('Saves/' + self.name, 'wb') as f:
            pickle.dump(self, f)
        print('Game saved as ' + self.name)
        return self

    def load(self):
        with open('Saves/' + self.name, 'rb') as f:
            self = pickle.load(f)
        print('Game loaded as ' + self.name)
        return self

class Mob():
    maxhp = 20
    hp = maxhp

#class Quest():
#    def __init__(name, description):
#        print('Class for quests')
