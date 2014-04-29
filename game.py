#!/usr/bin/env python3
#I am aiming to write this code both in python3 and python2 for learning case (python2 for wide range of people, python3 for future and coolness)
"""
    Copyright (c) 2014 EwanCoder <ewancoder@gmail.com>

    This game compiles these independent concepts:
        1. Supernatural world, based on CW Supernatural Show
        2. Text-based rpg quest games
        3. Typo games - the faster you type, the more you gain
"""

import pickle
import pygame as pg
pg.mixer.pre_init(22050, -16, True, 512)
pg.init()

import ewmenu
import interface


#========== CONSTANTS ==========
BACKSPACE = '\x08'
CAPTION = 'Big Typernatural Project'
from string import ascii_letters as CHARS
SIZE = (1000, 700)

#========== CLASSES ==========
class Pers():
    def save(self, name):
        with open('Saves/' + name, 'wb') as f:
            pickle.dump(self, f)

    def load(self, name):
        with open('Saves/' + name, 'rb') as f:
            self = pickle.load(f)

class Game():
    def main(self, screen):
        pg.mixer.stop()
        clock = pg.time.Clock()
        
        background = pg.image.load('background.jpg')
        text = "This is some long long text which needs of word wrapping loool :)"

        message = interface.Message(screen)

        while True:
            screen.fill(0)
            screen.blit(background, (0,0))

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()

            clock.tick(30)
            message.refresh(text, screen)

            pg.display.flip()

class Battle():
    #===== MAIN BATTLE FUNCTION =====
    def main(self, screen):
        #Create new clock
        clock = pg.time.Clock()

        #Stop music if playing
        if pg.mixer.get_busy():
            pg.mixer.stop()
        #Load files
        background = pg.image.load('background.jpg') #Setup battle background - here will be random select from Images/Battle folder

        #===== MAIN LOOP =====
        while True:
            clock.tick(30)

            #===== EVENTS =====
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                elif event.type == pg.KEYDOWN:
                    if event.unicode in CHARS + BACKSPACE and event.unicode != '':
                        if event.unicode == BACKSPACE:
                            self.prompt = self.prompt[:-1]
                        else:
                            self.prompt += event.unicode
                    elif event.key == pg.K_ESCAPE:
                        print("Here will be pause-message about 'q' = exit to menu")
                        return #Need to do it only if self.paused is true & q is pressed
                    elif event.key == pg.K_RETURN:
                        print("Here will be word nulling")

            #===== DRAWING =====
            screen.fill(0)
            screen.blit(background, (0,0))

            #===== SCREEN REFRESH =====
            pg.display.flip()

class Menu():
    #===== MAIN BATTLE FUNCTION =====
    def main(self, screen):
        #Create new clock
        clock = pg.time.Clock()
        #Set loop variable
        running = True

        #Setup initial menu pack
        mainMenu = (
            ['Start / Load Game', lambda: Game().main(screen)],
            ['Settings', lambda: setattr(self, 'menu', ewmenu.EwMenu(settingsMenu))],
            ['Quit', lambda: setattr(self, 'running', False)]
        )
        settingsMenu = (
            ['Start / Load Game', lambda: Game().main(screen)]
        )

        #Load files
        background = pg.image.load('Images/background.jpg') #Background image
        main_theme = pg.mixer.Sound('Music/menu.ogg') #Background music
        #Construct menu
        menu = ewmenu.EwMenu(mainMenu)
        #Background movement variables
        x, dx = 0, 1

        #===== MAIN LOOP =====
        while running:
            clock.tick(30)

            #===== EVENTS =====
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    exit()
                elif e.type == pg.KEYDOWN:
                    if e.key == pg.K_DOWN or e.key == pg.K_j or e.key == pg.K_s:
                        menu.move(1)
                    elif e.key == pg.K_UP or e.key == pg.K_k or e.key == pg.K_w:
                        menu.move(-1)
                    elif e.key == pg.K_RETURN or e.key == pg.K_SPACE or e.key == pg.K_l:
                        menu.activate()
            
            #===== CALCULATIONS =====
            #Turn on music if not playing
            if not pg.mixer.get_busy():
                main_theme.play(-1) #Repeating music continuosly
            #Move background image
            x += dx
            if x > background.get_size()[0] - SIZE[0] or x <= 0:
                dx *= -1

            #===== DRAWING =====
            screen.fill(0)
            screen.blit(background, (-x,0))
#            menu.draw(screen) #Refresh menu

            #===== SCREEN REFRESH =====
            pg.display.flip()

#========== MAIN PROGRAM ==========
if __name__ == '__main__':
    pg.display.set_caption(CAPTION)
    screen = pg.display.set_mode(SIZE)
    Menu().main(screen)
    pg.quit()
