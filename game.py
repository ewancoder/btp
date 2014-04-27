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
import ewmenu

#========== CONSTANTS ==========
CAPTION = 'Big Typernatural Project'
SIZE = (1000, 700)

#========== CLASSES ==========
class Menu():
    running = True
    def main(self, screen):
        clock = pg.time.Clock()

        menu = ewmenu.EwMenu(
            ['New game', lambda: setattr(self, 'running', False)],
            ['Load game', lambda: setattr(self, 'running', False)],
            ['Settings', lambda: setattr(self, 'running', False)],
            ['Quit', lambda: setattr(self, 'running', False)]
        )

        while self.running:
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
