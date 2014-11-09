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
    #place = 'introduction'
    place = 'Forest/StumpOfDworaks'

    #History of viewed hints and intros
    hints = 'init'
    intros = 'init'

    #===== Characteristics =====
    #Speed of movement [mps, meters per stroke]: but 1 stroke = 1 minute of gametime, so you will benefit by moving faster not only in less-strokes way, but also in less-time-spent way
    speed = 5

    experience = 0
    gold = 0 #Money
    level = 1
    maxhp = 20
    maxhp = 200
    attack = 30

    #Dynamic characteristics
    hp = maxhp

    #The time (in minutes)
    time = 0

    #Statistics
    strokes = 0
    battleStrokes = 0

    #All kind of items, even money
    #Starts with _ -> _number_ where 'number' is number of items
    #Need to make somehow items attributes (.cost, .krit, .atk, .def...)
    items = [
        '_2_PocketKnife',
        '_10_Gold'
    ]

    #Temporary for equip slot
    shield = '0'
    sword = '0'

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
    def __init__(self, style = 'default'):
        self.maxhp = 100
        self.attack = 5
        self.name = 'Mysterious creature'
        self.speed = 100 #Added to self.act per tick, speed of monster
        self.experience = 5
        self.gold = 5

        self.act = 0 #Activity: when self.act = 10000, mob is attacking

        if style == 'Skeleton':
            self.maxhp = 100
            self.attack = 10
            self.name = 'Skeleton'
            self.speed = 100
            self.experience = 5
            self.gold = 5

        self.hp = self.maxhp

#class Quest():
#    def __init__():
#        pass
