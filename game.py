#!/usr/bin/env python3
#I am aiming to write this code both in python3 and python2 for learning sake (python2 for wide people range, python3 for future and coolness)
"""
    Copyright (c) 2014 EwanCoder <ewancoder@gmail.com> GPL

    This game compiles these independent concepts:
        1. Supernatural world, based on CW Supernatural Show
        2. Text-based rpg quest game
        3. Type game - the faster you type, the more you gain
"""

import ewmenu
import interface

import os #For checking file existence

import pygame as pg
pg.mixer.pre_init(22050, -16, True, 512)
pg.init()

#========== CONSTANTS ==========
CAPTION = 'Big Typernatural Project'
SIZE = (1000, 700)

#========== CLASSES ==========
class Screens():

    #===== VARIABLES =====
    x, dx = 0, 1    #Background movement

    def loginScreen(self, surface):
        message = interface.Message(surface)
        inputbox = interface.Input(surface)
        text = 'Tell me your name, Stranger!\nIf you are new here, I will come with you through the first steps you take in this dangerous world, otherwise you will find yourself onto the place you left behind last time...'
        bg = pg.image.load('Images/login.jpg')
        clock = pg.time.Clock()
        step = 0 #STEP on which current input/interface handling is dangling :D

        while True:
            clock.tick(30)


            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    exit()

            name = inputbox.events(events)
            if name != None:
                if step == 0:
                    if os.path.isfile('Saves/' + name):
                        text = 'I see, you\'re back, ' + name + '. Well, then you will continue your journew from where you have started... I must leave you now. Good luck!'
                    else:
                        text = 'Greetings, sir ' + name + '. I will lead you through some survival basis in this cruel world, then you must do it by yourself\nPress [RETURN]'
                    step += 1
                else:
                    Game().start(name)
                    return

            surface.fill(0)
            surface.blit(bg, (-self.x,0))
            self.x += self.dx
            #Move background image
            if self.x > (bg.get_size()[0] - SIZE[0]) / 2:
                self.dx = 0

            message.draw(text, surface)
            inputbox.draw(surface)

            pg.display.flip()

class Game():

    def start(self, name):
        clock = pg.time.Clock()

class Menu():

    #===== VARIABLES =====
    x, dx = 0, 1    #Background movement

    def main(self, surface, items = 0):
        clock = pg.time.Clock()

        #===== INITIAL SETUP =====
        mainMenu = (
            ['Start / Load Game', lambda: Screens().loginScreen(surface)],
            ['Settings', lambda: self.main(surface, settingsMenu)],
            ['Quit', lambda: exit()]
        )
        settingsMenu = (
            ['There\'re no settings here yet...', lambda: print('There will be settings')],
            ['Back', lambda: self.main(surface)]
        )
        if items == 0:
            items = mainMenu
        #Load files
        background = pg.image.load('Images/background.jpg')
        main_theme = pg.mixer.Sound('Music/menu.ogg')
        #Construct menu
        menu = ewmenu.EwMenu(items)

        #===== MAIN LOOP =====
        while True:
            clock.tick(30)

            #===== EVENTS =====
            events = pg.event.get()
            for e in events:
                if e.type == pg.QUIT:
                    exit()
            #Processing menu events
            menu.events(events)

            #===== CALCULATIONS =====
            #Turn on music if not playing
            if not pg.mixer.get_busy():
                main_theme.play(-1) #Repeating music continuously
            #Move background image
            self.x += self.dx
            if self.x > background.get_size()[0] - SIZE[0] or self.x <= 0:
                self.dx *= -1

            #===== DRAWING =====
            surface.fill(0)
            surface.blit(background, (-self.x, 0))
            menu.draw(surface)

            #===== SCREEN REFRESH =====
            pg.display.flip()

#========== MAIN PROGRAM ==========
if __name__ == '__main__':
    pg.display.set_caption(CAPTION)
    screen = pg.display.set_mode(SIZE)
    Menu().main(screen)
    pg.quit()
