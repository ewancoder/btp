#!/usr/bin/env python3

import os

import pygame as pg

import data as d
import interface

class Menu():

    BG = pg.image.load('Images/background.jpg')
    MENU_MUSIC = pg.mixer.Sound('Music/menu.ogg')

    #Returns its value (exits Menu) if not ''
    ret = ''
    
    def __init__(self, surface):
        self.surface = surface

        MAIN_MENU = (
            ['Start / Load Game', lambda: setattr(self, 'ret', 'login')],
            ['Settings', lambda: setattr(self.menu, 'now', 1)],
            ['Quit', lambda: quit()]
        )
        SETTINGS_MENU = (
            ['This is settings example', lambda: print('There will be settings.')],
            ['Back', lambda: setattr(self.menu, 'now', 0)]
        )
        MENU = (
            MAIN_MENU,
            SETTINGS_MENU
        )

        self.menu = interface.Menu(MENU)

    def loop(self):
        clock = pg.time.Clock()
        x, dx = 0, 1

        while True:
            clock.tick(30)
            if self.ret != '':
                return self.ret

            events = pg.event.get()
            for e in events:
                if e.type == pg.QUIT:
                    quit()
            self.menu.events(events)

            if not pg.mixer.get_busy():
                self.MENU_MUSIC.play(-1)
            x += dx
            if x > self.BG.get_size()[0] - self.surface.get_size()[0] or x <= 0:
                dx *= -1

            self.surface.fill(0)
            self.surface.blit(self.BG, (-x, 0))
            self.menu.draw(self.surface)

            pg.display.flip()

class World():
    def loop(self, surface, place):
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
            if x > (bg.get_size()[0] - surface.get_size()[0]) / 2:
                dx = 0

            message.draw(text, surface)
            inputBox.draw(surface)

            pg.display.flip()

class Introduction():
    def loop(self, surface, name):
        x, dx = 0, 1
        message = interface.Message(surface)
        clock = pg.time.Clock()
        it = d.IntroText(name)
        allstep = len(it.introtext) - 1
        allstep2 = len(it.introtext2) - 1
        step = 0
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

class Login():
    def __init__(self, surface):
        self.surface = surface

        self.message = interface.Message(surface)
        self.parchment = interface.Parchment(surface)
        self.text = 'Tell me your name, Stranger!\nIf you are new here, I will tell you a story, and then you will step into this dangerous world, otherwise you will find yourself onto the place you left behind last time...'
        self.bg = pg.image.load('Images/login.jpg')

    def loop(self):
        clock = pg.time.Clock()
        x, dx = 0, 1
        intro = False
        step = 0 #If step = 1 - Return is pressed

        while True:
            clock.tick(30)
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    return
                #if event.type == pg.KEYDOWN and event.key == pg.K_RETURN and step == 1:
                #    if intro:
                #        Screens().introduction(surface, name)
                #    return name

            ievent = self.parchment.events(events) #inputEvent
            if ievent != None:
                name = ievent
                #step = 1
                if os.path.isfile('Saves/' + name):
                    self.text = 'I see, you\'re back, ' + name + '. Well, then you will continue your journew from where you have started... I must leave you now. Good luck!\nPress [RETURN]'
                else:
                    self.text = 'Greetings, sir ' + name + '. I will tell you a story of this world, then you can try to survive by yourself\nPress [RETURN]'
                    intro = True
                return name

            self.surface.fill(0)
            self.surface.blit(self.bg, (-x,0))
            x += dx
            #Move background image
            if x > (self.bg.get_size()[0] - self.surface.get_size()[0]) / 2:
                dx = 0

            self.message.draw(self.text, self.surface)
            if step == 0:
                self.parchment.draw(self.surface)

            pg.display.flip()

class Battle():
    def loop(self, surface, mobs, pers, mob):
        battleInput = interface.Input(surface)
        clock = pg.time.Clock()
        while True:
            clock.tick(30)
            battleInput.draw(surface)

        return pers
