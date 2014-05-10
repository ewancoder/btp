#!/usr/bin/env python3
"""
Main game module uses :mod:`screens` module to wrap around all interfaces.

Imports
-------

    :mod:`screens` - handles all interfaces

    :mod:`os` - need for checking file existence (not really pythonic way)

    :mod:`pickle` - need for easy save/load :class:`game.Pers` class

    :mod:`random` - need for calculating mobs attack chance

    :mod:`pygame` - main module for the game
"""

import screens

import os #For checking file existence
import pickle
import random

import pygame as pg
pg.mixer.pre_init(22050, -16, True, 512)
pg.init()

#========== CONSTANTS ==========
CAPTION = 'Big Typernatural Project'
SIZE = (1000, 700)

#========== CLASSES ==========
class Mob():
    name = 'Skeleton' #: Just variable

class Quest():
    print('Class for quests and tasks and notes')

class Pers():
    name = ''   #: Player's name - just for saving and loading without passing arguments
    place = 'OldManHouse'   #: Current place
    maxhp = 20              #: Max hitpoints
    hp = maxhp              #: Current hitpoints

    def save(self):
        """Saves player to file"""
        with open('Saves/' + self.name, 'wb') as f:
            pickle.dump(self, f)
            print('Game saved as ' + self.name)

    def load(self):
        """Load player from file"""
        with open('Saves/' + self.name, 'rb') as f:
            self = pickle.load(f)
            print('Game loaded as ' + self.name)

class Game():
    name = '' #: lol

    def loop(self, surface):
        """Main function of the game"""

        #===== VARIABLES =====
        name = ''       #: Name of current pers
        pers = Pers()   #: Main pers object
        started = False #: If savegame is loaded/created, do not load it twice+

        #===== MAIN LOOP =====
        while True:
            #Menu / login screen
            while pers.name == '':
                login = screens.Menu().main(surface)
                if login:
                    pers.name = screens.Login().main(surface)

            #Save / load game + run introduction
            if not started:
                if os.path.isfile('Saves/' + pers.name):
                    pers.load()
                else:
                    pers.save()
                    screens.Introduction().main(surface, pers.name)
                started = True  #: Prevent multiple game loading
            #: Load map at current state
            (pers.place, mobs) = screens.Map().main(surface, pers.place)
            #Load battle if attacked
            if random.randrange(0, 100) < mobs['Chance']:
                pers = screens.Battle.main(surface, mobs, pers, Mob())
            #If anything else for screens -> Screens().anythingelse()
            #Check_upon_death + check_upon_new_level + everything else (Pers.update?)
            #: Save game with each iteration (each screen + after battle)
            pers.save()

#========== MAIN PROGRAM ==========
if __name__ == '__main__':
    pg.display.set_caption(CAPTION)
    screen = pg.display.set_mode(SIZE)
    Game().loop(screen)
    pg.quit()
