#!/usr/bin/env python3

import pygame as pg

class Message():
    def wordwrap(self, text, font, rect, text_color, bg_color, justification = 1):
        finallines = []
        lines = text.splitlines()

        for line in lines:
            if font.size(line)[0] > rect.width:
                words = line.split(' ')
                newline = ''
                for word in words:
                    if font.size(word)[0] >= rect.width:
                        print('Too long word!')
                        break
                    testline = newline + word + ' '
                    if font.size(testline)[0] < rect.width:
                        newline = testline
                    else:
                        finallines.append(newline)
                        newline = word + ' '
                finallines.append(newline)
            else:
                finallines.append(line)

        key_color = (0, 255, 0)

        surface = pg.Surface(rect.size, pg.SRCALPHA, 32)
        surface.fill(bg_color)

        newheight = 0
        for line in finallines:
            if newheight + font.size(line)[1] >= rect.height:
                print('Too tall line!')
                break
            if line != '':
                temp = font.render(line, 1, text_color)
                if justification == 0:
                    surface.blit(temp, (0, newheight))
                elif justification == 1:
                    surface.blit(temp, ((rect.width - temp.get_width()) / 2, newheight))
                elif justification == 2:
                    surface.blit(temp, (rect.width - temp.get_width(), newheight))
            newheight += font.size(line)[1]

        return surface

    def refresh(self, text, screen):
        screen.blit(self.wordwrap(text, self.font, self.rect, (200,200,100), (255,0,0, 80)), (self.x,self.y))

    def __init__(self, screen):
        x = 10
        self.y = 10
        self.font = pg.font.Font('Fonts/comic.ttf', 30)
        self.rect = pg.Rect((0, 0, screen.get_size()[0]-x*2, screen.get_size()[1] / 3))
        self.x = screen.get_size()[0] / 2 - self.rect.width / 2
