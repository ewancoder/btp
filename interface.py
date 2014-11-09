import random #For Word X-positioning
import data #for random words

import classes #for menu settings

import pygame as pg

import constants

class Menu():
    X, Y = 10, 10
    DCOLOR, HCOLOR = (0, 0, 0), (200, 200, 200)
    FONT = pg.font.Font('Fonts/rpg.otf', 40)
    SELECT_SOUND = pg.mixer.Sound('Sounds/door.ogg')
    SWITCH_SOUND = pg.mixer.Sound('Sounds/click.ogg')

    out = 150 #for X changing
    selected = 0    #Index of selected menu item
    unselected = 0  #Index of unselected menu (for cool effects)
    now = 0         #Index of menu which is showing NOW
    unsel_timer = 0   #30 for 1 sec --- sel. timer for cool effects
    sel_timer = 0


    def __init__(self, items):
        self.ITEMS = items
        self.update()

    def update(self):
        self.out = 150
        self.selected = 0
        self.unselected = 0
        self.items = [{'Label': i[0], 'Action': i[1], 'Type': i[2]} for i in self.ITEMS[self.now]]

    def draw(self, surface, settings):
        offset = 0 #Incremental variable for making y-difference
        for index, i in enumerate(self.items):
            if self.selected == index:
                if self.sel_timer >= 0:
                    self.sel_timer -= 4
                    color = (self.HCOLOR[0] + int(self.sel_timer*1.5),
                             self.HCOLOR[1],
                             self.HCOLOR[2])
                else:
                    color = self.HCOLOR
            elif self.unselected == index:
                if self.unsel_timer > 1:
                    self.unsel_timer -= 1
                    color = (self.HCOLOR[0] - int(self.HCOLOR[0] / self.unsel_timer),
                             self.HCOLOR[1] - int(self.HCOLOR[1] / self.unsel_timer),
                             self.HCOLOR[2] - int(self.HCOLOR[2] / self.unsel_timer))
                else:
                    color = self.DCOLOR
            else:
                color = self.DCOLOR
            if i['Type'] == 'checkbox':
                if getattr(settings, i['Action']) == False:
                    text = self.FONT.render('X ' + i['Label'], True, color)
                else:
                    text = self.FONT.render('O ' + i['Label'], True, color)
            else:
                text = self.FONT.render(i['Label'], True, color)
            if self.out > 0:
                surface.blit(text, (self.X-self.out, self.Y + offset))
                self.out -= 10
            else:
                surface.blit(text, (self.X, self.Y + offset))
            offset += self.FONT.get_height()

    def events(self, events):
        for e in events:
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_DOWN or e.key == pg.K_j or e.key == pg.K_s:
                    if self.selected < len(self.items) - 1:
                        self.SWITCH_SOUND.play()
                        self.unselected = self.selected
                        self.selected += 1
                        self.unsel_timer = 10
                        self.sel_timer = 40
                elif e.key == pg.K_UP or e.key == pg.K_k or e.key == pg.K_w:
                    if self.selected > 0:
                        self.SWITCH_SOUND.play()
                        self.unselected = self.selected
                        self.selected -= 1
                        self.unsel_timer = 10
                        self.sel_timer = 40
                elif e.key == pg.K_RETURN or e.key == pg.K_SPACE or e.key == pg.K_l:
                    self.SELECT_SOUND.play()
                    if self.items[self.selected]['Type'] == '':
                        self.items[self.selected]['Action']()
                    elif self.items[self.selected]['Type'] == 'checkbox':
                        return self.items[self.selected]['Action']
                    self.update()
                    
class ProgressBar():
    def __init__(self, width, height=4, color=(240,100,100, 220), secondColor=(0,0,0, 90)):
        self.width = width
        self.height = height
        self.color = color
        self.secondColor = secondColor
        self.surface = pg.Surface((width,self.height), pg.SRCALPHA, 32)

    def draw(self, surface, xy, progress):
        (x, y) = xy
        self.surface.fill(self.secondColor)
        #pg.draw.rect(self.surface, (255,255,255), pg.Rect(0,0,self.width,self.height))
        pg.draw.rect(self.surface, self.color, pg.Rect(0,0,int(self.width*progress),self.height))
        pg.draw.rect(self.surface, (100,0,0), pg.Rect(0,0,self.width,self.height), 1)
        surface.blit(self.surface, (x, y))

class Move():
    ALPHA = 90
    A_TITLE_COLOR = (200,200,100) #Activated title
    TITLE_COLOR = (200,100,100) #Not activated title, hardly used yet
    FONT_COLOR = (200,200,200)
    FONT = pg.font.Font('Fonts/rpg.otf', 22)

    def __init__(self, text, style):
        self.away = False #If true - moveaway with cool effect (when progress >= 1)
        self.locked = False
        self.locked_color = 0 #RED-increment for animation of locking
        self.text = text
        self.style = style
        #self.rtext = '' #This variable created automatically by screens.py
        self.width = self.FONT.size(self.text)[0] + 20

        self.RECT = pg.Rect((0, 0, self.width, self.FONT.size(text)[1]))
        self.surface = pg.Surface(self.RECT.size, pg.SRCALPHA, 32)
        self.rRECT = pg.Rect((0, 0, self.width, self.FONT.size(text)[1]))
        self.rsurface = pg.Surface(self.rRECT.size, pg.SRCALPHA, 32)

        self.progressBar = ProgressBar(self.width)
        self.progress = 0

    def draw(self, surface):
        if self.style == 'right':
            if self.away == False:
                self.x = surface.get_width() - self.width - 30
            elif self.x < surface.get_width():
                self.x += 30
            self.y = surface.get_height() - self.RECT.size[1]*2 - 60
        elif self.style == 'left':
            if self.away == False:
                self.x = 20
            elif self.x > -self.width:
                self.x -= 30
            self.y = surface.get_height() - self.RECT.size[1]*2 - 60
        elif self.style == 'top':
            self.x = surface.get_width() / 2 - self.width / 2
            if self.away == False:
                self.y = Message.HEIGHT + 30
            elif self.y > -60:
                self.y -= 30
        elif self.style == 'bottom':
            self.x = surface.get_width() / 2 - self.width / 2
            if self.away == False:
                self.y = surface.get_height() - self.RECT.size[1]*2 - 30
            elif self.y < surface.get_height():
                self.y += 30
        self.progressBar.draw(surface, (self.x, self.y), self.progress)

        self.surface.fill((0,0,0, self.ALPHA))
        self.rsurface.fill((self.locked_color,0,0, self.ALPHA))
        if self.locked and self.locked_color < 70:
            self.locked_color += 10
        elif not self.locked and self.locked_color > 0:
            self.locked_color -= 10
        text = self.FONT.render(self.text, True, self.A_TITLE_COLOR)
        rtext = self.FONT.render(self.rtext, True, self.FONT_COLOR)
        self.surface.blit(text, ((self.RECT.width - text.get_width()) / 2, 0))
        self.rsurface.blit(rtext, (10, 0))
        surface.blit(self.surface, (self.x, self.y))
        surface.blit(self.rsurface, (self.x, self.y + self.RECT.height))

class Attack():
    ALPHA = 90
    A_TITLE_COLOR = (200,200,100) #Activated title
    TITLE_COLOR = (200,100,100) #Not activated title, hardly used yet
    FONT_COLOR = (200,200,200)
    FONT = pg.font.Font('Fonts/rpg.otf', 32)

    def __init__(self, style):
        self.away = False #If true - moveaway with cool effect (when progress >= 1)
        self.locked = False
        self.locked_color = 0 #RED-increment for animation of locking
        self.style = style
        self.rtext = ''
        self.width = 140
        self.curr_angle = 0
        self.angle = 5 #Changeable angle of rotation
        self.da = .2

        self.rRECT = pg.Rect((0, 0, self.width, self.FONT.size('')[1]))
        self.rsurface = pg.Surface(self.rRECT.size, pg.SRCALPHA, 32)

        #For fancy and useless different-angles animation
        if style == 'torso':
            self.curr_angle = 2
        elif style == 'groin':
            self.curr_angle = 4
        elif style == 'legs':
            self.curr_angle = -2

    def fixX(self, surf_width):
        """Function to change self.x in Defence(Attack) class"""
        self.rsurface.fill((self.locked_color,0,0, self.ALPHA))

    def draw(self, surface):
        if self.style == 'head':
            if self.away == False:
                self.y = surface.get_height() / 5
                self.x = surface.get_width() / 2 + 100
            elif self.x < surface.get_width():
                self.x += 30
        elif self.style == 'torso':
            if self.away == False:
                self.y = surface.get_height() / 5 * 2
                self.x = surface.get_width() / 2 + 100
            elif self.x < surface.get_width():
                self.x += 30
        elif self.style == 'groin':
            if self.away == False:
                self.y = surface.get_height() / 5 * 3
                self.x = surface.get_width() / 2 + 100
            elif self.x < surface.get_width():
                self.x += 30
        elif self.style == 'legs':
            if self.away == False:
                self.y = surface.get_height() / 5 * 4
                self.x = surface.get_width() / 2 + 100
            elif self.x < surface.get_width():
                self.x += 30

        self.curr_angle += self.da
        if self.curr_angle > self.angle or self.curr_angle < -self.angle:
            self.da *= -1

        self.fixX(surface.get_width())

        if self.locked and self.locked_color < 70:
            self.locked_color += 10
        elif not self.locked and self.locked_color > 0:
            self.locked_color -= 10
        rtext = self.FONT.render(self.rtext, True, self.FONT_COLOR)
        self.rsurface.blit(rtext, (10, 0))
        surface.blit(pg.transform.rotate(self.rsurface, self.curr_angle), (self.x, self.y + self.rRECT.height))

class Defence(Attack):
    def fixX(self, surf_width):
        self.rsurface.fill((0,0,self.locked_color, self.ALPHA))
        self.x = surf_width - self.x - self.width

class Hint():
    ALPHA = 180
    FONT = pg.font.Font('Fonts/rpg.otf', 30)

    def __init__(self, text, y=10, x=10, style='default', delay=0):
        self.text = str(text)
        self.x = x
        self.y = y + 30
        self.Y = y + 10
        self.alpha = 0
        self.surface = pg.Surface((self.FONT.size(self.text)[0] + 10, self.FONT.size(self.text)[1]))
        self.surface.set_alpha(0)
        if style == 'default':
            self.color = (200,100,100)
        self.delay = delay
        self.hide = False
        self.shift = 0

    def draw(self, surface):
        if self.delay>0:
            self.delay -= 1
        else:
            x = surface.get_width() - self.surface.get_width() - self.x
            if self.alpha < self.ALPHA and self.hide == False:
                self.alpha += 4
            if self.y > self.Y:
                self.y -= 1
            self.surface.set_alpha(self.alpha)
            bg_color = (0,0,0, self.alpha)
            self.rend_text = self.FONT.render(self.text, True, self.color)
            self.surface.fill((bg_color))
            self.surface.blit(self.rend_text, (5,0))
            surface.blit(self.surface, (x, self.y))

        if self.hide == True:
            if self.alpha > 0:
                self.alpha -= 8
                if self.alpha < 0:
                    self.alpha = 0

        if self.shift > 0:
            self.shift -= 1
            self.y -= 1
            self.Y -= 1

class Message():
    ALPHA = 130
    hidden = False
    hid_timer = 500;
    FONT_COLOR = (200,200,200)
    HEIGHT = 220

    def __init__(self, surface):
        self.RECT = pg.Rect((0, 0, surface.get_size()[0] - 10*2, self.HEIGHT))
        self.X = surface.get_size()[0] / 2 - self.RECT.width / 2
        self.setFontSize(30)
        self.surface = surface

    def setFontSize(self, size):
        self.FONT = pg.font.Font('Fonts/rpg.otf', size)

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
        if self.hidden == False or (self.hidden == True and self.hid_timer < 1000):
            surface = pg.Surface(self.RECT.size, pg.SRCALPHA, 32)
            surface.fill((0,0,0, self.ALPHA))

            height = 0
            for line in self.wordwrap(finallines):
                text = self.FONT.render(line, True, self.FONT_COLOR)
                surface.blit(text, ((self.RECT.width - text.get_width()) / 2, height))
                height += self.FONT.size(line)[1]

            self.surface.blit(surface, (self.X - self.hid_timer, 10))
            if self.hidden == False and self.hid_timer > 0:
                self.hid_timer -=100
            elif self.hidden == True:
                self.hid_timer +=100

class Input():
    KEY_SOUND = pg.mixer.Sound('Sounds/click.ogg')
    HEIGHT = 150

    def __init__(self, surface):
        self.prompt = ''
        self.FONT = pg.font.Font('Fonts/rpg.ttf', 90)
        self.WIDTH = surface.get_size()[0] / 2
        self.X = (surface.get_size()[0] - self.WIDTH) / 2
        self.Y = surface.get_size()[1]/1.3 - self.HEIGHT/2
        self.surface = pg.Surface((self.WIDTH, self.HEIGHT), pg.SRCALPHA)

    def draw(self, surface):
        self.surface.fill((0,0,0, 120))
        text = self.FONT.render(self.prompt, True, (180,150,40))
        self.surface.blit(text, ((self.WIDTH - text.get_width()) / 2, (self.HEIGHT - text.get_height()) / 2))
        surface.blit(self.surface, (self.X, self.Y))

    def events(self, events):
        for e in events:
            if e.type == pg.KEYDOWN:
                if e.unicode.isalpha():
                    self.prompt += e.unicode
                    self.KEY_SOUND.play()
                elif e.key == pg.K_BACKSPACE:
                    self.prompt = self.prompt[:-1]
                elif e.key == pg.K_RETURN:
                    prompt = self.prompt
                    self.prompt = ''
                    return prompt

class Notify():
    def __init__(self, word, x, y, style='green'):
        self.x = x
        self.y = y
        self.alpha = 255
        self.FONT = pg.font.Font('Fonts/rpg.otf', 40)
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
    def __init__(self, surface, mob):
        self.mobRed = 40 #For flashing
        self.mobBlue = 0 #For flashing
        self.Red = 0
        self.Blue = 40

        self.FONT = pg.font.Font('Fonts/rpg.otf', 16)
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
        self.picture.append(pg.Surface((self.WIDTH * 8/10, self.HEIGHT / 1.3)))
        self.picture[0].blit(pg.transform.scale(pg.image.load('Images/Pers.png'), (500,500)), (0,0))
        self.picture[0].set_colorkey(0)
        self.picture.append(pg.Surface((self.WIDTH * 8/10, self.HEIGHT / 1.3)))
        self.picture[1].blit(pg.transform.scale(pg.image.load('Images/Mobs/' + mob.name + '.png'), (500,500)), (0,0))
        self.picture[1].set_colorkey(0)

        self.hp = ProgressBar(self.WIDTH, 20, (100, 200, 100, 180), (200,100,100, 90))
        self.mobhp = ProgressBar(self.WIDTH, 20, (100, 200, 100, 180), (200,100,100, 90))
        self.mobActivity = ProgressBar(self.WIDTH, 20, (200, 150, 100, 180), (0,0,0, 90))
        self.textcolor = (200,200,0)

    def draw(self, surface, pers, mob):
        if self.mobRed > 40:
            self.mobRed -= 20
        elif self.mobRed < 40:
            self.mobRed = 40
        if self.mobBlue > 0:
            self.mobBlue -= 20
        elif self.mobBlue < 0:
            self.mobBlue = 0
        if self.Blue > 40:
            self.Blue -= 20
        elif self.Blue < 40:
            self.Blue = 40
        if self.Red > 0:
            self.Red -= 20
        elif self.Red < 0:
            self.Red = 0

        self.surface[0].fill((self.Red,0,self.Blue, 90))
        self.surface[1].fill((self.mobRed,0,self.mobBlue, 90))
        self.hp.draw(self.surface[0], (0,0), pers.hp / pers.maxhp)
        self.mobhp.draw(self.surface[1], (0,0), mob.hp / mob.maxhp)
        self.mobActivity.draw(self.surface[1], (0,20), mob.act / constants.MOB_ACT)
        text = [
            self.FONT.render('{0} / {1}'.format(int(pers.hp), int(pers.maxhp)), True, self.textcolor),
            self.FONT.render('{0} / {1}'.format(int(pers.hp), int(pers.maxhp)), True, self.textcolor)
        ]
        for i in range(2):
            self.surface[i].blit(text[i], (self.surface[i].get_width() / 2 - text[i].get_width() / 2,0))
            self.surface[i].blit(self.picture[i], (self.surface[i].get_size()[0] / 10, 120))
            surface.blit(self.surface[i], (self.X[i], self.Y))
