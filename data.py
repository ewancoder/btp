with open('words.txt') as f:
    words = f.read().splitlines()

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
                ('Go left', 'left', 'Forest/Grove')
            ],
            'Hints': ('Type white text under yellow captions to move',
                      'You will move to another location when progress bar is full',
                      'o')
        })

        self.place.append({
            'Id': 'Forest/Grove',
            'Text': 'Small grove of fresh trees, plentiful of branches, logs and flowers.',
            'Moves': [
                ('Go right', 'right', 'Forest/StumpOfDestiny'),
                ('Go left', 'left', ''),
                ('To the grove', 'top', 'Forest/StumpOfDestiny'),
                ('To unknown lands', 'bottom', 20, '')
            ]
        })

        self.place.append({
            'Id': 'Forest/CheeryGrove',
            'Text': 'Light and cheerful grove goes right onto the road to Oak Village.',
            'Moves': [
                ('Go here', (300,300), 'top', 'Forest/Grove', (-60,-20)),
                ('Go to road', (300,100), 7, 'Forest/RoadToOakVillage', (-60,-20))
            ]
        })

        self.place.append({
            'Id': 'Forest/RoadToOakVillage',
            'Text': 'You can\'t go further because I\'ve not developed it yet',
            'Moves': [
                ('To the grove', (400,300), 'bottom', 'Forest/CheeryGrove', (-60,-20))
                ]
            })
