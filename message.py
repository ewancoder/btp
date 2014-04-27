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

        surface = pg.Surface(rect.size)
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

        surface.set_alpha(100)

        return surface

    def main(self, text, font, rect, screen):
        x = 200
        screen.blit(self.wordwrap(text, font, rect, (0,0,0), (255,0,0)), (x, 10))
