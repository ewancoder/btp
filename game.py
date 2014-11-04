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
SIZE = (1366, 768)

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

    name = '' #Actual name of a player (not pers.name because we need to clean mess after reloading to another pers)
    oldname = '' #for saving pers state meanwhile in menu

    while True:
        while name == '':
            loaded = False
            menu = menuScreen.loop(settings, oldname)
            if menu == 'login':
                name = loginScreen.loop()
            elif menu == 'back_' + oldname:
                name = oldname
                loaded = True
            else:
                setattr(settings, menu, not getattr(settings, menu))
                settings = settings.save()

        if not loaded:
            pers = classes.Pers()
            pers.name = name
            if os.path.isfile('Saves/' + pers.name):
                pers = pers.load()
                print(pers.hints)
            else:
                if not os.path.isdir('Saves'):
                    os.mkdir('Saves')
                pers = pers.save()
            loaded = True

        worldScreen.update(pers) #Load whole world current environment based on "pers"
        worldScreen.loop(settings)
        oldname = name
        name = ''

if __name__ == '__main__':
    pg.display.set_caption(CAPTION)
    screen = pg.display.set_mode(SIZE)
    gameLoop(screen)
    pg.quit()
