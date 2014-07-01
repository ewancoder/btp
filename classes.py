#!/usr/bin/env python3

import pickle

class Pers():
    #If name is '' - show main menu screen
    name = ''
    #Unique ID of the place which is loaded by World class
    place = 'introbegin'

    #Characteristics
    experience = 0
    level = 1
    maxhp = 20

    #Dynamic characteristics
    hp = maxhp

    #Statistics
    strokes = 0

    def save(self):
        with open('Saves/' + self.name, 'wb') as f:
            pickle.dump(self, f)
            print('Game saved as ' + self.name)

    def load(self):
        with open('Saves/' + self.name, 'rb') as f:
            self = pickle.load(f)
            print('Game loaded as ' + self.name)

#class Mob():
#    maxhp = 20
#    hp = maxhp

#class Quest():
#    def __init__(name, description):
#        print('Class for quests')
