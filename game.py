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

#========== CONSTANTS ==========
CAPTION = 'Big Typernatural Project'
SIZE = (1000, 700)

#========== CLASSES ==========
class Menu():
    def main(self, screen):
        print("Here will be menu!")

#========== MAIN PROGRAM ==========
if __name__ == '__main__':
    screen = pg.display.set_mode(SIZE)
    pg.display.set_caption(CAPTION)
    Menu().main(screen)
