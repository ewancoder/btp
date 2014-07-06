import os

import pygame as pg

import classes
import data
import interface

class Menu():
    BG = pg.image.load('Images/menu.jpg')
    MUSIC = pg.mixer.Sound('Music/menu.ogg')
    
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
        #Returns its value (exits Menu) if not ''
        self.ret = ''
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
                self.MUSIC.play(-1)
            x += dx
            if x > self.BG.get_size()[0] - self.surface.get_size()[0] or x <= 0:
                dx *= -1

            self.surface.fill(0)
            self.surface.blit(self.BG, (-x, 0))
            self.menu.draw(self.surface)

            pg.display.flip()

class Login():
    TEXT = 'Tell me your name, Stranger!\nIf you are new here, I will tell you a story, and then you will step into this dangerous world, otherwise you will find yourself onto the place you left behind last time...'
    BG = pg.image.load('Images/login.jpg')

    def __init__(self, surface):
        self.message = interface.Message(surface)
        self.parchment = interface.Input(surface)
        self.surface = surface

    def loop(self):
        clock = pg.time.Clock()
        self.parchment.prompt = ''
        x, dx = 0, 1

        while True:
            clock.tick(30)
            events = pg.event.get()
            for e in events:
                if e.type == pg.QUIT:
                    quit()
                elif e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
                    return ''
            name = self.parchment.events(events) #inputEvent
            if name not in (None, ''):
                return name

            self.surface.fill(0)
            self.surface.blit(self.BG, (-x,0))
            x += dx
            if x > self.BG.get_size()[0] - self.surface.get_size()[0]:
                dx = 0
            self.message.draw(self.TEXT, self.surface)
            self.parchment.draw(self.surface)

            pg.display.flip()

class World():
    def __init__(self, surface):
        self.data = data.Data()
        self.introIndex = 0
        self.musicOldName = ''
        self.surface = surface
        self.inputBox = interface.Input(surface)
        self.message = interface.Message(surface)

    #Passing pers, and not persPlace, just for future extension
    def update(self, pers):
        self.pers = pers
        self.time = 0
        self.data.update(self.pers)
        if self.pers.place[:5] == 'intro':
            self.intro = True
            place = self.pers.place[5:]
            if self.introIndex < len(getattr(self.data, eval('place'))):
                self.PLACE = None
                self.text = getattr(self.data, eval('place'))[self.introIndex]
                self.bg = pg.image.load('Images/Intro/' + place + str(self.introIndex) + '.jpg')
                if self.introIndex+1 < len(getattr(self.data, eval('place'))):
                    self.introIndex += 1
                else:
                    self.introIndex = 0
                    self.PLACE = next(item for item in self.data.place if item['Id'] == self.pers.place)
            musicName = place
        else:
            self.intro = False
            place = self.pers.place
            self.PLACE = next(item for item in self.data.place if item['Id'] == place)
            self.bg = pg.image.load('Images/' + place + '.jpg')
            self.text = self.PLACE['Text']
            musicName = os.path.basename(os.path.dirname('Images/' + place + '.jpg'))
            self.time += self.PLACE['Time'] if 'Time' in self.PLACE.keys() else 10

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
                        return self.PLACE, None
            if self.intro == False:
                e = self.inputBox.events(events)
                if e!= None and e in self.PLACE['Move']:
                    move = next(item for item in self.data.place if item['Id'] == self.PLACE['Goto'][self.PLACE['Move'].index(e)])
                    self.time += move['Time'] if 'Time' in move else 10
                    self.pers.time += self.time
                    return self.PLACE, self.PLACE['Goto'][self.PLACE['Move'].index(e)]

            self.surface.fill(0)
            self.surface.blit(self.bg, (-x,0))
            x += dx
            if x > self.bg.get_size()[0] - self.surface.get_size()[0]:
                dx = 0

            self.message.draw(self.text, self.surface)
            if self.intro == False:
                self.inputBox.draw(self.surface)

            pg.display.flip()

class Battle():
    def __init__(self, surface):
        self.surface = surface
        self.battleInput = interface.Input(self.surface)
        self.battleText = interface.Message(self.surface)

    def loop(self, mobs, pers):
        clock = pg.time.Clock()
        mob = classes.Mob()

        while True:
            clock.tick(30)
            self.surface.fill(0)
            self.battleInput.draw(self.surface)
            self.battleText.draw('BattleTestWord', self.surface)

            pg.display.flip()

            for e in pg.event.get():
                if e.type == pg.QUIT:
                    #quit()
                    return pers #Temporary for chances debugging
