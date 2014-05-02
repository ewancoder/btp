#!/usr/bin/env python3
#I am aiming to write this code both in python3 and python2 for learning sake (python2 for wide people range, python3 for future and coolness)
"""
    Copyright (c) 2014 EwanCoder <ewancoder@gmail.com> GPL

    This game blends these independent concepts:
        1. Supernatural world, based on CW Supernatural Show
        2. Text-based rpg quest game
        3. Type game - the faster you type, the more you gain
"""

from screens import Screens

import os #For checking file existence
import pickle #For save/load gamedata
import random

import pygame as pg
pg.mixer.pre_init(22050, -16, True, 512)
pg.init()

#========== CONSTANTS ==========
CAPTION = 'Big Typernatural Project'
SIZE = (1000, 700)

#========== CLASSES ==========
class Mob():
    name = 'Skeleton'

class Quest():
    print('Class for quests and tasks and notes')

class Pers():
    name = ''   #Player's name - just for saving and loading without passing arguments
    place = 'OldManHouse'   #Current place
    maxhp = 20              #Max hitpoints
    hp = maxhp              #Current hitpoints

    def save(self):
        with open('Saves/' + self.name, 'wb') as f:
            pickle.dump(self, f)
            print('Game saved as ' + self.name)

    def load(self):
        with open('Saves/' + self.name, 'rb') as f:
            self = pickle.load(f)
            print('Game loaded as ' + self.name)

class Game():
    """Game logics handling"""

    def loop(self, surface):

        #===== VARIABLES =====
        name = ''       #Name of current pers
        pers = Pers()   #Main pers object
        started = False #If savegame is loaded/created, do not load it twice+

        #===== MAIN LOOP =====
        while True:
            #Menu / login screen
            while pers.name == '':
                option = Screens().menu(surface)
                #if option == 1:    #Future-way to handle multiple options
                if option:
                    pers.name = Screens().login(surface)
            #Save / load game + run introduction
            if not started:
                if os.path.isfile('Saves/' + pers.name):
                    pers.load()
                else:
                    pers.save()
                    Screens().introduction(surface, pers.name)
                started = True  #Prevent multiple game loading
            #Load map at current state
            (pers.place, mobs) = Screens().map(surface, pers.place)
            #Load battle if attacked
            if random.randrange(0, 100) < mobs['Chance']:
                pers = Screens().battle(surface, mobs, pers, Mob())
            #If anything else for screens -> Screens().anythingelse()
            #Check_upon_death + check_upon_new_level + everything else (Pers.update?)
            #Save game with each iteration (each screen + after battle)
            self.save()

#========== MAIN PROGRAM ==========
if __name__ == '__main__':
    pg.display.set_caption(CAPTION)
    screen = pg.display.set_mode(SIZE)
    Game().loop(screen)
    pg.quit()
