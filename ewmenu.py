#!/usr/bin/env python3

import pygame as pg

class EwMenu():

    #===== CONSTANTS =====
    X, Y = 10, 10
    DCOLOR, HCOLOR = (200, 200, 100), (200, 100, 100)
    
    #===== VARIABLES =====
    selected = 0    #Index of selected menu item
    now = 0         #Index of menu which is showing NOW

    def __init__(self, items):
        """Need __init__ for passing 'items' argument and forming dictionary"""
        self.ITEMS = items
        self.update()
        self.FONT = pg.font.Font('Fonts/rpg.ttf', 40)
        self.SOUND = pg.mixer.Sound('Sounds/select.ogg')

    def update(self):
        #KOSTYL FOR 0
        if self.now == -1:
            self.now = 0
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
