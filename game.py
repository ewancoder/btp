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
    pers = classes.Pers()
    menuScreen = screens.Menu(surface)
    loginScreen = screens.Login(surface)
    worldScreen = screens.World(surface)
    battleScreen = screens.Battle(surface)

    while True:
        while pers.name == '':
            loaded = False
            if menuScreen.loop() == 'login':
                pers.name = loginScreen.loop()

        if not loaded:
            if os.path.isfile('Saves/' + pers.name):
                pers = pers.load()
            else:
                if not os.path.isdir('Saves'):
                    os.mkdir('Saves')
                pers = pers.save()
            loaded = True

        worldScreen.update(pers) #Load whole world current environment based on "pers"
        #NEED ASSURANCE
        worldScreen.loop()
        #place, move = worldScreen.loop() #Loop current world "snap" (until you move away or hit a monster)
        #print(pers.time)
        #if place != None:
        #    pers.place = place['Goto'] if  move == None else move
        #    if 'Mobs' in place.keys():
        #        if random.randrange(0, 100) < place['Mobs']['Chance']:
        #            pers = battleScreen.loop(pers)
        #pers.save()

if __name__ == '__main__':
    pg.display.set_caption(CAPTION)
    screen = pg.display.set_mode(SIZE)
    gameLoop(screen)
    pg.quit()
