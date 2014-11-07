import os
import random

import pygame as pg

import classes
import data
import interface

SIZE = (1400,800)

class Hints():
    def __init__(self, offset=0):
        #Need to use __init__ for different Hints instances for menu/login/world/battle
        self.hints = []
        self.ind = [] #For indexed items
        self.count = 0 #count for hidden hints
        self.offset = offset

    def add(self, text, index, delay=0):
        if text == '':
            text = 'H' + str(len(self.hints))
        self.hints.append(interface.Hint(text, self.offset + (len(self.hints) - self.count)*40, delay=delay))
        self.ind.append(index)

    def draw(self, surface, settings): #for settings.hints
        if settings.hints == True:
            for hint in self.hints:
                hint.draw(surface)

    def hide(self, index=0):
        try:
            if index == 0:
                ind = self.count
            else:
                ind = self.ind.index(index)
            self.hints[ind].hide = True
            self.count += 1
            for i in range(ind+1,len(self.hints)):
                self.hints[i].shift = 40
            self.ind[ind] = "hidden"
        except:
            pass

class Menu():
    BG = pg.transform.scale(pg.image.load('Images/menu.jpg'), SIZE)
    MUSIC = pg.mixer.Sound('Music/menu.ogg')
    
    def __init__(self, surface):
        self.surface = surface
        MAIN_MENU = (
            ['Start / Load Game', lambda: setattr(self, 'ret', 'login'), ''],
            ['Settings', lambda: setattr(self.menu, 'now', 1), ''],
            ['Quit', lambda: quit(), '']
        )
        SETTINGS_MENU = (
            ['Show hints', 'hints', 'checkbox'],
            ['Back', lambda: setattr(self.menu, 'now', 0), '']
        )
        MENU = (
            MAIN_MENU,
            SETTINGS_MENU
        )
        self.menu = interface.Menu(MENU)
        self.hints = Hints()
        self.hints.add('Use J/K to move Down/Up', 'jk')
        self.hints.add('Use L (or Enter) to switch', 'lenter', 60)
        self.hints.add('Version 0.01 alpha', 'version', 120)

    def loop(self, settings, oldname=''): #settings is settings object (current state already, save-loaded outside, in game.py file)
        clock = pg.time.Clock()
        #Returns its value (exits Menu) if not ''
        self.ret = ''

        while True:
            clock.tick(30)
            if self.ret != '':
                return self.ret

            events = pg.event.get()
            for e in events:
                if e.type == pg.QUIT:
                    quit()
                if e.type == pg.KEYDOWN:
                    if e.key == pg.K_j or e.key == pg.K_k:
                        self.hints.hide('jk')
                    elif e.key == pg.K_l or e.key == pg.K_RETURN:
                        self.hints.hide('lenter')
                    elif e.key == pg.K_F12 and oldname != '':
                        self.ret = 'back_' + oldname
            toggle = self.menu.events(events)
            if toggle != None:
                self.ret = toggle

            if not pg.mixer.get_busy():
                self.MUSIC.play(-1)

            self.surface.fill(0)
            self.surface.blit(self.BG, (-10, -10))
            self.menu.draw(self.surface, settings) #Pass settings to next cycle (which draws based on True/False value)
            self.hints.draw(self.surface, settings)

            pg.display.flip()

class Login():
    TEXT = 'Tell me your name, Stranger!\nIf you belong to this place, you\'ll find yourself into the place you left behind last time, otherwise you shall begin your journey in the forest of damned...'
    BG = pg.transform.scale(pg.image.load('Images/login.jpg'), SIZE)

    def __init__(self, surface):
        self.message = interface.Message(surface)
        self.parchment = interface.Input(surface)
        self.surface = surface

    def loop(self):
        clock = pg.time.Clock()
        self.parchment.prompt = ''

        while True:
            clock.tick(30)
            events = pg.event.get()
            for e in events:
                if e.type == pg.QUIT:
                    quit()
                elif e.type == pg.KEYDOWN:
                    if e.key == pg.K_ESCAPE:
                        return ''
                    elif e.key == pg.K_F1:
                        self.message.hid_timer = 500
                        self.message.hidden = not self.message.hidden
            name = self.parchment.events(events) #inputEvent
            if name not in (None, ''):
                return name

            self.surface.fill(0)
            self.surface.blit(self.BG, (-10,-10))
            self.message.draw(self.TEXT)
            self.parchment.draw(self.surface)

            pg.display.flip()

class World():
    def __init__(self, surface):
        self.t_counter = 0 #Transition counter (255 -> 0)
        #self.started = False #Kostyl, if True - works 1 time for long black-intro in game world
        self.away_counter = 0

        self.data = data.Data()
        self.introIndex = 0
        self.musicOldName = ''
        self.surface = surface
        self.message = interface.Message(surface)
        self.battleScreen = Battle(surface)
        self.hints = Hints(interface.Message.HEIGHT + 10)

    #Passing pers, and not persPlace, just for future extension
    def update(self):
        self.dx = 0
        self.dy = 0
        self.locked = -1 #for locking words-movement
        self.moves = []
        #self.pers = pers
        #self.time = 0
        self.data.update(self.pers)

        try:
            self.oldbg = self.bg
            self.t_counter = 255
        except:
            self.t_counter = 0

        #Outside of if-loop
        place = self.pers.place
        self.PLACE = next(item for item in self.data.place if item['Id'] == place)

#        if self.pers.place[:5] == 'intro':
#            self.intro = True
#            #place = self.pers.place
#            if self.introIndex < len(getattr(self.data, eval('place'))):
#                self.PLACE = None
#                self.text = getattr(self.data, eval('place'))[self.introIndex]
#                self.bg = pg.transform.scale(pg.image.load('Images/Intro/' + place + str(self.introIndex) + '.jpg'), SIZE)
#
#                if self.introIndex+1 < len(getattr(self.data, eval('place'))):
#                    self.introIndex += 1
#                else:
#                    self.introIndex = 0
#                    self.PLACE = next(item for item in self.data.place if item['Id'] == self.pers.place)
#                    self.t_counter = 255
#                    self.started = True
#            musicName = place

        if 'Intros' in self.PLACE.keys() and self.pers.place not in self.pers.intros:
            self.intro = True
            if self.introIndex < len(self.PLACE['Intros']):
                self.text = self.PLACE['Intros'][self.introIndex]
                self.bg = pg.transform.scale(pg.image.load('Images/Intro/' + place + str(self.introIndex) + '.jpg'), SIZE)
                self.introIndex += 1
            else:
                self.introIndex = 0
                self.pers.intros += ', ' + self.pers.place
            musicName = os.path.basename(os.path.dirname('Images/' + place + '.jpg'))

        if 'Intros' not in self.PLACE.keys() or self.pers.place in self.pers.intros:
            #self.started = False
            self.intro = False
            self.text = self.PLACE['Text']
            self.bg = pg.transform.scale(pg.image.load('Images/' + place + '.jpg'), SIZE)
            musicName = os.path.basename(os.path.dirname('Images/' + place + '.jpg'))
            #self.time += self.PLACE['Time'] if 'Time' in self.PLACE.keys() else 10
            for ind, move in enumerate(self.PLACE['Moves']):
                self.moves.append(interface.Move(move[0], move[1], ind))
            #Begin battle (testing section)
            try:
                if random.randrange(0,100) < self.PLACE['Mobs']['Chance']:
                    self.pers = self.battleScreen.loop(self.pers, self.bg)
            except:
                pass

        if self.musicOldName != musicName:
            self.musicOldName = musicName
            music = pg.mixer.Sound('Music/' + musicName + '.ogg')
            if pg.mixer.get_busy():
                pg.mixer.stop()
            music.play()

        try:
            if self.PLACE['Id'] not in self.pers.hints.split():
                for ind, hint in enumerate(self.PLACE['Hints']):
                    self.hints.add(hint, '', ind*60)
                #self.pers.hints.append(self.PLACE['Id'])
                    #APPENDING DOESNT WORK SOMEHOW :(
                self.pers.hints = self.pers.hints + ', ' + self.PLACE['Id']
                print(self.pers.hints)
        except:
            pass

        #For image centered
        self.x = (self.surface.get_width() / 2) - (self.bg.get_width() / 2)
        self.y = (self.surface.get_height() / 2) - (self.bg.get_height() / 2)

        #Finally, save pers
        self.pers = self.pers.save()

    def loop(self, settings):
        clock = pg.time.Clock()

        while True:
            clock.tick(30)
            events = pg.event.get()
            for e in events:
                if e.type == pg.QUIT:
                    exit()
                if e.type == pg.KEYDOWN:
                    if self.intro == True and e.key == pg.K_RETURN:
                        self.update()
                    elif self.intro == True and e.key == pg.K_SPACE:
                            self.introIndex = 0
                            self.pers.intros += ', ' + self.pers.place
                            self.update()
                    elif e.key == pg.K_F1:
                        self.message.hid_timer = 500
                        self.message.hidden = not self.message.hidden
                    elif e.key == pg.K_BACKSPACE:
                        self.hints.hide()
                    elif e.key == pg.K_F12:
                        return
            for index, move in enumerate(self.moves):
                if self.locked == index or self.locked == -1:
                    ind = move.events(events)
                    if ind != None:
                        moveLocal = self.PLACE['Moves'][ind]
                        self.locked = ind
                        if ind != -1:
                            move.progress += .01 * self.pers.speed
                        if move.progress >= 1:
                            #for move in self.moves:
                            #    move.away = True
                            move.away = True #Moves only an item you chose
                            self.away_counter += 1
                        else:
                            if moveLocal[1] == 'left':
                                if self.x < -10:
                                    self.dx -= 5 * self.pers.speed
                            elif moveLocal[1] == 'right':
                                self.dx += 5 * self.pers.speed

            if self.away_counter > 0:
                self.away_counter += 1
            if self.away_counter > 10:
                self.away_counter = 0
                self.pers.place = moveLocal[2]
                self.update()
                #self.pers = self.pers.save()

            if self.intro == False:
                pass
                #REPROGRAM TO MOVE CHARACTER OVER SCREEN

            #LOGIC FOR ALL SPRITES

            if self.dx > 0:
                if self.x > self.surface.get_width() - self.bg.get_width() + 10:
                    self.x -= 1
                else:
                    self.x = self.surface.get_width() - self.bg.get_width() + 10
                self.dx -= 1
            if self.dx < 0:
                if self.x < -10:
                    self.x += 1
                else:
                    self.x = -10
                self.dx += 1

            #if self.dy > 0:
            #    self.y -= 1
            #    self.dy -= 1
            #if self.dy < 0:
            #    self.y += 1
            #    self.dy += 1

            self.surface.fill(0)
            if self.intro == True:
                x = -10
                y = -10
                try:
                    self.surface.fill((255,255,255))
                    self.oldbg.set_alpha(self.t_counter)
                    self.surface.blit(self.oldbg, (x,y))
                except:
                    pass
            else:
                #Should calculate exact position
                x = self.x
                y = self.y

            if self.away_counter > 0:
                self.bg.set_alpha(255 - self.away_counter * 20)
            else:
                self.bg.set_alpha(255-self.t_counter)
            self.surface.blit(self.bg, (x,y))
            self.t_counter -= 20

            #DRAW ALL SPRITES
            
            for move in self.moves:
                move.draw(self.surface, self.x)

            self.message.draw(self.text)
            self.hints.draw(self.surface, settings)

            pg.display.flip()

class Battle():
    def __init__(self, surface):
        self.surface = surface

    def loop(self, pers, bg):
        #self.bg = pg.transform.scale(pg.image.load('Images/Battle/' + os.path.basename(os.path.dirname(pers.place)) + '.jpg'), SIZE)
        self.bg = bg

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
            spd = 1
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
