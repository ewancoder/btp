class Data():
    def update(self, pers):
        self.chest = []
        self.place = []

        self.place.append({
            'Id': 'introIntroduction',
            'Goto': 'House/OldManHouse'
        })

        self.Introduction = [
            'After all worlds has merged, all the Elvines has died, for they did not belong to a new world created by curious Elder One, they did not managed to bear their cause, to save world each from another apart. All, but for Lucifer who was exalted and was not anymore one of the Elvines.',
            'Even the Goddess was perished forewer, for pure Light essence could not live in new world',
            'Other races survived, but begun big survival fight between races and all kinds of creatures',
            'And so it was for two thousand long years, blood spilled on earth until the Earth could not absorb it anymore, and then blood became rivers. They formed 3 big forks, and they was named upon 3 greatest warrior on that war: Lieones, Batrexar and Adela',
            'Then, after 20 years, a lot of creature kinds was dead end, but lots was alive. A peace was made between three main fractions, and that was it.',
            'One land for brave Great Lieones, who killed last dragon by himself; one for Smart Batrexar, who was the most concerned in a peace, and one for charming Adela, who was as deathly dangerous as charming.',
            'And after 10 years after that, amidst these grievous days, a boy had born. A mother died giving birth. A father was long dead. There was no relatives to him, so he strangled to live.',
            'One old man with no name find the boy. He took him and taught to fight. He called him... [' + pers.name + ']...'
        ]

        self.place.append({
            'Id': 'House/OldManHouse',
            'Text': 'lanerismololothisshouldstraightenourfontslolThisis the place where you\'ve been raised. Old man are now gone for a ' + str(20 + (pers.time / (24 * 60))) + ' days. So you are decided to go off [CHANGEABLE BY TIME AND OTHER FACTORS].\nYou can go [out] or [upstairs]. Also you can check [chest] under the window.',
            'Desc': ['Go out onto the streets', 'Go up onto the second floor'],
            'Move': ['out', 'upstairs'],
            'Goto': ['Village/OldManHouse', 'House/OldManHouseUpstairs'],
            'Mobs': {'Chance': 50}
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
