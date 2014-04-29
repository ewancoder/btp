#!/usr/bin/env python
import pygame as pg
pg.mixer.pre_init(22050, -16, True, 512)
pg.init()

class EwMenu():
    """EwanMenu - simple class for easy menu creation"""

    #Initializing
    pg.font.init()

    #===== CONSTANTS =====
    #Initial coordinates
    X, Y = 10, 10
    #Default color
    DCOLOR = (200, 200, 100)
    #Highlighted color
    HCOLOR = (200, 100, 100)
    #Default font
    font = pg.font.Font('Fonts/rpg.ttf', 40)
    
    #Initialize sound
    #pg.mixer.init()
    s_selected = pg.mixer.Sound('Sounds/select.ogg')

    #Variables
    selected = 0

    #===== FUNCTIONS =====
    #Initialization
    def __init__(self, *items):
        #Add all items in a dictionary
        self.items = [{'Label': x[0], 'Action': x[1]} for x in items]
        print(self.items)
    
    #Draw all text on surface
    def draw(self, surface):
        offset = 0  #Incremental variable for making y-difference between menu items
        for index, item in enumerate(self.items):
            if self.selected == index:
                color = self.DCOLOR
            else:
                color = self.HCOLOR
            text = self.font.render(item['Label'], True, color)
            surface.blit(text, (self.X, self.Y + offset)) #Add item to surface
            offset += self.font.get_height() #Increment offset

    #Update menu items status
    def move(self, move):
        if move == 1:
            self.s_selected.play()
            self.selected += 1
        elif move == -1:
            self.s_selected.play()
            self.selected += 1
        #Block going off the range
        if self.selected > len(self.items) - 1:
            self.selected = len(self.items) - 1
        elif self.selected < 0:
            self.selected = 0

    def activate(self):
        self.items[self.selected]['Action'][1]()
