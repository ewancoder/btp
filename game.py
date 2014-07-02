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

def gameLoop(surface):
    pers = classes.Pers()
    worldScreen = screens.World(surface)

    while True:
        while pers.name == '':
            loaded = False
            mainScreen = screens.Menu(surface).loop()
            if mainScreen == 'login':
                pers.name = screens.Login(surface).loop()

        if not loaded:
            if os.path.isfile('Saves/' + pers.name):
                pers.load()
            else:
                if not os.path.isdir('Saves'):
                    os.mkdir('Saves')
                pers.save()
            loaded = True

        worldScreen.update(pers)
        (place, mobs) = worldScreen.loop()
        if place != 0:
            pers.place = place
        #Need try - because mobs could even not exist
        try:
            if random.randrange(0, 100) < mobs['Chance']:
                pers = screens.Battle().loop(surface, mobs, pers)
        except:
            pass
        pers.save()

if __name__ == '__main__':
    pg.display.set_caption(CAPTION)
    screen = pg.display.set_mode(SIZE)
    gameLoop(screen)
    pg.quit()
