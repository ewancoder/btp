#!/usr/bin/env python3

import pygame as pg

class Menu():

    #===== CONSTANTS =====
    X, Y = 10, 10
    DCOLOR, HCOLOR = (200, 200, 100), (200, 100, 100)
    FONT = pg.font.Font('Fonts/rpg.ttf', 40)
    SOUND = pg.mixer.Sound('Sounds/select.ogg')
    
    #===== VARIABLES =====
    selected = 0    #Index of selected menu item
    now = 0         #Index of menu which is showing NOW

    def __init__(self, items):
        """Need __init__ for passing 'items' argument and forming dictionary"""
        self.ITEMS = items
        self.update()

    def update(self):
        #KOSTYL FOR 0 - no needed anymore
        #if self.now == -1:
        #    self.now = 0
        self.selected = 0
        self.items = [{'Label': i[0], 'Action': i[1]} for i in self.ITEMS[self.now]]

    def draw(self, surface):
        offset = 0 #Incremental variable for making y-difference
        for index, i in enumerate(self.items):
            if self.selected == index:
                color = self.DCOLOR
            else:
                color = self.HCOLOR
            text = self.FONT.render(i['Label'], True, color)
            surface.blit(text, (self.X, self.Y + offset))
            offset += self.FONT.get_height()

    def events(self, events):
        for e in events:
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_DOWN or e.key == pg.K_j or e.key == pg.K_s:
                    if self.selected < len(self.items) - 1:
                        self.selected += 1
                elif e.key == pg.K_UP or e.key == pg.K_k or e.key == pg.K_w:
                    if self.selected > 0:
                        self.selected -= 1
                elif e.key == pg.K_RETURN or e.key == pg.K_SPACE or e.key == pg.K_l:
                    self.SOUND.play()
                    self.items[self.selected]['Action']()
        if self.now != 0:
            self.update()
            self.now = 0

class Input():

    #===== VARIABLES =====
    prompt = ''
    def __init__(self, surface):
        self.FONT = pg.font.Font('Fonts/rpg.ttf', 50)
        self.BG = pg.image.load('Images/parchment.png')
        self.setsize(surface)
        self.X = (surface.get_size()[0] - self.WIDTH) / 2
        self.Y = surface.get_size()[1] - self.HEIGHT
        #Surface which contains background + text
        self.surface = pg.Surface((self.WIDTH, self.HEIGHT), pg.SRCALPHA)
        self.surface.set_colorkey(0)

    #KOSTYL
    def setsize(self, surface):
        self.WIDTH = surface.get_size()[0] / 1.2
        self.HEIGHT = surface.get_size()[1] / 8

    def draw(self, surface):
        self.surface.fill((0,0,0, 120))
        text = self.FONT.render(self.prompt, True, (180,150,0))
        self.surface.blit(text, ((self.WIDTH - text.get_width()) / 2, (self.HEIGHT - text.get_height()) / 2))
        surface.blit(self.surface, (self.X, self.Y))

    def events(self, events):
        for e in events:
            if e.type == pg.KEYDOWN:
                if e.unicode.isalpha():
                    self.prompt += e.unicode
                elif e.key == pg.K_BACKSPACE:
                    self.prompt = self.prompt[:-1]
                elif e.key == pg.K_RETURN:
                    prompt = self.prompt
                    self.prompt = ''
                    return prompt

class Parchment(Input):
    def setsize(self, surface):
        self.WIDTH = self.BG.get_width()
        self.HEIGHT = self.BG.get_height()
    def draw(self, surface):
        self.surface.fill(0)
        self.surface.blit(self.BG, (0,0))
        text = self.FONT.render(self.prompt, True, (0,0,0))
        self.surface.blit(text, ((self.WIDTH - text.get_width()) / 2, (self.HEIGHT - text.get_height()) / 2))
        surface.blit(self.surface, (self.X, self.Y))


class Message():

    def __init__(self, surface):
        self.FONT = pg.font.Font('Fonts/comic.ttf', 30)
        self.RECT = pg.Rect((0, 0, surface.get_size()[0] - 10*2, surface.get_size()[1] / 3))
        self.X = surface.get_size()[0] / 2 - self.RECT.width / 2

    def wordwrap(self, text):
        text_color = (200,200,100)
        bg_color = (0,0,0, 80)
        finallines = []
        lines = text.splitlines()

        for line in lines:
            if self.FONT.size(line)[0] > self.RECT.width:
                words = line.split(' ')
                newline = ''
                for word in words:
                    if self.FONT.size(word)[0] >= self.RECT.width:
                        print('Too long word!')
                        break
                    testline = newline + word + ' '
                    if self.FONT.size(testline)[0] < self.RECT.width:
                        newline = testline
                    else:
                        finallines.append(newline)
                        newline = word + ' '
                finallines.append(newline)
            else:
                finallines.append(line)

        surface = pg.Surface(self.RECT.size, pg.SRCALPHA, 32)
        surface.fill(bg_color)

        height = 0
        for line in finallines:
            text = self.FONT.render(line, True, text_color)
            surface.blit(text, ((self.RECT.width - text.get_width()) / 2, height))
            height += self.FONT.size(line)[1]

        return surface

    def draw(self, text, surface):
        surface.blit(self.wordwrap(text), (self.X, 10))
