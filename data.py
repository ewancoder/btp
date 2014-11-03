words = [
    'question', 'weather', 'earth', 'rueful', 'translate', 'yank', 'ugly', 'illegal', 'opensource', 'potato', 'automobile', 'surgery', 'dye', 'faceless', 'gather', 'hideous', 'jumper', 'knee', 'light', 'zdor', 'xor', 'complex', 'vegetable', 'brick', 'nest', 'modest'
]

class Data():
    def update(self, pers):
        self.chest = []
        self.place = []

        self.place.append({
            'Id': 'introduction',
            'Goto': 'Forest/StumpOfDestiny'
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
            'Id': 'Forest/StumpOfDestiny',
            'Text': 'This is The mighty Stump of Destiny, historical relict found in these woods after the Great Sorrow. It gave life to many Dworaks after the slaughter, which then took care of those in need. They rebuild community of Elves and Humans, communed orks with dwarfs. And all this were possible because of a simple stump. Even small things could do a big difference.',
            'Moves': [
                ('Go left', (20,400), (-1,0), 'Forest/Grove'),
                ('Go right', (-20,400), (1,0), 'test'),
                ('Pray', (300,300), 'test', 'test')
            ]
        })

        self.place.append({
            'Id': 'Forest/Grove',
            'Text': 'Small grove of fresh trees',
            'Moves': [
                ('Go left', (20,400), (-1,0), 'Village/WestGate'),
                ('Go right', (-20,400), (1,0), 'Forest/StumpOfDestiny')
            ]
        })

        self.place.append({
            'Id': 'House/OldManHouse',
            'Text': 'This is the place where you\'ve been raised. Old man are now gone for a {0} days. So you are decided to go off [CHANGEABLE BY TIME AND OTHER FACTORS].\nYou can go [out] or [upstairs]. Also you can check [chest] under the window.'.format(int(20 + pers.time / (24 * 60))),
            'Desc': ['Go out onto the streets', 'Go up onto the second floor'],
            'Move': ['out', 'upstairs'],
            'Goto': ['Village/OldManHouse', 'House/OldManHouseUpstairs'],
            'Time': [1, 1],
            'Mobs': {
                'Chance': 100,
                'Speed': 2,
                'Object': 'Skeleton(atk = 5)'
            },
        })

        self.chest.append({
            'Id': 'Village/OldManHouse',
            'Items': [
                'Pocket knife',
                '_80_Gold',
                '_q_Beginning',
                '_n_OldManNote'
            ]
        })

        self.place.append({
            'Id': 'Village/OldManHouse',
            'Text': 'Your old home standing here, lurching in dappled shadows of pale ivy leaves. Here you\'ve been raised, here you\'ve been taught. Brooding memories filling your brain.',
            'Desc': ['Go into the old man\s house', 'Go to the center of the village', 'Go to west towards the gates'],
            'Move': ['in', 'go to center', 'go to west'],
            'Goto': ['House/OldManHouse', 'Village/PaleVillageCenter', 'Village/PaleVillageWest'],
        })
