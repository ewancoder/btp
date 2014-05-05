valeMobs = {
    'Chance': 50
}

class IntroText():

    def __init__(self, name):
        self.introtext2 = [
            'After all worlds has merged, all the Elvines has died, for they did not belong to a new world created by curious Elder One, they did not managed to bear their cause, to save world each from another apart. All, but for Lucifer who was exalted and was not anymore one of the Elvines.',
            'Even the Goddess was perished forewer, for pure Light essence could not live in new world',
            'Other races survived, but begun big survival fight between races and all kinds of creatures',
            'And so it was for two thousand long years, blood spilled on earth until the Earth could not absorb it anymore, and then blood became rivers. They formed 3 big forks, and they was named upon 3 greatest warrior on that war: Lieones, Batrexar and Adela',
            'Then, after 20 years, a lot of creature kinds was dead end, but lots was alive. A peace was made between three main fractions, and that was it.',
            'One land for brave Great Lieones, who killed last dragon by himself; one for Smart Batrexar, who was the most concerned in a peace, and one for charming Adela, who was as deathly dangerous as charming.',
            'And after 10 years after that, amidst these grievous days, a boy had born. A mother died giving birth. A father was long dead. There was no relatives to him, so he strangled to live.',
            'One old man with no name find the boy. He took him and taught to fight. He called him... [' + name + ']...'
        ]

    introtext = [
        'Long before the Age of Heroes, when there was nothing but the essence of the pure Light, 6 worlds have been created by the hand of the Goddess Liana.',
        'She divided them one from another, so one cannot reach another, not from mortal world.',
        'Six pure worlds there was. The first one and the most beautiful was for Elvines, pure Light essence creatures, who lived to serve Liana. The Sine, they called it.',
        'The other was the Mist, for smart Agons, whose knowledge sometimes can come closely to Elder Ones, so they quickly invented ways of technology, immortality and life secrets, yet they were never to reach other worlds.',
        'The other one was for humans, who often reach for quarrel and provoke wars. There was The Earth, the third world.',
        'Another one was for elves, who live they infinite life forever, be it a curse or a blessing. A planet of an endless forest, The Eden they called it.',
        'Fifth world was for beasts, for Werewolves, Dragons and Orgons, and other things. The Purgatory this world was called.',
        'Sixth world was for Dark Things, for Daemons and Devils, for those Beasts who desire to absorb all other worlds. And kind goddess Liana gave them home as well, for each and every one deserve love. Hellium the Hell it was called.',
        'The seventh, and the last world was for The Elder Ones. It was ever and will be.',
        'Long time all the worlds were in peace, but once upon a time there was a big quarrel between The Elder Ones, and they have separated.',
        'With their breakup, big grief had come in each of worlds, lots of wars and pain and death.',
        'There was pain everywhere except the Sine, the Elvines world, because it was the world of pure Light and Love, and war there was no possible.',
        'And when there was nothing but a war and pain and dread in each of the worlds, one of the Elvines decided to help them against the will of the Goddess Liana. He grab his sword of light and descent to the waisted worlds.',
        'He gave them hope, he trained them to rule their destiny. It was the Age of Heroes.',
        'The Goddess saw him in the fire of battle, saw what he did. And she punished him, for he did betrayed her and the Elder Ones, for a man could not control his destiny. She cut his wings and left him in exile.',
        'So he stuck in the last world he did not yet managed to help - Hellium the Hell. His name was Luciferus.',
        'Long time has left after his rebelion, and all kinds of creatures eventually become more wise and did not rise for a wars anymore. Even The Hell become more peaceful place than it was before, though Lucifer could not help them much without his wings.',
        'But Lucifer did not count one last piece: The Elder Ones',
        'The Elder Ones were much much older than even Goddess Liana and all those seven world. They existed and will exist endlessly in a circle of time. They created everything and they are everything. So, they were wise, wiser than anything and anyone.',
        'There was one thing, that had bring a quarrel to them and separated them from their main cause: to bring peace and rule the destiny. It was the suggestion of the younger Elder One, though he was thousand times older than the worlds we know. He suggested to blend all the worlds together and see what happens.',
        'Some agreed, cause all the time all worlds existed was just another day for Elder Ones, some of more wise had not. And the war begun between The Elder One. And then great Grief begun, and some time after that the Age of Heroes.',
        'When Lucifer had been exalted from the Sine, the younger Elder One who wanted to blend the worlds almost win the Elder War. It was only time matter when they were going to finally blend it, and the time is nothing for the Elder Ones.',
        'Sure enough, when Lucifer was fighting on the Hell, trying to make some peace, it happens.\nNone could predict the consequences.\nEven the Elder Ones...'
    ]

place = []
place.append({'Id': 'OldManHouse', 'Text': 'This is the place where you\'ve been raised. Old man are now gone [COUNT TIME]. So you are decided to go off [CHANGEABLE BY TIME AND OTHER FACTORS].\nYou can go [out] or [upstairs]. Also you can check [chest] under the window.', 'Actions': ['out', 'upstairs', 'chest'], 'Goto': ['Big Vale', 'Small Vale', 'Chest'], 'Mobs': valeMobs})
place.append({'Id': 'Big Vale', 'Text': 'There are smoke everywhere and big fire dance around the Great Fault\nYou can go [left] and [right]', 'Actions': ['left', 'right'], 'Goto': ['Big Vale', 'Small Vale'], 'Mobs': valeMobs})

