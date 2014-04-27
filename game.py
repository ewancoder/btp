#!/usr/bin/env python3
#I am aiming to write this code both in python3 and python2 for learning case (python2 for wide range of people, python3 for future and coolness)
"""
    Copyright (c) 2014 EwanCoder <ewancoder@gmail.com>

    This game compiles these independent concepts:
        1. Supernatural world, based on CW Supernatural Show
        2. Text-based rpg quest games
        3. Typo games - the faster you type, the more you gain
"""

import pygame as pg
from string import ascii_letters as CHARS

import ewmenu
import message

#========== CONSTANTS ==========
BACKSPACE = '\x08'
CAPTION = 'Big Typernatural Project'
SIZE = (1000, 700)

#========== CLASSES ==========
class Game():
    def main(self, screen):
        pg.mixer.stop()
        clock = pg.time.Clock()
        
        background = pg.image.load('background.jpg')
        text = "This is some long long text which needs of word wrapping loool :)"
        font = pg.font.Font(None, 30)
        rect = pg.Rect((40, 40, 600, 200))

        while True:
            screen.fill(0)
            screen.blit(background, (0,0))

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()

            clock.tick(30)
            message.Message().main(text, font, rect, screen)

            pg.display.flip()

class Battle():
    paused = False #If paused, goes black screen and paused :)
    prompt = ''
    def main(self, screen):
        pg.mixer.stop()
        background = pg.image.load('background.jpg')
        clock = pg.time.Clock()
        while True:
            clock.tick(30)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                elif event.type == pg.KEYDOWN:
                    if event.unicode in CHARS + BACKSPACE and event.unicode != '':
                        if event.unicode == BACKSPACE:
                            self.prompt = self.prompt[:-1]
                    elif event.key == pg.K_ESCAPE:
                        self.paused = not self.paused
                        print("Here will be pause-message about 'q' = exit to menu")
                    elif event.key == pg.K_RETURN:
                        print("Here will be word nulling")
                    if event.key == pg.K_q and self.paused == True:
                        return

            screen.fill(0)
            screen.blit(background, (0,0))

            pg.display.flip()

class Menu():
    running = True
    def main(self, screen):
        clock = pg.time.Clock()
        background = pg.image.load('background.jpg')
        pg.mixer.init()
        main_theme = pg.mixer.Sound('main.ogg')
        menu = ewmenu.EwMenu(
            ['New game', lambda: Game().main(screen)],
            ['Load game', lambda: Battle().main(screen)],
            ['Settings', lambda: setattr(self, 'running', False)],
            ['Quit', lambda: setattr(self, 'running', False)]
        )

        x, dx = 0, 1

        while self.running:
            if not pg.mixer.get_busy():
                main_theme.play(-1) #Repeating music
            screen.fill(0)
            screen.blit(background, (-x,0))
            x += dx
            if x > background.get_size()[0] - SIZE[0] or x <= 0:
                dx *= -1

            events = pg.event.get()
            clock.tick(30)
            for event in events:
                if event.type == pg.QUIT:
                    exit()
            menu.update(events)
            menu.draw(screen)

            #===== FLIPPING DISPLAY AFTER DRAWING =====
            pg.display.flip()

#========== MAIN PROGRAM ==========
if __name__ == '__main__':
    pg.display.set_caption(CAPTION)
    screen = pg.display.set_mode(SIZE)
    Menu().main(screen)
    pg.quit()
