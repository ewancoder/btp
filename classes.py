#!/usr/bin/env python3

import pickle

class Mob():
    maxhp = 20
    hp = maxhp

class Quest():
    print('Class for quests and tasks and notes')

class Pers():
    name = ''
    place = 'OldManHouse'
    maxhp = 20
    hp = maxhp

    def save(self):
        """Saves self Pers() object to file"""
        with open('Saves/' + self.name, 'wb') as f:
            pickle.dump(self, f)
            print('Game saved as ' + self.name)

    def load(self):
        """Load self Pers() object from file"""
        with open('Saves/' + self.name, 'rb') as f:
            self = pickle.load(f)
            print('Game loaded as ' + self.name)
