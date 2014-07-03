#!/usr/bin/env python3

import os

import pygame as pg

import classes
import data
import interface

#Whole menu main screen
class Menu():
    BG = pg.image.load('Images/menu.jpg')
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

#Login screen (parchment + input field)
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

        while True:
            clock.tick(30)
            events = pg.event.get()
            for e in events:
                if e.type == pg.QUIT:
                    return

            name = self.parchment.events(events) #inputEvent
            if name != None:
                if os.path.isfile('Saves/' + name):
                    self.text = 'I see, you\'re back, ' + name + '. Well, then you will continue your journew from where you have started... I must leave you now. Good luck!\nPress [RETURN]'
                else:
                    self.text = 'Greetings, sir ' + name + '. I will tell you a story of this world, then you can try to survive by yourself\nPress [RETURN]'
                    intro = True
                return name

            self.surface.fill(0)
            self.surface.blit(self.bg, (-x,0))
            x += dx
            if x > (self.bg.get_size()[0] - self.surface.get_size()[0]) / 2:
                dx = 0
            self.message.draw(self.text, self.surface)
            self.parchment.draw(self.surface)

            pg.display.flip()

#Whole world screen - picture, input field
class World():
    def __init__(self, surface):
        self.data = data.Data()
        self.intro = False
        self.introIndex = 0
        self.message = interface.Message(surface)
        self.musicOldName = ''
        self.surface = surface
        self.bg = '' #Because an error occur
        self.text = ''
        self.inputBox = interface.Input(surface)

    #Passing pers, and not persPlace, just for future extension
    def update(self, pers):
        self.data.update(pers)
        if pers.place[:5] == 'intro':
            self.intro = True
            place = pers.place[5:]
            if self.introIndex < len(getattr(self.data, eval('place'))):
                self.PLACE = 0
                self.text = getattr(self.data, eval('place'))[self.introIndex]
                self.bg = pg.image.load('Images/Intro/' + place + str(self.introIndex) + '.jpg')
                self.introIndex += 1
            else:
                self.introIndex = 0
                self.PLACE = next(item for item in self.data.place if item['Id'] == pers.place)
        else:
            pers.time += 10
            self.intro = False
            place = pers.place
            self.PLACE = next(item for item in self.data.place if item['Id'] == place)
            self.text = self.PLACE['Text']
            self.bg = pg.image.load('Images/' + place + '.jpg')

        musicName = os.path.basename(os.path.dirname('Images/' + place + '.jpg'))
        if self.musicOldName != musicName:
            self.musicOldName = musicName
            music = pg.mixer.Sound('Music/' + musicName + '.ogg')
            if pg.mixer.get_busy():
                pg.mixer.stop()
            music.play()

    def loop(self):
        clock = pg.time.Clock()
        x, dx = 0, 1

        while True:
            clock.tick(30)
            events = pg.event.get()
            for e in events:
                if e.type == pg.QUIT:
                    exit()
                if e.type == pg.KEYDOWN:
                    if e.key == pg.K_RETURN and self.intro == True:
                        if self.PLACE != 0:
#                            return self.PLACE['Goto'], None
                            return self.PLACE
                        else:
                            return None, None
            if self.intro == False:
                e = self.inputBox.events(events)
                if e!= None and e in self.PLACE['Move']:
                    return (self.PLACE['Goto'][self.PLACE['Move'].index(e)], self.PLACE['Mobs'])

            self.surface.fill(0)
            self.surface.blit(self.bg, (-x,0))
            x += dx
            if x > (self.bg.get_size()[0] - self.surface.get_size()[0]) / 2:
                dx = 0

            self.message.draw(self.text, self.surface)
            if self.intro == False:
                self.inputBox.draw(self.surface)

            pg.display.flip()

#Whole battle screen with lots of skill-buttons and input for typing
class Battle():
    def __init__(self, surface):
        lol = ''

    def loop(self, mobs, pers):
        mob = classes.Mob()
        battleInput = interface.Input(surface)
        clock = pg.time.Clock()
        while True:
            clock.tick(30)
            battleInput.draw(surface)

        return pers
