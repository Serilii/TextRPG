#starting variables
flag_fighting = False
flag_shopping = False
flag_in_dungeon = False

defeated_enemies = 0
damage_done = 0
inventory = []
enemies = []
shop = []
world_height = 9
world_width = 9

yes_array = ["yes", "yeah", "yo", "ys","ye", "ahoi", "yup", "ja", "correct", "right", "si", "sure", "okay", "agree", "absolutely", "roger", "aye", "positive"]
no_array = ["no", "nope", "nop", "nein", "never" , "not", "negative", "njet" ]

#important global variables
crit_bonus = 0              #bonus chance for critting, additive, whole numbers (+5 increases critchance by flat 5% )
healing_multiplicator = 1   #healing multiplicator, factorial (1.5 = + 50% )
textspeed = 0.02            #lower textspeed means faster
spawn_chance = 40           #spawn chance of monsters in whole numbers
