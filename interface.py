#!/usr/bin/env python3

import pygame as pg

class Input():

    #===== VARIABLES =====
    prompt = ''
    def __init__(self, surface):
        self.FONT = pg.font.Font('Fonts/rpg.ttf', 50)
        self.BG = pg.image.load('Images/parchment.png')
        self.WIDTH = self.BG.get_width()
        self.HEIGHT = self.BG.get_height()
        self.X = (surface.get_size()[0] - self.WIDTH) / 2
        self.Y = surface.get_size()[1] - self.HEIGHT
        #Surface which contains background + text
        self.surface = pg.Surface((self.WIDTH, self.HEIGHT))
        self.surface.set_colorkey(0)

    def draw(self, surface):
        self.surface.fill(0)
        self.surface.blit(self.BG, (0,0))
        text = self.FONT.render(self.prompt, True, (0,0,0))
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
