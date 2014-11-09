import os
import random

import pygame as pg

import classes
import data
import interface

import constants

SIZE = constants.BG_SIZE
d = data.Data()

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
        self.away_counter = 0

        self.introIndex = 0
        self.musicOldName = ''
        self.surface = surface
        self.message = interface.Message(surface)
        self.hints = Hints(interface.Message.HEIGHT + 10)
        self.pershp = interface.ProgressBar(surface.get_width() / 1.3, 8)

    def randWord(self):
        unique = False
        while not unique:
            unique = True
            word = random.choice(data.words)
            for m in self.moves:
                for rword in m.rtext.split():
                    if word[:1] == rword[:1]:
                        unique = False
        return word

    #Passing pers, and not persPlace, just for future extension
    def update(self):
        self.locked = -1 #for locking words-movement
        self.moves = []
        unique = False
        #self.pers = pers
        #self.time = 0
        #self.data.update(self.pers)
        d.update(self.pers)

        try:
            self.oldbg = self.bg
            self.t_counter = 255
        except:
            self.t_counter = 0

        #Outside of if-loop
        place = self.pers.place
        #self.PLACE = next(item for item in self.data.place if item['Id'] == place)
        self.PLACE = next(item for item in d.place if item['Id'] == place)

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

                rtext = self.randWord()
                for i in range(4):
                    rtext += ' ' + self.randWord()

                self.moves.append(interface.Move(move[0], move[1]))
                self.moves[ind].rtext = rtext

            #Begin battle (testing section)
            #MOVED TO TYPING SECTION
            #try:
            #    if random.randrange(0,100) < self.PLACE['Mobs']['Chance']:
            #        self.pers = self.battleScreen.loop(self.pers, self.bg)
            #except:
            #    pass

        music = pg.mixer.Sound('Music/' + musicName + '.ogg')
        if self.musicOldName != musicName:
            self.musicOldName = musicName
            if pg.mixer.get_busy():
                pg.mixer.stop()
            music.play()
        elif not pg.mixer.get_busy():
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
                    elif e.key == pg.K_ESCAPE and self.locked != -1:
                        while self.moves[self.locked].rtext[:1] != ' ':
                            self.moves[self.locked].rtext = self.moves[self.locked].rtext[1:]
                        self.moves[self.locked].rtext = self.moves[self.locked].rtext[1:] + ' ' + self.randWord()
                        #NEED TO CHECK IT, MAY RUIN EVERYTHING
                        self.moves[self.locked].locked = False
                        #move.locked = False
                        self.locked = -1
                    elif e.unicode.isalpha():
                        for index, move in enumerate(self.moves):
                            if self.locked == -1 or self.locked == index:
                                if move.rtext.startswith(e.unicode):

                                    #HERE IS ALL DONE FOR CURRENT move IF PRESSED KEY, INCLUDING CHANGING TIME AND BATTLE STARTING IF CHANCE IS BIG
                                    move.rtext = move.rtext[1:]

                                    move.locked = True
                                    self.locked = index
                                    moveLocal = self.PLACE['Moves'][index]
                                    try:
                                        move.progress += 1 / (moveLocal[3] / self.pers.speed)
                                    except:
                                        move.progress += 1 / (constants.DISTANCE / self.pers.speed)
                                    #Each stoke adds 1 minute to the time (and to the statistics)
                                    self.pers.time += 1
                                    self.pers.strokes += 1 #Need this separately because time will flow regardless of typing, from other actions too
                                    #HERE IS BATTLE CHANCES ENGAGED (EACH TYPO)
                                    if 'Mobs' in self.PLACE.keys():
                                        if random.randrange(0,100) < self.PLACE['Mobs']['Chance']:
                                            self.pers = Battle(self.surface).loop(self.pers, self.bg)
                                            #IF PERS IS KILLED, MOVE IT TO CAMP (just use update() because pers.hp is 0 already and place is changed within Battle class)

                                    if move.rtext[0] == ' ':
                                        move.rtext = move.rtext[1:] + ' ' + self.randWord()
                                        move.locked = False
                                        self.locked = -1
                                        if move.progress >= 1:
                                            move.away = True
                                            self.away_counter = 1
                                            moveLocal = self.PLACE['Moves'][index]
                                        break
                                    
            if self.away_counter > 0:
                self.away_counter += 1
            if self.away_counter > 10:
                self.away_counter = 0
                self.pers.place = moveLocal[2]
                self.update()
                #self.pers = self.pers.save()

            #LOGIC FOR ALL SPRITES

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
                self.bg.set_alpha(255 - self.t_counter)
            self.surface.blit(self.bg, (x,y))
            self.t_counter -= 20

            #DRAW ALL SPRITES
            
            for move in self.moves:
                move.draw(self.surface)

            self.message.draw(self.text)
            self.hints.draw(self.surface, settings)

            if self.intro == False:
                self.pershp.draw(self.surface, (self.surface.get_width() / 2 - self.pershp.width / 2, 5), self.pers.hp / self.pers.maxhp)

            pg.display.flip()

class Battle():
    def __init__(self, surface):
        self.surface = surface
        self.attacks = [
            interface.Attack('head'),
            interface.Attack('torso'),
            interface.Attack('groin'),
            interface.Attack('legs')
        ]
        self.defences = [
            interface.Defence('head'),
            interface.Defence('torso'),
            interface.Defence('groin'),
            interface.Defence('legs')
        ]

        self.defence = -1 #Current defence [head, torso, groin, legs] [1, 2, 3, 4]
        self.attack = -1 #Current attack [1, 2, 3, 4]
        self.attackX = 5000 #Under screen for sure
        self.mob_defence_X = 0
        self.mob_defence = random.randint(1, 4)
        self.mob_attack = -1
        self.mob_attack_X = 0

        self.defence_X = 5000

        for j in range(len(self.attacks)):
            rtext = self.randWord()
            for i in range(3):
                rtext += ' ' + self.randWord()
            self.attacks[j].rtext = rtext
        for j in range(len(self.defences)):
            rtext = self.randWord()
            for i in range(3):
                rtext += ' ' + self.randWord()
            self.defences[j].rtext = rtext
        
    def randWord(self):
        unique = False
        while not unique:
            unique = True
            word = ''
            while len(word) > 10 or len(word) < 6:
                word = random.choice(data.words)
            for m in self.attacks:
                for rword in m.rtext.split():
                    if word[:1] == rword[:1]:
                        unique = False
            for m in self.defences:
                for rword in m.rtext.split():
                    if word[:1] == rword[:1]:
                        unique = False
        return word

    def loop(self, pers, bg):
        #self.bg = pg.transform.scale(pg.image.load('Images/Battle/' + os.path.basename(os.path.dirname(pers.place)) + '.jpg'), SIZE)
        self.bg = bg
        current = next(item for item in d.place if item['Id'] == pers.place)['Mobs']
        clock = pg.time.Clock()
        mob = classes.Mob(current['Type'])

        #speed.append(mob.speed)
        self.stats = interface.BattleStats(self.surface, mob)

        #CREATE SHIELD
        self.shield = pg.transform.scale(pg.image.load('Images/Shields/' + pers.shield + '.png'), (100,100))
        self.mob_shield = pg.transform.scale(pg.image.load('Images/Shields/0.png'), (100,100))
        #CREATE SWORD
        self.sword = pg.transform.scale(pg.image.load('Images/Swords/' + pers.sword + '.png'), (100,100))
        self.mob_sword = pg.transform.flip(pg.transform.scale(pg.image.load('Images/Swords/' + pers.sword + '.png'), (100,100)), True, False)

        self.locked = [-1, -1] #At start, there's none locked attacks
        self.atkdef = [self.attacks, self.defences]

        while mob.hp > 0 and pers.hp > 0:
            clock.tick(30)

            #Calculate MOB AI
            mob.act += mob.speed
            if mob.act >= constants.MOB_ACT:
                mob.act = 0
                self.mob_attack = random.randint(1,4)
                self.mob_attack_X = self.surface.get_width() / 2 - self.mob_sword.get_width() / 2 + 100 #Prepare to swing a sword with mob's hand
                if self.mob_attack != self.defence:
                    self.stats.Red = 200 #Flash player
                    pers.hp -= random.randrange(int(mob.attack * constants.PRE / constants.RANDOMIZER), int(mob.attack * constants.PRE * constants.RANDOMIZER)) / constants.PRE
                    #Clean pers shield - DO NOT CLEAR IT IF NOT CRUSHED
                    #self.defence = -1
                else:
                    #self.defence_X = self.surface.get_width() / 2 - self.shield.get_width() / 2 - 100
                    temp_defence = self.defence #For shield bouncing
                    self.defence = -1
                    self.stats.Blue = 200 #Flash shield

            events = pg.event.get()
            for e in events:
                if e.type == pg.QUIT:
                    quit()
                if e.type == pg.KEYDOWN:
                    if e.key == pg.K_ESCAPE:
                        for i in range(2):
                            if self.locked[i] != -1:
                                while self.atkdef[i][self.locked[i]].rtext[:1] != ' ':
                                    self.atkdef[i][self.locked[i]].rtext = self.atkdef[i][self.locked[i]].rtext[1:]
                                self.atkdef[i][self.locked[i]].rtext = self.atkdef[i][self.locked[i]].rtext[1:] + ' ' + self.randWord()
                                self.atkdef[i][self.locked[i]].locked = False
                                self.locked[i] = -1
                    elif e.unicode.isalpha():
                        for i in range(2):
                            for index, attack in enumerate(self.atkdef[i]):
                                if self.locked[i] == -1 or self.locked[i] == index:
                                    if self.locked[i-1] == -1:
                                        if attack.rtext.startswith(e.unicode):
                                            attack.rtext = attack.rtext[1:]
                                            attack.locked = True
                                            self.locked[i] = index
                                            pers.battleStrokes += 1 #statistics :)

                                            if attack.rtext[0] == ' ':
                                                attack.rtext = attack.rtext[1:] + ' ' + self.randWord()
                                                attack.locked = False
                                                self.locked[i] = -1

                                                if i == 0:
                                                    #ATTACK THE MOB
                                                    self.attack = index + 1
                                                    self.attackX = self.surface.get_width() / 2 - self.sword.get_width() / 2 - 100 #Prepare to swing a sword
                                                    if self.mob_defence != self.attack:
                                                        #Somehow it cannot accept list like stats.red[i]
                                                        self.stats.mobRed = 200 #Flash red
                                                        mob.hp -= random.randrange(int(pers.attack * constants.PRE / constants.RANDOMIZER), int(pers.attack * constants.PRE * constants.RANDOMIZER)) / constants.PRE
                                                        #Renew mob shield
                                                        self.mob_defence = random.randint(1, 4)
                                                    else:
                                                        #Renew mob shield
                                                        self.mob_defence_X = self.surface.get_width() / 2 - self.mob_shield.get_width() / 2 + 100 #Prepare to defend the monster
                                                        temp_mob_defence = self.mob_defence
                                                        self.mob_defence = random.randint(1, 4)
                                                        #IF PERS HAS SHIELDBREAKING - THIS IS THE TIME TO BREAK SHIELD
                                                        self.stats.mobBlue = 200 #Flash shield
                                                else:
                                                    #DEFEND THE PLAYER
                                                    self.defence = index + 1 #Set this to [1, 2, 3 or 4] correspondingly to [head, torso, groin, legs]

                                                break

            #STATS
            if pers.hp < 1:
                pers.hp = 0
            if mob.hp < 1:
                mob.hp = 0

            #NOTIFICATIONS
#            for n in notifications:
#                if n.y > -n.surface.get_size()[1]:
#                    n.draw(self.surface)
#                else:
#                    del n

            self.surface.fill(0)
            self.surface.blit(self.bg, (0,0))
            self.stats.draw(self.surface, pers, mob)

            #Draw shield
            if self.defence != -1:
                self.surface.blit(self.shield, (self.surface.get_width() / 2 - self.shield.get_width() / 2, self.surface.get_height() / 5 * self.defence))

            if self.attack != -1 and self.attackX < self.surface.get_width()/2 + 100:
                self.surface.blit(self.sword, (self.attackX, self.surface.get_height() / 5 * self.attack))
                self.attackX += 30
                if self.mob_defence_X > self.surface.get_width() / 2 - 100:
                    self.surface.blit(self.mob_shield, (self.mob_defence_X, self.surface.get_height() / 5 * temp_mob_defence))
                    self.mob_defence_X -= 30

            if self.mob_attack != -1 and self.mob_attack_X > self.surface.get_width()/2 - 100:
                self.surface.blit(self.mob_sword, (self.mob_attack_X, self.surface.get_height() / 5 * self.mob_attack))
                self.mob_attack_X -= 30
                if self.defence_X < self.surface.get_width() / 2 + 100:
                    print(self.defence_X)
                    self.surface.blit(self.shield, (self.defence_X, self.surface.get_height() / 5 * temp_defence))
                    self.defence_X += 30

            for attack in self.attacks:
                attack.draw(self.surface)
            for defence in self.defences:
                defence.draw(self.surface)

            pg.display.flip()

        if pers.hp == 0:
            pers.hp = pers.maxhp * .2
            pers.experience -= pers.experience / 10
            camp = next(item for item in d.place if item['Id'].startswith(basename(pers.place)))['Id']
        elif mob.hp == 0:
            #REWARDS
            pers.experience += random.randrange(int(mob.experience*constants.PRE / constants.RANDOMIZER), int(mob.experience*constants.PRE * constants.RANDOMIZER)) * constants.RATES / constants.PRE
            pers.gold += random.randrange(int(mob.gold*constants.PRE / constants.RANDOMIZER), int(mob.gold*constants.PRE * constants.RANDOMIZER)) * constants.RATES / constants.PRE

            #SHOW REWARDS WINDOW HERE, BEFORE RETURNING

        return pers
