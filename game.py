#!/usr/bin/env python3

import os
import pickle
import random

import pygame as pg
pg.mixer.pre_init(22050, -16, True, 512)
pg.init()

import screens

#===== CONSTANTS =====
CAPTION = 'Big Typernatural Project'
SIZE = (1000, 700)

#===== CLASSES =====
#class Mob():
#    maxhp = 20
#    hp = maxhp

#class Quest():
#    print('Class for quests and tasks and notes')

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

class Game():
    def loop(self, surface):
        """Main function loop of the game, which loops while true"""

        #===== VARIABLES =====
        pers = Pers()
        started = False #: Prevent multiple game loads + game quit to menu trigger

        #===== MAIN LOOP =====
        while True:
            #: Create menu
            while pers.name == '':
                mainScreen = screens.Menu(surface).loop()
                #: If login (menu) returned a value - create loginscreen
                if mainScreen == 'login':
                    #loginScreen
                    pers.name = screens.Login(surface).loop()

            #: Load game or save new game, then started=True
            if not started:
                if os.path.isfile('Saves/' + pers.name):
                    pers.load()
                else:
                    pers.save()
                    screens.Introduction().loop(surface, pers.name)
                started = True
            (pers.place, mobs) = screens.World().loop(surface, pers.place)
            if random.randrange(0, 100) < mobs['Chance']:
                pers = screens.Battle().loop(surface, mobs, pers, Mob())
            #: Save each loop
            pers.save()

#===== MAIN PROGRAM =====
if __name__ == '__main__':
    pg.display.set_caption(CAPTION)
    screen = pg.display.set_mode(SIZE)
    Game().loop(screen)
    pg.quit()
