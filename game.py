#!/usr/bin/env python3

import screens

import os
import pickle
import random

import pygame as pg
pg.mixer.pre_init(22050, -16, True, 512)
pg.init()

#===== CONSTANTS =====
CAPTION = 'Big Typernatural Project'    #: Main window caption
SIZE = (1000, 700)                      #: Size of main window (should be at least the size of images in Images folder

#===== CLASSES =====
class Mob():
    """Creates new monster which to fight you"""

    maxhp = 20  #: Sets within __init__ method, max hitpoints
    hp = maxhp

    def __init__(self, maxhp):
        """Sets maxhp"""
        self.maxhp = maxhp

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

class Game():
    def loop(self, surface):
        """Main function loop of the game, which loops while true
        
        :param surface: A surface on which all will be drawing
        :var pers: main Pers() object
        """

        #===== VARIABLES =====
        pers = Pers()
        started = False #: Prevent multiple game loads + game quit to menu trigger

        #===== MAIN LOOP =====
        while True:
            #: Create menu
            while pers.name == '':
                login = screens.Menu().main(surface)
                #: Create loginscreen
                if login:
                    pers.name = screens.Login().main(surface)

            #: Load game of save new game, then started=True
            if not started:
                if os.path.isfile('Saves/' + pers.name):
                    pers.load()
                else:
                    pers.save()
                    screens.Introduction().main(surface, pers.name)
                started = True
            (pers.place, mobs) = screens.World().main(surface, pers.place)
            if random.randrange(0, 100) < mobs['Chance']:
                pers = screens.Battle().main(surface, mobs, pers, Mob())
            #: Save each loop
            pers.save()

#===== MAIN PROGRAM =====
if __name__ == '__main__':
    pg.display.set_caption(CAPTION)
    screen = pg.display.set_mode(SIZE)
    Game().loop(screen)
    pg.quit()
