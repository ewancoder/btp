#!/usr/bin/env python3

import pickle

class Settings():
    hints = True

    def save(self):
        with open('settings', 'wb') as f:
            pickle.dump(self, f)
        print('Settings saved')
        return(self)

    def load(self):
        with open('settings', 'rb') as f:
            self = pickle.load(f)
        print('Settings loaded')
        return(self)

class Pers():
    #If name is '' - show main menu screen
    name = ''
    #Unique ID of the place which is loaded by World class
    #If starts with 'intro' - load place[5:][0...len(place[5:])] consecutively just as a slideshow
    place = 'introduction'

    #Characteristics
    experience = 0
    level = 1
    maxhp = 20
    maxhp = 200
    atk = 30

    #Speed of movement
    speed = 5

    #Dynamic characteristics
    hp = maxhp

    #The time (in minutes, +10 per turn)
    time = 0

    #Statistics
    strokes = 0

    #All kind of items, even money
    #Starts with _ -> _number_ where 'number' is number of items
    #Need to make somehow items attributes (.cost, .krit, .atk, .def...)
    items = [
        '_2_PocketKnife',
        '_10_Gold'
    ]

    #History of viewed hints
    hints = 'init'

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
    def __init__(self, maxhp = 200, atk = 1):
        self.maxhp = maxhp
        self.hp = maxhp
        self.atk = atk
        self.name = 'Mysterious creature'

class Skeleton(Mob):
    def __init(self):
        self.name = 'Skeleton'

#class Quest():
#    def __init__():
#        pass
