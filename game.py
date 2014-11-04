#!/usr/bin/env python3
#BTP, Ewancoder, 2014

import os
import random

import pygame as pg
pg.mixer.pre_init(44100, -16, 2, 2048)
pg.init()

import classes
import screens

CAPTION = 'Big Typernatural Project'
SIZE = (1000, 700)

def gameLoop(surface):
    settings = classes.Settings()
    try:
        settings = settings.load()
    except:
        pass

    pers = classes.Pers()
    menuScreen = screens.Menu(surface)
    loginScreen = screens.Login(surface)
    worldScreen = screens.World(surface)

    while True:
        while pers.name == '':
            loaded = False
            menu = menuScreen.loop(settings)
            if menu == 'login':
                pers.name = loginScreen.loop()
            else:
                setattr(settings, menu, not getattr(settings, menu))
                settings = settings.save()

        if not loaded:
            if os.path.isfile('Saves/' + pers.name):
                pers = pers.load()
            else:
                if not os.path.isdir('Saves'):
                    os.mkdir('Saves')
                pers = pers.save()
            loaded = True

        worldScreen.update(pers) #Load whole world current environment based on "pers"
        worldScreen.loop(settings)

if __name__ == '__main__':
    pg.display.set_caption(CAPTION)
    screen = pg.display.set_mode(SIZE)
    gameLoop(screen)
    pg.quit()
