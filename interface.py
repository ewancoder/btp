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
    def __init__(self, surface):
        self.BG_COLOR = (0,0,0, 80)
        self.TEXT_COLOR = (100,100,200)
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


