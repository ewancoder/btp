import random

import pygame as pg

class Menu():
    X, Y = 10, 10
    DCOLOR, HCOLOR = (200, 200, 100), (200, 100, 100)
    FONT = pg.font.Font('Fonts/rpg.ttf', 40)
    SELECT_SOUND = pg.mixer.Sound('Sounds/select.ogg')
    SWITCH_SOUND = pg.mixer.Sound('Sounds/switch.ogg')

    selected = 0    #Index of selected menu item
    now = 0         #Index of menu which is showing NOW

    def __init__(self, items):
        self.ITEMS = items
        self.update()

    def update(self):
        self.selected = 0
        self.items = [{'Label': i[0], 'Action': i[1]} for i in self.ITEMS[self.now]]

    def draw(self, surface):
        offset = 0 #Incremental variable for making y-difference
        for index, i in enumerate(self.items):
            if self.selected == index:
                color = self.HCOLOR
            else:
                color = self.DCOLOR
            text = self.FONT.render(i['Label'], True, color)
            surface.blit(text, (self.X, self.Y + offset))
            offset += self.FONT.get_height()

    def events(self, events):
        for e in events:
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_DOWN or e.key == pg.K_j or e.key == pg.K_s:
                    if self.selected < len(self.items) - 1:
                        self.SWITCH_SOUND.play()
                        self.selected += 1
                elif e.key == pg.K_UP or e.key == pg.K_k or e.key == pg.K_w:
                    if self.selected > 0:
                        self.SWITCH_SOUND.play()
                        self.selected -= 1
                elif e.key == pg.K_RETURN or e.key == pg.K_SPACE or e.key == pg.K_l:
                    self.SELECT_SOUND.play()
                    self.items[self.selected]['Action']()
                    self.update()

class Message():
    def __init__(self, surface):
        self.BG_COLOR = (0,0,0, 80)
        self.TEXT_COLOR = (200,200,100)
        self.RECT = pg.Rect((0, 0, surface.get_size()[0] - 10*2, surface.get_size()[1] / 3))
        self.X = surface.get_size()[0] / 2 - self.RECT.width / 2
        self.setFontSize(24)
        self.surface = surface

    def setFontSize(self, size):
        self.FONT = pg.font.Font('Fonts/comic.ttf', size)

    def wordwrap(self, text):
        size = 20

        finallines = []
        lines = text.splitlines()
        for line in lines:
            if self.FONT.size(line)[0] > self.RECT.width:
                words = line.split(' ')
                newline = ''
                for word in words:
                    while self.FONT.size(word)[0] >= self.RECT.width:
                        size -= 1
                        self.setFontSize(size)
                    testline = newline + word + ' '
                    if self.FONT.size(testline)[0] < self.RECT.width:
                        newline = testline
                    else:
                        finallines.append(newline)
                        newline = word + ' '
                finallines.append(newline)
            else:
                finallines.append(line)

        return finallines

    def draw(self, finallines):
        surface = pg.Surface(self.RECT.size, pg.SRCALPHA, 32)
        surface.fill(self.BG_COLOR)

        height = 0
        for line in self.wordwrap(finallines):
            text = self.FONT.render(line, True, self.TEXT_COLOR)
            surface.blit(text, ((self.RECT.width - text.get_width()) / 2, height))
            height += self.FONT.size(line)[1]

        self.surface.blit(surface, (self.X, 10))

class Input():
    def __init__(self, surface):
        self.prompt = ''
        self.FONT = pg.font.Font('Fonts/rpg.ttf', 50)
        self.WIDTH = surface.get_size()[0] / 1.2
        self.HEIGHT = surface.get_size()[1] / 8
        self.X = (surface.get_size()[0] - self.WIDTH) / 2
        self.Y = surface.get_size()[1] - self.HEIGHT
        self.surface = pg.Surface((self.WIDTH, self.HEIGHT), pg.SRCALPHA)

    def draw(self, surface):
        self.surface.fill((0,0,0, 120))
        text = self.FONT.render(self.prompt, True, (180,150,0))
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

class Word():
    def __init__(self, surface, word):
        self.BG_COLOR = (0,0,0, 80)
        self.FONT = pg.font.Font('Fonts/comic.ttf', 40)
        self.HI_COLOR = (200,100,100)
        self.DEF_COLOR = (100,100,200)

        self.color = self.DEF_COLOR
        self.surface = pg.Surface((self.FONT.size(word)[0], self.FONT.size(word)[1]), pg.SRCALPHA)
        self.word = word
        self.x = random.randint(0, surface.get_size()[0] - self.FONT.size(word)[0])
        self.y = -50    #Out of the screen

    def draw(self, speed, surface):
        self.text = self.FONT.render(self.word, True, self.color)
        self.surface.fill((self.BG_COLOR))
        self.surface.blit(self.text, (0,0))
        surface.blit(self.surface, (self.x, self.y))
        self.y += speed
        if self.y > surface.get_size()[1]:
            return 'hit'

    def highlight(self):
        self.color = self.HI_COLOR

    def unhighlight(self):
        self.color = self.DEF_COLOR

class Notify():
    def __init__(self, word, x, y, style='green'):
        self.x = x
        self.y = y
        self.alpha = 255
        self.FONT = pg.font.Font('Fonts/comic.ttf', 40)
        self.word = str(word)
        self.surface = pg.Surface((self.FONT.size(self.word)[0], self.FONT.size(self.word)[1]))
        self.surface.set_alpha(150)
        if style == 'green':
            self.color = (100,200,100)
        elif style == 'red':
            self.color = (200,100,100)

    def draw(self, surface):
        if self.alpha > 0:
            self.alpha -= 3
            if self.alpha < 0:
                self.alpha = 0
        self.surface.set_alpha(self.alpha)
        bg_color = (0,0,0, self.alpha)
        self.text = self.FONT.render(self.word, True, self.color)
        self.surface.fill((bg_color))
        self.surface.blit(self.text, (0,0))
        surface.blit(self.surface, (self.x, self.y))
        self.y -= 1

class BattleStats():
    def __init__(self, surface):
        self.FONT = pg.font.Font('Fonts/rpg.ttf', 50)
        tempWidth = 2.2
        self.WIDTH = surface.get_size()[0] / tempWidth
        self.HEIGHT = surface.get_size()[1] / 1.1
        self.X = []
        self.X.append((tempWidth / 4 - 1/2) * self.WIDTH)
        self.X.append((tempWidth / 4 * 3 - 1/2) * self.WIDTH)
        self.Y = (surface.get_size()[1] - self.HEIGHT) / 1.3
        self.surface = []
        self.surface.append(pg.Surface((self.WIDTH, self.HEIGHT), pg.SRCALPHA))
        self.surface.append(pg.Surface((self.WIDTH, self.HEIGHT), pg.SRCALPHA))
        self.picture = []
        self.picture.append(pg.image.load('Images/menu.jpg'))
        self.picture.append(pg.image.load('Images/menu.jpg'))

    def draw(self, surface, pers, mob):
        color = (200,100,100)
        for i in range(2):
            self.surface[i].fill((0,0,0, 120))
            if i == 0:
                text = self.FONT.render('HP: {0}/{1}'.format(int(pers.hp), int(pers.maxhp)), True, color)
                left = pg.Surface((int(self.surface[i].get_size()[0] * pers.hp / pers.maxhp), 30))
                gauge = pg.Surface((int(self.surface[i].get_size()[0] * (pers.maxhp - pers.hp) / pers.maxhp), 30))
            else:
                text = self.FONT.render('HP: {0}/{1}'.format(int(mob.hp), int(mob.maxhp)), True, color)
                left = pg.Surface((int(self.surface[i].get_size()[0] * mob.hp / mob.maxhp), 30))
                gauge = pg.Surface((int(self.surface[i].get_size()[0] * (mob.maxhp - mob.hp) / mob.maxhp), 30))
            self.surface[i].blit(text, (20, 20))
            left.set_alpha(100)
            gauge.set_alpha(100)
            left.fill((200,255,200))
            gauge.fill((255,200,200))
            self.surface[i].blit(left, (0,0))
            self.surface[i].blit(gauge, (left.get_size()[0], 0))
            self.surface[i].blit(self.picture[i], (50, 50))
            pg.draw.rect(self.surface[i], (255,255,255), pg.Rect(0,0,gauge.get_size()[0]+left.get_size()[0],100), 1)
            surface.blit(self.surface[i], (self.X[i], self.Y))
