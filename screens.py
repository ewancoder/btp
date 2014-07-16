import os
import random

import pygame as pg

import classes
import data
import interface

class Menu():
    BG = pg.image.load('Images/menu.jpg')
    MUSIC = pg.mixer.Sound('Music/menu.ogg')
    
    def __init__(self, surface):
        self.surface = surface
        MAIN_MENU = (
            ['Start / Load Game', lambda: setattr(self, 'ret', 'login')],
            ['Settings', lambda: setattr(self.menu, 'now', 1)],
            ['Quit', lambda: quit()]
        )
        SETTINGS_MENU = (
            ['This is settings example', lambda: print('There will be settings.')],
            ['Back', lambda: setattr(self.menu, 'now', 0)]
        )
        MENU = (
            MAIN_MENU,
            SETTINGS_MENU
        )
        self.menu = interface.Menu(MENU)

    def loop(self):
        clock = pg.time.Clock()
        #Returns its value (exits Menu) if not ''
        self.ret = ''
        x, dx = 0, 1

        while True:
            clock.tick(30)
            if self.ret != '':
                return self.ret

            events = pg.event.get()
            for e in events:
                if e.type == pg.QUIT:
                    quit()
            self.menu.events(events)

            if not pg.mixer.get_busy():
                self.MUSIC.play(-1)
            x += dx
            if x > self.BG.get_size()[0] - self.surface.get_size()[0] or x <= 0:
                dx *= -1

            self.surface.fill(0)
            self.surface.blit(self.BG, (-x, 0))
            self.menu.draw(self.surface)

            pg.display.flip()

class Login():
    TEXT = 'Tell me your name, Stranger!\nIf you are new here, I will tell you a story, and then you will step into this dangerous world, otherwise you will find yourself onto the place you left behind last time...'
    BG = pg.image.load('Images/login.jpg')

    def __init__(self, surface):
        self.message = interface.Message(surface)
        self.parchment = interface.Input(surface)
        self.surface = surface

    def loop(self):
        clock = pg.time.Clock()
        self.parchment.prompt = ''
        x, dx = 0, 1

        while True:
            clock.tick(30)
            events = pg.event.get()
            for e in events:
                if e.type == pg.QUIT:
                    quit()
                elif e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
                    return ''
            name = self.parchment.events(events) #inputEvent
            if name not in (None, ''):
                return name

            self.surface.fill(0)
            self.surface.blit(self.BG, (-x,0))
            x += dx
            if x > self.BG.get_size()[0] - self.surface.get_size()[0]:
                dx = 0
            self.message.draw(self.TEXT)
            self.parchment.draw(self.surface)

            pg.display.flip()

class World():
    def __init__(self, surface):
        self.data = data.Data()
        self.introIndex = 0
        self.musicOldName = ''
        self.surface = surface
        self.inputBox = interface.Input(surface)
        self.message = interface.Message(surface)

    #Passing pers, and not persPlace, just for future extension
    def update(self, pers):
        self.pers = pers
        #self.time = 0
        self.data.update(self.pers)
        if self.pers.place[:5] == 'intro':
            self.intro = True
            place = self.pers.place[5:]
            if self.introIndex < len(getattr(self.data, eval('place'))):
                self.PLACE = None
                self.text = getattr(self.data, eval('place'))[self.introIndex]
                self.bg = pg.image.load('Images/Intro/' + place + str(self.introIndex) + '.jpg')
                if self.introIndex+1 < len(getattr(self.data, eval('place'))):
                    self.introIndex += 1
                else:
                    self.introIndex = 0
                    self.PLACE = next(item for item in self.data.place if item['Id'] == self.pers.place)
            musicName = place
        else:
            self.intro = False
            place = self.pers.place
            self.PLACE = next(item for item in self.data.place if item['Id'] == place)
            self.bg = pg.image.load('Images/' + place + '.jpg')
            self.text = self.PLACE['Text']
            musicName = os.path.basename(os.path.dirname('Images/' + place + '.jpg'))
            #self.time += self.PLACE['Time'] if 'Time' in self.PLACE.keys() else 10

        if self.musicOldName != musicName:
            self.musicOldName = musicName
            music = pg.mixer.Sound('Music/' + musicName + '.ogg')
            if pg.mixer.get_busy():
                pg.mixer.stop()
            music.play()

    def loop(self):
        clock = pg.time.Clock()
        x, dx = 0, 1

        while True:
            clock.tick(30)
            events = pg.event.get()
            for e in events:
                if e.type == pg.QUIT:
                    exit()
                if e.type == pg.KEYDOWN:
                    if e.key == pg.K_RETURN and self.intro == True:
                        return self.PLACE, None
            if self.intro == False:
                e = self.inputBox.events(events)
                if e!= None and e in self.PLACE['Move']:
                    moveIndex = self.PLACE['Move'].index(e)
                    move = next(item for item in self.data.place if item['Id'] == self.PLACE['Goto'][moveIndex])
                    self.pers.time += move['Time'][moveIndex] if 'Time' in move else 10
                    moveto = self.PLACE['Goto'][self.PLACE['Move'].index(e)]
                    newplace = next(item for item in self.data.place if item['Id'] == moveto)
                    return newplace, moveto

            self.surface.fill(0)
            self.surface.blit(self.bg, (-x,0))
            x += dx
            if x > self.bg.get_size()[0] - self.surface.get_size()[0]:
                dx = 0

            self.message.draw(self.text)
            if self.intro == False:
                self.inputBox.draw(self.surface)

            pg.display.flip()

class Battle():
    def __init__(self, surface):
        self.surface = surface

    def loop(self, pers):
        self.bg = pg.image.load('Images/Battle/' + os.path.basename(os.path.dirname(pers.place)) + '.jpg')

        clock = pg.time.Clock()
        mob = classes.Mob()
        d = data.Data()
        d.update(pers)
        self.started = False
        prompt = ''
        words, bwords, speed, notifications = [], [], [], []
        words.append(random.choice(data.words))
        bwords.append(interface.Word(self.surface, words[-1]))
        try:
            spd = next(item for item in d.place if item['Id'] == pers.place)['Mobs']['Speed']
        except:
            spd = 0
        speed.append(spd)

        self.stats = interface.BattleStats(self.surface, mob)

        def updateWord():
            if words[self.index].startswith(e.unicode):
                words[self.index] = words[self.index][1:]
                if words[self.index] == '':
                    persHit = random.randint(int((pers.atk - pers.atk / 3) * 1000), int((pers.atk + pers.atk / 3) * 1000)) / 1000
                    persHit *= self.length / 10
                    mob.hp -= persHit
                    #UPDATE STATE OF BATTLE (hit monster + animate it)
                    bwords[self.index].word = words[self.index]
                    #go to next word
                    self.started = False
                    #It is the condition lol :D
                    #words[self.index] = ''
                    notifications.append(interface.Notify('{:.2f}'.format(persHit), bwords[self.index].x, bwords[self.index].y))
                    self.index = None
                else:
                    bwords[self.index].word = words[self.index]
        
        addword = pg.USEREVENT+1
        pg.time.set_timer(addword, 1000)
        self.index = None

        mob.hp = mob.maxhp
        while mob.hp > 0 and pers.hp > 0:
            clock.tick(30)

            events = pg.event.get()
            for e in events:
                if e.type == pg.QUIT:
                    quit()
                if e.type == pg.KEYDOWN:
                    if e.unicode.isalpha():
                        if not self.started:
                            for ind, word in enumerate(words):
                                if word.startswith(e.unicode):
                                    self.index = ind
                                    break
                            if self.index != None:
                                if bwords[self.index].word.startswith(e.unicode):
                                    bwords[self.index].highlight()
                                    self.started = True
                                    self.length = len(words[self.index])
                                    updateWord()
                        else:
                            updateWord()
                if e.type == addword:
                    #Horrible piece of shit
                    temp = 0
                    while True:
                        temp += 1
                        go = True
                        newWord = random.choice(data.words)
                        for word in words:
                            if word.startswith(newWord[:1]):
                                go = False
                        if go or temp == 100:
                            temp = 0
                            break
                    words.append(newWord)
                    bwords.append(interface.Word(self.surface, words[-1]))
                    speed.append(spd)

            self.surface.fill(0)
            self.surface.blit(self.bg, (0,0))

            #STATS
            if pers.hp < 1:
                pers.hp = 0
            if mob.hp < 1:
                mob.hp = 0
            self.stats.draw(self.surface, pers, mob)

            #NOTIFICATIONS
            for n in notifications:
                if n.y > -n.surface.get_size()[1]:
                    n.draw(self.surface)
                else:
                    del n

            #WORDS
            for ind, w in enumerate(bwords):
                if words[ind] != '':
                    if w.draw(speed[ind], self.surface) == 'hit':
                        if self.started == True:
                            self.index = None
                            #go to next word
                            self.started = False
                            for ww in bwords:
                                ww.unhighlight()
                        words[ind] = ''
                        mobHit = random.randint(int((mob.atk - mob.atk / 3) * 1000), int((mob.atk + mob.atk / 3) * 1000)) / 1000
                        pers.hp -= 10 * mobHit
                        notifications.append(interface.Notify('{:.2f} [HH]'.format(mobHit + 10), bwords[ind].x, bwords[ind].y - 50, 'red'))

            pg.display.flip()

        if pers.hp == 0:
            pers.hp = pers.maxhp * .2
            pers.experience -= pers.experience / 10
            camp = next(item for item in d.place if item['Id'].startswith(basename(pers.place)))['Id']

        return pers
