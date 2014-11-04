with open('words.txt') as f:
    words = f.read().splitlines()

class Data():
    def update(self, pers):
        self.chest = []
        self.place = []

        self.place.append({
            'Id': 'introduction',
            'Goto': 'Forest/StumpOfDworaks'
        })

        self.introduction = [
            'There was a peaceful, beautiful planet... once upon a time, when humanity only began to evolve into something bigger.',
            'Humans just started developing artificial black holes for quick interstellar travel, when suddenly it happend.',
            'Not a man knew what was going on. The sky just gone black out of clear sunny day, it suddenly became pitch-dark.',
            'There was panic. Scientists could not determine a cause of this event. Anyway, they hadn\'t much time. 3 hours later, The lightning stuck the Earth. The lightning a man have never seen.',
            'After that, many people died. There was lots of earthquakes, tsunamis, every kind of horrible disasters. And noone knew what\'s going on. Then strange things began to happen.',
            'Impossible monsters came to our world. Werewolves, walking trees, dark and horrible dragon-like creatures.',
            'But with them, there came other kind of creatures, who fought evil ones with rage and fury.',
            'So Earth was not Earth anymore...',
            'For 200 long years there was a bloody war between all possible creatures.',
            'Then we found some kind of peace.',
            'In such horrible times a boy was born, his mother died giving birth, father was long gone for war.',
            'But one old man with no name found the boy. He took him and taught to fight. He called him... [' + pers.name + ']...'
        ]

        self.place.append({
            'Id': 'Forest/StumpOfDworaks',
            'Text': 'This is The mighty Stump of Dworaks, historical relict found in these woods after the Great Sorrow. It gave life to many Dworaks after the Moonlight slaughter, which then took care of those in need. They rebuild community of Elves and Humans, communed Orks with Dwarfs. And all this were possible because of a simple stump. They say, "Even small things could do a big difference"...',
            'Moves': [
                ('Small grove to the left', 'left', 'Forest/SunnyGrove')
            ],
            'Hints': ('Type white text under yellow captions to move',
                      'You will move to another location when progress bar is full',
                      'Once you will master your running skills, you could move faster')
        })

        self.place.append({
            'Id': 'Forest/SunnyGrove',
            'Text': 'Small grove of fresh trees, plentiful of branches, logs and flowers. I can surely rest here.',
            'Moves': [
                ('Go right, to the Stump of Dworaks', 'right', 'Forest/StumpOfDworaks'),
                ('Go left, to the Moonshine lake', 'left', 'Forest/MoonshineLake'),
                ('To the road', 'top', 'Forest/OakVillageRoad'),
                ('To the Dark forest', 'bottom', 'Forest/DarkForestEntrance')
            ]
        })

        self.place.append({
            'Id': 'Forest/MoonshineLake',
            'Text': 'Moonshine lake is the only source of clean water out there.',
            'Moves': [
                ('Back to grove', 'bottom', 'Forest/SunnyGrove')
            ]
        })

        self.place.append({
            'Id': 'Forest/DarkForestEntrance',
            'Text': 'This is a very dangerous place indeed. Many tried to conquer its posessions, but none have left alive',
            'Moves': [
                ('Back to grove', 'bottom', 'Forest/SunnyGrove')
            ]
        })

        self.place.append({
            'Id': 'Forest/OakVillageRoad',
            'Text': 'This road leads to the Oak village, the place where I grew up',
            'Moves': [
                ('Back to grove', 'bottom', 'Forest/SunnyGrove')
            ]
        })
