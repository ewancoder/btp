#!/usr/bin/env python3

import os

import pygame as pg

import classes
import data
import interface

#Whole menu main screen
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
        BG = self.BG
        MENU_MUSIC = self.MENU_MUSIC
        menu = self.menu
        ret = self.ret  #NEED TO REPEAT IT EACH FRAME
        #FUCK. SUPPOSEDLY I'm going to start using just self.everywhere
        surface = self.surface

        clock = pg.time.Clock()
        x, dx = 0, 1

        while True:
            clock.tick(30)
            ret = self.ret
            if ret != '':
                return ret

            events = pg.event.get()
            for e in events:
                if e.type == pg.QUIT:
                    quit()
            menu.events(events)

            if not pg.mixer.get_busy():
                MENU_MUSIC.play(-1)
            x += dx
            if x > BG.get_size()[0] - surface.get_size()[0] or x <= 0:
                dx *= -1

            surface.fill(0)
            surface.blit(BG, (-x, 0))
            menu.draw(surface)

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

#Whole world screen - picture, input field
class World():
    def __init__(self, surface):
        self.intro = False
        self.introIndex = 0
        self.message = interface.Message(surface)
        self.musicOldName = ''
        self.surface = surface
        self.bg = '' #Because an error occur
        self.text = ''
        self.inputBox = interface.Input(surface)

    def update(self, pers):
        #Passing pers, and not persPlace, just for future extension
        intro = self.intro
        introIndex = self.introIndex
        musicOldName = self.musicOldName
        bg = self.bg
        text = self.text

        if pers.place[:5] == 'intro':
            intro = True
            place = pers.place[5:]
            if introIndex < len(getattr(data, eval('place'))):
                PLACE = 0
                text = getattr(data, eval('place'))[introIndex]
                bg = pg.image.load('Images/' + place + str(introIndex) + '.jpg')
                introIndex += 1
            else:
                introIndex = 0
                PLACE = next(item for item in data.place if item['Id'] == place)
        else:
            intro = False
            place = pers.place
            PLACE = next(item for item in data.place if item['Id'] == place)
            text = PLACE['Text']
            bg = pg.image.load('Images/' + place + '.jpg')

        musicName = os.path.basename(os.path.dirname('Images/' + place + '.jpg'))
        if musicOldName != musicName:
            musicOldName = musicName
            music = pg.mixer.Sound('Music/' + musicName + '.ogg')
            if pg.mixer.get_busy():
                pg.mixer.stop()
            music.play()

        self.bg = bg
        self.intro = intro
        self.text = text
        self.introIndex = introIndex
        self.PLACE = PLACE

    def loop(self):
        surface = self.surface
        intro = self.intro
        bg = self.bg
        message = self.message
        text = self.text
        PLACE = self.PLACE
        inputBox = self.inputBox

        clock = pg.time.Clock()
        x, dx = 0, 1

        while True:
            clock.tick(30)
            events = pg.event.get()
            for e in events:
                if e.type == pg.QUIT:
                    exit()
                if e.type == pg.KEYDOWN:
                    if e.key == pg.K_RETURN and intro == True:
                        if PLACE != 0:
                            return (PLACE['Goto'], PLACE['Mobs'])
                        else:
                            return (0, 0)
            if intro == False:
                e = inputBox.events(events)
                if e != None:
                    if e in PLACE['Actions']:
                        return (PLACE['Goto'][PLACE['Actions'].index(e)], PLACE['Mobs'])

            surface.fill(0)
            surface.blit(bg, (-x,0))
            x += dx
            if x > (bg.get_size()[0] - surface.get_size()[0]) / 2:
                dx = 0

            message.draw(text, surface)
            if intro == False:
                inputBox.draw(surface)

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
