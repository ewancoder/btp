SIZE = (1366, 768) #Window size
#SIZE = (640, 480) #Mini size
BG_SIZE = (SIZE[0]+50, SIZE[1]+50) #Background images size

DISTANCE = 100 #Standart distance between any locations [in meters]

RANDOMIZER = 1.3 #How much a random value (of experience/gold) should be randomized (1 - not at all, 2 - twice). ALL RANDOMIZING now use this value as INITIAL POINT. For example, RANDOMIZER * 0.9 = 1.3 * 0.9 = 1.17 - this is randomized value of monster speed in battle
    #given experience
    #given gold
    #pers attack

RATES = 1 #Simply put: it's game rates. Set this to 10 and you get x10 gold, x10 experience

LEVELS = (100, 2) #First number is the experience needed to get 2nd level, second number is multiplier for the next level

PRE = 100 #PREcision, how much zero after dot after calculating random values

MOB_ACT = 10000 #Max quota for speed increasing in battle (mob.speed)
