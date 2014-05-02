#!/usr/bin/env python3
#I am aiming to write this code both in python3 and python2 for learning sake (python2 for wide people range, python3 for future and coolness)
"""
    Copyright (c) 2014 EwanCoder <ewancoder@gmail.com> GPL

    This game blends these independent concepts:
        1. Supernatural world, based on CW Supernatural Show
        2. Text-based rpg quest game
        3. Type game - the faster you type, the more you gain
"""

import data as d #All text data + map dictionaries and etc.

import ewmenu
import interface

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
class Screens():

    def menu(self, surface):
        clock = pg.time.Clock()

        #===== CONSTANTS =====
        #Load files
        BG = pg.image.load('Images/background.jpg')
        MENU_MUSIC = pg.mixer.Sound('Music/menu.ogg')
        MAIN_MENU = (
            ['Start / Load Game', lambda: Screens().login(surface)],
            ['Settings', lambda: setattr(self, 'now', 1)],
            ['Quit', lambda: exit()]
        )
        SETTINGS_MENU = (
            ['This is settings example', lambda: print('There will be settings.')],
            ['Back', lambda: setattr(menu, 'goto', 1)]
        )
        MENU = (
            MAIN_MENU,
            SETTINGS_MENU
        )
        
        #===== VARIABLES =====
        x, dx = 0, 1    #Background movement
        #Construct menu
        menu = ewmenu.EwMenu(MENU)

        #===== MAIN LOOP =====
        while True:
            clock.tick(30)

            #===== EVENTS =====
            events = pg.event.get()
            for e in events:
                if e.type == pg.QUIT:
                    return
            #Processing menu events
            menu.events(events)

            #===== CALCULATIONS =====
            #Turn on music if not playing
            if not pg.mixer.get_busy():
                MENU_MUSIC.play(-1)
            #Move background image
            x += dx
            if x > BG.get_size()[0] - surface.get_size()[0] or x <= 0:
                dx *= -1

            #===== DRAWING =====
            surface.fill(0)
            surface.blit(BG, (-x, 0))
            menu.draw(surface)

            #===== SCREEN REFRESH =====
            pg.display.flip()

    def map(self, surface, place):
        x, dx = 0, 1
        message = interface.Message(surface)
        inputBox = interface.Input(surface)
        clock = pg.time.Clock()
        bg = pg.image.load('Images/Places/' + place + '.jpg')
        imusic = pg.mixer.Sound('Music/intro.ogg')
        PLACE = next(item for item in d.place if item['Id'] == place)
        text = PLACE['Text']
        if pg.mixer.get_busy():
            pg.mixer.stop()
        imusic.play()

        while True:
            clock.tick(30)
            events = pg.event.get()
            for e in events:
                if e.type == pg.QUIT:
                    exit()
            ievent = inputBox.events(events)
            if ievent != None:
                e = ievent
                if e in PLACE['Actions']:
                    return (PLACE['Goto'][PLACE['Actions'].index(e)], PLACE['Mobs'])

            surface.fill(0)
            surface.blit(bg, (-x,0))
            x += dx
            #Move background image
            if x > (bg.get_size()[0] - surface.get_size()[0]) / 2:
                dx = 0

            message.draw(text, surface)
            inputBox.draw(surface)

            pg.display.flip()

    def introduction(self, surface, name):
        x, dx = 0, 1
        message = interface.Message(surface)
        clock = pg.time.Clock()
        it = d.IntroText(name)
        allstep = len(it.introtext) - 1 #Number of step images
        allstep2 = len(it.introtext2) - 1
        step = 0 #Number of current intro slide
        bg = pg.image.load('Images/Intro/intro0.jpg')
        imusic = pg.mixer.Sound('Music/intro.ogg')
        text = it.introtext[0]
        if pg.mixer.get_busy():
            pg.mixer.stop()
        imusic.play()

        while True:
            clock.tick(30)
            events = pg.event.get()
            for e in events:
                if e.type == pg.QUIT:
                    return
                if e.type == pg.KEYDOWN and e.key == pg.K_RETURN:
                    if step < allstep:
                        step += 1
                        bg = pg.image.load('Images/Intro/intro' + str(step) + '.jpg')
                        if not pg.mixer.get_busy():
                            imusic = pg.mixer.Sound('Music/intro2.ogg')
                            imusic.play()
                        text = it.introtext[step]
                        x, dx = 0, 1
                    elif step == allstep:
                        bg = pg.image.load('Images/blackscreen.jpg')
                        text = ''
                        step += 1
                        imusic.stop()
                        x, dx = 0, 0
                    elif step - 2 < allstep + allstep2:
                        bg = pg.image.load('Images/Intro/intro' + str(step-1) + '.jpg')
                        if not pg.mixer.get_busy():
                            imusic = pg.mixer.Sound('Music/intro3.ogg')
                            imusic.play()
                        text = it.introtext2[step - allstep - 1]
                        step += 1
                        x, dx = 0, 1
                    else:
                        return()

            surface.fill(0)
            surface.blit(bg, (-x,0))
            if bg.get_size()[0] > 1100:
                x += dx
                #Move background image
                if x > (bg.get_size()[0] - surface.get_size()[0]) / 1:
                    dx = 0

            message.draw(text, surface)

            pg.display.flip()

    def login(self, surface):
        x, dx = 0, 1
        message = interface.Message(surface)
        parchment = interface.Parchment(surface)
        text = 'Tell me your name, Stranger!\nIf you are new here, I will tell you a story, and then you will step into this dangerous world, otherwise you will find yourself onto the place you left behind last time...'
        bg = pg.image.load('Images/login.jpg')
        clock = pg.time.Clock()
        intro = False
        step = 0 #If step = 1 - Return is pressed

        while True:
            clock.tick(30)


            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    return
                if event.type == pg.KEYDOWN and event.key == pg.K_RETURN and step == 1:
                    if intro:
                        Screens().introduction(surface, name)
                    Game().start(surface, name)
                    return

            ievent = parchment.events(events) #inputEvent
            if ievent != None:
                name = ievent
                step = 1
                if os.path.isfile('Saves/' + name):
                    text = 'I see, you\'re back, ' + name + '. Well, then you will continue your journew from where you have started... I must leave you now. Good luck!\nPress [RETURN]'
                else:
                    text = 'Greetings, sir ' + name + '. I will tell you a story of this world, then you can try to survive by yourself\nPress [RETURN]'
                    intro = True

            surface.fill(0)
            surface.blit(bg, (-x,0))
            x += dx
            #Move background image
            if x > (bg.get_size()[0] - surface.get_size()[0]) / 2:
                dx = 0

            message.draw(text, surface)
            if step == 0:
                parchment.draw(surface)

            pg.display.flip()

    def battle(self, surface, mobs, pers, mob):
        battleInput = interface.Input(surface)
        clock = pg.time.Clock()
        while True:
            clock.tick(30)
            battleInput.draw(surface)

        return pers

class Mob():
    name = 'Skeleton'

class Quest():
    print('Class for quests and tasks and notes')

class Pers():
    place = 'OldManHouse'
    maxhp = 20
    hp = maxhp

class Game():
    """Game logics handling"""

    #===== VARIABLES =====
    pers = Pers()

    def menu(self, surface):
        mainMenu = Screens().menu(surface)

    def start(self, surface, name):
        d.chname(name)
        if os.path.isfile('Saves/' + name):
            self.load(name)
        else:
            self.save(name)
        running = True #I need this because there'll be no other way out
        while running:
            (self.pers.place, mobs) = Screens().map(surface, self.pers.place)
            if random.randrange(0, 100) < mobs['Chance']:
                self.pers = Screens().battle(surface, mobs, self.pers, Mob())
            #IF anything else for screens -> Screens().anythingelse()
            #check_upon_death + check_upon_new_level + everything else (Pers.update?)
            self.save(name)

    def save(self, name):
        with open('Saves/' + name, 'wb') as f:
            pickle.dump(self.pers, f)
            print('Game saved as ' + name)

    def load(self, name):
        with open('Saves/' + name, 'rb') as f:
            self.pers = pickle.load(f)
            print('Game loaded as ' + name)

#========== MAIN PROGRAM ==========
if __name__ == '__main__':
    pg.display.set_caption(CAPTION)
    screen = pg.display.set_mode(SIZE)
    Game().menu(screen)
    pg.quit()
