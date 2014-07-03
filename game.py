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
    mainScreen = screens.Menu(surface)
    loginScreen = screens.Login(surface)
    worldScreen = screens.World(surface)
    battleScreen = screens.Battle(surface)

    while True:
        while pers.name == '':
            loaded = False
            if mainScreen.loop() == 'login':
                pers.name = loginScreen.loop()

        if not loaded:
            if os.path.isfile('Saves/' + pers.name):
                pers = pers.load()
            else:
                if not os.path.isdir('Saves'):
                    os.mkdir('Saves')
                pers = pers.save()
            loaded = True

        worldScreen.update(pers)
        place, mobs = worldScreen.loop()
        if place != None:
            pers.place = place
        else:
            pers.place = place
        #Need try - because mobs could even not exist
        try:
            if random.randrange(0, 100) < PLACE['Mobs']['Chance']:
                pers = battleScreen.loop(PLACE['Mobs']['Chance'], pers)
        except:
            pass
        pers.save()

if __name__ == '__main__':
    pg.display.set_caption(CAPTION)
    screen = pg.display.set_mode(SIZE)
    gameLoop(screen)
    pg.quit()
