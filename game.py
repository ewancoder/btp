#!/usr/bin/env python3

import os
import random

import pygame as pg
pg.mixer.pre_init(22050, -16, True, 512)
pg.init()

import classes
import screens

CAPTION = 'Big Typernatural Project'
SIZE = (1000, 700)

class Game():
    def loop(self, surface):
        #===== VARS =====
        pers = classes.Pers()
        started = False #Prevents multiple game loads

        #===== MAIN LOOP =====
        while True:
            #Create menu
            while pers.name == '':
                mainScreen = screens.Menu(surface).loop()
                #If mainScreen (menu) returned a value - create loginScreen
                if mainScreen == 'login':
                    #loginScreen
                    pers.name = screens.Login(surface).loop()

            #Load game or save new game, then started=True
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
            #Save each loop
            pers.save()

#===== MAIN PROGRAM =====
if __name__ == '__main__':
    pg.display.set_caption(CAPTION)
    screen = pg.display.set_mode(SIZE)
    Game().loop(screen)
    pg.quit()
