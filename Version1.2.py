############################################################################# Interlude ############################################################################################

# Hello there! This is my very first program. The purpose is to learn the basics of coding , applying them to a playable game and bugfixing everything just to learn what's possible and what isn't.
# Since I learned a lot by actively coding, there might be code snippets with more or less quality inbetween. Don't be surprised! :)
# Funfact: Animations in the console are possible and present in the game!
# All you need to play is an IDE and Python so far. Just look at the code or play it as you wish. But enjoy!

####################################################################################################################################################################################
#ideas : magic system, defensive options (shields, dodges), glasses that show enemy stats, random item chances at pawn shop

from random import *
from time import *
import os
from copy import *
#import cursor --> cursor.hide()  # module to be downloaded/ experimental

#variablen
flag_fighting = False
flag_shopping = False
flag_in_dungeon = False
defeated_enemies = 0
damage_done = 0
inventory = []
enemies = []
shop = []

yes_array = ["yes", "yeah", "yo", "ys","ye", "ahoi", "yup", "ja", "correct", "right", "si", "sure", "okay", "agree", "absolutely", "roger", "aye", "positive"]
no_array = ["no", "nope", "nop", "nein", "never" , "not", "negative", "njet" ]

#important global variables
crit_bonus = 0              #bonus chance for critting, additive, whole numbers (+5 increases critchance by flat 5% )
healing_multiplicator = 1   #healing multiplicator, factorial (1.5 = + 50% )
textspeed = 0.02            #lower textspeed means faster
spawn_chance = 40           #spawn chance of monsters in whole numbers
world_height = 9
world_width = 9


####################################### class for player ####################################
class player:
    def __init__(self, name, hp, maxhp, gold, x, y, mana, maxmana):
        self.name = name
        self.maxhp = maxhp
        self.hp = hp
        self.gold = gold
        self.x = x
        self.y = y
        self.mana = mana
        self.maxmana = maxmana
        self.worldmap_x = 0
        self.worldmap_y = 0

    def heal(self, value):
        self.hp += value
        if self.hp > self.maxhp:    #anti overheal
            self.hp = self.maxhp    
   
    def get_name(self):         #get the name with the right \t format
        x = 1-(len(self.name) // 8)
        y = self.name + x*"\t" + "    "
        return y

####################################### class for regular items ####################################
class item:
    def __init__(self, name, value, quantity, healing, function : str, potion = False):
        self.name = name
        self.value = value
        self.quantity = quantity
        self.healing = healing
        self.function = function
        self.number = 0
        self.potion = potion
 
    def increase(self, ammount):
        self.quantity += ammount
 
    def decrease(self, ammount):
        if self.quantity >= ammount:
            self.quantity -= ammount
        else:
            self.quantity = 0
    def heal(self):
        if self.quantity > 0:
            self.decrease(1)
            heal = int(self.healing * healing_multiplicator)
            p1.hp += heal
            if p1.hp > p1.maxhp:        #anti overheal
                p1.hp = p1.maxhp
            print("You used a " + self.name + ". You restored " + str(heal) + " health.")
        else:
            print("You are out of that item!")
   
    def get_name(self): #get the name with the right \t format
        x = 2-(len(self.name) // 8)
        if 7 < (len(self.name)) < 12:       #item names between 8 and 12 letters arent formatted right without this line
            x += 1
        y = self.name + x*"\t"
        return y
 
 
#creating some items
dummy = item("Dummy", 0, 0, 0, "", 0)
potion = item("Potion", 10, 5, 50, "Restores health\t", True)
testitem = item("item with loooooong name", 0, 1, 0, "hard to pronounce")
stone = item("Stone",1, 4, 0, "Looks very throwable" ,)
bottle = item("Empty bottle", 1, 0, 0, "I don't remember drinking this..")
superpotion = item("Super Potion", 35, 1, 100, "Restores even more health")
healingherb = item("Healing Herb", 3, 5, 5, "Used to brew potions" )
attackpotion = item("Attack Potion", 50, 0, 0, "Buffs Attack for 5 rounds", True )
defensepotion = item("Defense Potion", 50, 1, 0, "Buffs defense for 5 rounds", True)
batfang = item("Bat Fang", 10, 1, 0, "A hand full of sharp Bat fangs")
slime_item = item("Slime", 3, 1, 0, "Is this...the corpse?!..",)

#packing every item into inventory
inventory = [dummy, potion, testitem, stone, bottle, superpotion, healingherb, attackpotion, defensepotion, batfang, slime_item]

shop = [potion, stone, bottle, superpotion ]
witch_hut_items = [healingherb, attackpotion, defensepotion]

#define using item
def use_item(item):
    global flag_fighting
    if item.quantity > 0:   #checking if item quantity is > 0
       
        if item.healing > 0:    #healing if healing item
            item.heal()
 
        #using Stone
        elif item.name.lower() == "stone":
            if flag_fighting == True:
                item.decrease(1)
                current_enemy.hp -= 10
                print("You threw the Stone and hit an eye. The " + current_enemy.name + " lost 10 HP. Maybe you should use your weapons.") #if fighting
            else:
                print("You hold the stone very tight. It almost cut your finger.")    #if not fighting
        
        elif item.potion == True: #using potion
            if flag_fighting == True: #if fighting
                use_potion(item)    
            else:
                print(f"The {item.name} looks bomb but let's wait for the thirst of war.") #if not fighting

        else:       #default flavour text if item has no healing or certain use
            print("You throw the " + item.name + " very hard on the ground. It shatters into a million pieces. You don't know what you expected. You collect the pieces and glue them together.")
    else:       #quantity is 0
        print("I have none of that.")
    junk = input(" ↩ ")

def use_potion(ptn):
    match ptn.name.lower():
        case "attack potion":
            attackpotion.decrease(1)
            attackup.buff(6)
            print("You gobbled the Attack Potion and raised your attack for 5 rounds!")
        case "defense potion":
            defensepotion.decrease(1)
            defenseup.buff(6)
            print("You devoured the Defense Potion and hardened your skin for 5 rounds!")

####################################### class for enemies ####################################
class enemy:
    def __init__(self, name, hp, atk, defense, gold, loot = None, loot_ammount = 0, loot_chance = 0):
        self.name = name
        self.hp = hp
        self.maxhp = hp
        self.atk = atk
        self.defense= defense
        self.number = 0
        self.gold = gold
        self.loot = loot
        self.lootammount = loot_ammount
        self.loot_chance = loot_chance
 
    def heal(self, value):
        self.hp += value
        if self.hp > self.maxhp:    #anti overheal
            self.hp = self.maxhp
   
    def get_name(self):         #get the name with the right \t format
        x = 1-(len(self.name) // 8)
        y = self.name + x*"\t" + "    "
        return y
 
#crating some enemys                #lootchances are in % x 100 (natural numbers idk)
dummy = enemy("dummy", 0, 0, 0, 0)
slime = enemy("Slime", 30, 3, 0, 5, slime_item, 1, 80)
goblin = enemy("Goblin", 70, 7, 4, 13)
wolf = enemy("Wolf", 95, 11, 5, 20)
dragon = enemy("Dragon", 150, 35, 10, 100)
schlumpf = enemy("Smurf", 25, 10, 0, 25)
bat = enemy("Bat", 20, 4, 1, 4, batfang, 1, 75 )
ork = enemy("Ork", 100, 13, 5, 25)
eviled = enemy("EvilED", 66, 11, 6, 9)
troll = enemy("Troll", 80, 17, 3, 20)

#packing them all in an array
enemies = [dummy, slime, goblin, wolf, schlumpf, bat, ork, eviled, troll]
enemies_cave1 = [dummy, slime, bat]
#return one enemy of this array
def get_enemy():
    global current_world
    if current_world == cave1_map:
        r = enemies_cave1[randint(1,len(enemies_cave1)-1)]    
    else:
        r = enemies[randint(1,len(enemies)-1)]

    return r
 
####################################### class for weapons ####################################
class weapon:
    def __init__(self, name, damage, crit, price, text)  :
        self.name = name
        self.damage = damage
        self.crit = crit
        self.price = price
        self.number = 0
        self.text = text
        self.bagged = False
   
    def replace(self, weapon):
        global current_weapon
        weapons[current_weapon.number].bagged = True
        current_weapon = weapon
        weapon.bagged = False  
 
    def get_name(self):         #get the name with the right \t format
        x = 2-(len(self.name) // 8)
        y = self.name + x*"\t"
        return y
 
#creating weapons
dummy = weapon("dummy", 0, 0, 0, "")
woodensword = weapon("Wood Sword", 13, 5, 40, "A sword made of wood. Good for training")
baseballbat = weapon("Baseball Bat", 29, 1, 180, "Higher base damage. Also good for homeruns")
katana = weapon("Katana", 50, 20, 600, "Damage, Crit, Anime")
bow = weapon("Bow", 13, 60, 80, "Lower Damage but High Critical")
steelsword = weapon("Steel Sword", 20, 8, 150,  "Solid Weapon to fight solid monsters" )
axe = weapon("Axe", 38, 10, 280, "Nice for chopping trees. Also good for chopping evil.")
spear = weapon("Spear", 27, 25, 250, "Good range, Nice crits. Throwing things is awesome." )

#packing weapons into array
weapons = [dummy, woodensword, baseballbat, katana, bow, steelsword, axe, spear]
smithy = [woodensword, baseballbat, katana, bow, steelsword, axe, spear]
 
#opening smithy
def open_smithy():
    speak("The further you follow the rising smoke the louder the sound of hammering metal gets. A silent man is heating up the forge. You enter. ")
    speak("'Welcome. I sell weapons.")
    sleep(1)
    print("Current gold:  " + str(p1.gold))
    print("________________________________________________________________________________________")
    print("UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU")
    for i in smithy:
        print(i.get_name() + "\t" + str(i.price) + " Gold     \tNr. " + str(i.number) + "\t\t use:  " + i.text)
    print("________________________________________________________________________________________")
    global flag_shopping
    flag_shopping = True
    while flag_shopping == True :
        print("You can select weapons by typing the name or Nr. \t type '0' or 'exit' to go leave.")
        action = input()
        if action == "0" or action.lower() == "exit":
            speak("As the smith hammers the steel a spark flies into your eye. One of your eyes whitnesses you leaving the smithy. Ouch..")   
            flag_shopping = False
            return
        for wpn in smithy:
            if action.lower() == wpn.name.lower():
                buy_weapon(wpn)
        try:
            action=int(action)
            for wpn in smithy:
                if action == wpn.number:
                    buy_weapon(wpn)
        except:
            pass    
 
def buy_weapon(wpn):
    a = wpn
    if a.bagged == False and current_weapon.name != a.name :        
        if a.price <= p1.gold:
                q = ""
                while not(q.lower() in yes_array or q.lower() in no_array) :
                    q = input("Do you want to buy the " + a.name + "? 'Yes' or 'No'?\n")
                    if q.lower() in yes_array:
                        current_weapon.replace(a)
                        p1.gold -= a.price
                        print("You bought and equiped a " + a.name)
                        sleep(0.5)
                    elif q.lower() in no_array:
                        print("Then don't waste my time!")
        else:
            speak("You can't afford this. *The smith exhales loduly*")    
    else:
        print("You already have this weapon.")
 

####################################### class for base items ####################################
class baseitem:
    def __init__(self, name, function):
        self.name = name
        self.function = function
        self.obtained = False
   
    def get_name(self): #get the name with the right \t format
        x = 2-(len(self.name) // 8)
        y = self.name + x*"\t"
        return y
 
pendant1 = baseitem("Fairy Pendant", "A fairy shaped Pendant emitting a slight glow. Raises health and boosts healing.")
pendant2 = baseitem("Heart Pendant", "A heart shaped Pendant emitting a slight glow. Raises health and boosts healing.")
artifact = baseitem("Artifact ", "A weird stone you found in your pocket. It tickles when you touch it.")
artifact.obtained = True
whetstone = baseitem("Whetstone", "A chonky little whetstone for your weapons. The sharpness increases your crit chance.")
cauldron = baseitem("Cauldron", "You can craft stuff in this. Very handy! Very witchy..")
#put your base items into here!!!! :
baseitems = [artifact, pendant1, pendant2, whetstone, cauldron]
 
####################################### class for buildings ####################################
class building:
    def __init__(self, name):
        self.name = name
 
    def open(self):
        print("There is a " + self.name + " nearby.")
        action = ""
        while not(action.lower() in yes_array or action.lower() in no_array):
            action = input("Do you want to enter? 'Yes' or 'No'\n")
            if action.lower() in yes_array:
                match self.name.lower() :
                    case "smithy":  open_smithy()
                    case "shop":   open_shop()
                    case "forest fountain": open_fairy_fountain_1()
                    case "ruin fountain":   open_fairy_fountain_2()
                    case "witch hut":   open_witch_hut()

#creating the buildings and tiles
smithy_shop = building("Smithy")
shop1 = building("Shop")
fairy_fountain_1 = building("Forest Fountain")
fairy_fountain_2 = building("Ruin Fountain")
witch_hut = building("Witch Hut")


####################################### class for caves #####################################
class cave:
    def __init__(self, name: str, starting_x, starting_y, cavemap, monster_array = None):
        self.name = name
        self.starting_x = starting_x    #caves starting coordinates
        self.starting_y = starting_y    
        self.cavemap = cavemap          #contains the array with the current map to load it
        self.monster_array = monster_array      #corresponding monster array to list the monsters


    def enter(self):
        print("You stand in front of a cave. There is a shield:")
        print("'Beware of ", end = "") 
        self.list_enemies() 
        print("Do you want to enter?")
        action = input()
        if action.lower() in yes_array:
            p1.worldmap_x = p1.x            #safes the players coordinate into his world coordinate. for exiting later
            p1.worldmap_y = p1.y            
            p1.x = self.starting_x          #brings the player to the maps start
            p1.y = self.starting_y
            global current_world    
            current_world = self.cavemap    #current map becomes the cavemap
            global flag_in_dungeon 
            flag_in_dungeon = True
            print("You entered the cave.")

    def exit(self):
        global current_world
        current_world = worldmap       #loads the worldmap back into "current_world"
        p1.x = p1.worldmap_x           #teleports you back to your last position that was saved
        p1.y = p1.worldmap_y
        global flag_in_dungeon
        flag_in_dungeon = False
        print("You left the cave.")
    
    def list_enemies(self):             #function to return list of current enemies in the cave
        for monster in self.monster_array:
            if monster.name != "dummy":
                print(monster.name, end = "s , ")
        print("forgetting Moms birthday!'")

####################################### class for NPCs #####################################
class npc:
    def __init__(self, name):
        self.name = name
        self.talked = False

#creating NPCs
nancy = npc("Nancy")
smith = npc("the Smith")
grandma = npc("Grandma")
witch = npc("the Witch")

####################################### class for tiles ####################################
class tile:
    def __init__(self, name, spawns_enemy, building, npc:npc = None, item:item = None, caves:cave = None, movable = True):
        self.x = 0
        self.y = 0
        self. name = name
        self.spawns_enemy = spawns_enemy
        self.building = building
        self.npc = npc
        self.item = item
        self.caves = caves
        self.movable = movable
        
grassland = tile("Grassland", True, None)
 
Smithy_Tile = tile("Smithy", False, smithy_shop, smith)
Shop_Tile = tile("Shop", False, shop1, grandma)
Fairy_Fountain_Tile_1 = tile("Fairy Fountain", False, fairy_fountain_1)
Fairy_Fountain_Tile_2 = tile("Fairy Fountain", False, fairy_fountain_2)
Nancy_tile = tile("Campfire", True, None, nancy)
Witch_Hut_tile = tile("Witch Hut", False, witch_hut, witch)

def get_current_tile_name():
    r = current_world[p1.x][p1.y].name
    return r
def current_tile():
    return current_world[p1.x][p1.y]


#generating the worldmap with grassland only
worldmap = [[0 for x in range(world_width+1)] for y in range(world_height+1)]
for i in range(1, world_height+1):
    for j in range(1, world_width+1):
        worldmap[i][j] = deepcopy(grassland)        #deepcopy provides a value-copy instead of the same reference
 
#distributing tiles
worldmap[3][3] = Smithy_Tile
worldmap[1][2] = Shop_Tile
worldmap[6][7] = Fairy_Fountain_Tile_1
worldmap[5][4] = Fairy_Fountain_Tile_2
worldmap[1][1] = Nancy_tile
worldmap[7][9] = Witch_Hut_tile

#creating a cave
caveground = tile("Tunnel",True, None, )
empty = tile("empty",False, None,None,None,None,False)

cave1_map = [[deepcopy(empty) for x in range(10)] for y in range(10)]   #10 x 10 array with all empty tiles
for i in cave1_map:                          #a line of caveground
    i[4] = deepcopy(caveground)

cave1_map[9][4].item = attackpotion

cave1 = cave("Tunnel", 1, 4,cave1_map, enemies_cave1 )


cave1_tile = tile("Tunnel entrance", False, None, None, None, cave1 )   # overworld tile for cave1

worldmap[1][8] = cave1_tile
############################################ class for quests #############################################

class quest:
    def __init__(self, name, text):
        self.name = name
        self.ongoing = False
        self.done = False
        self.text = text

    def take(self):
        self.ongoing = True
        print("You took the quest '" + self.name + "'")

    def finish(self):
        self.ongoing = False
        self.done = True
        print("You finished the quest '" + self.name + "'")

    def get_name(self):         #get the name with the right \t format
        x = 3-(len(self.name) // 8)
        y = self.name + x*"\t"
        return y
    
    def get_done(self):
        if self.done == True:
            return " ☑ done "
        elif self.ongoing == True:
            return " ☐ going on"
        else:
            return ""
# creating quests
        
smithy_quest = quest("Smithy's Quest", "Kill the baby Dragon by the smithy so it can't burn the wood." )
grandma_quest = quest("Good Boi", "Bring grandma 5 healing herbs")

quests = [smithy_quest, grandma_quest]

def quest_log():
    print("-------------------------Quest Log-------------------------")
    for q in quests:
        if q.ongoing == True or q.done == True:
            print(q.get_name() + "\t" + q.get_done() + "\t\t" +  q.text )
    print("-----------------------------------------------------------")

############################################ class for buffs #############################################

class buffs:
    def __init__(self, name : str ,  raising):
        self.name = name
        self.multiplicator = raising
        self.counter = 0

    def buff(self, rounds):
        self.counter += rounds

    def decrement(self, rounds = 1):    #reduce remaining rounds by 'rounds' (default 1)
            self.counter -= rounds
            if self.counter < 0:        #no negative rounds allowed!
                 self.counter = 0


attackup = buffs( "Attack Up" , 0.5 )       # checked in pattack()
defenseup = buffs("Defense Up", 0.5)        # checked in eattack() , halves taken dmg for now since there is no defense value lmao

buff_array = [attackup, defenseup]

def buffs_decrement_all(rounds = 1):
    for bfs in buff_array:
        bfs.decrement(rounds)

############################################ alchemy #############################################

class recipy:
    def __init__(self, name, first: item, second: item, third: item , product:item, product_ammount):
        self.name = name
        self.ingredients = [first, second, third]
        self.product = product
        self.product_ammount = product_ammount

    def check(self, blob):
        rezept = self.ingredients.copy()     # = recipy array
        topf = blob.copy()                  # = input array
        for i in topf:              #checks if parameter array and this recipy array are the same by deleting same items and checking if array is emtpy
            if i in rezept:
                    rezept.remove(i)
        if rezept == []:
            cauldron_animation()
            print("")
            for i in self.ingredients:
                i.decrease(1)
            self.product.increase(self.product_ammount)
            return True
        else:
            return False
            

#safe the recipies with their parameter
potion_recipy = recipy("Potions", healingherb, healingherb, healingherb, potion, 5 )
super_potion_recipy = recipy("Super Potions", potion, healingherb, healingherb, superpotion, 4 )
defense_potion_recipy = recipy("Defense Potion", potion, stone, stone, defensepotion, 1)
attack_potion_recipy = recipy("Attack Potion", potion, batfang, batfang, attackpotion, 2)

#putting all recipies into an array for methods
recipy_book  = [potion_recipy, super_potion_recipy,defense_potion_recipy, attack_potion_recipy]


def open_cauldron():        #cauldrons crafting logic!
    flag_alchemy = True
    ingredients = []
    while flag_alchemy == True and len(ingredients) < 3 :     #starting alchemy loop
        cauldron_list()
        print("")
        print("What do you want to throw into the cauldron? \t '0' or 'exit' to leave")
        if ingredients != []:
            print("currently in the cauldron: ", end = "" )        #printing the current things in the cauldron
            for j in ingredients:
                print(j.name, end = " , ", flush = True)
        
        action = input()  # naming the ingredient
        print("", end = "\r")
        if action == "0" or action.lower() == "exit":           #exit cauldron
            for h in ingredients:
                h.increase(1)
            cauldron_list()
            flag_alchemy = False
            return
        for k in inventory:
            if action.lower() == k.name.lower() and k.quantity > 0:
                ingredients.append(k)
                k.decrease(1)
    print("")
    for i in recipy_book:                                       #check if ingredients check with a recipy
        if i.check(ingredients) :
            print(f"You crafted {i.product_ammount} x {i.name}!")
            print("")
            return
    speak("...Your ingredients swim around, unwilling to to do anything remarkably...")
    for e in ingredients:
        e.increase(1)       # this line makes that insuccesfull crafting gives items back. If someone would just delete it....
    cauldron_list()
    sleep(1)        
    
def cauldron_list():        #needed for the open cauldron function, it's here for convenience bc i need it again at the end without looping again uwu
    os.system('cls')
    print("-------------- Ingredientes --------------")
    for itm in inventory:
        if itm.quantity > 0:
            print(str(itm.quantity) + " x " + itm.get_name() + "\t\tuse: " + itm.function )     

############################################ functions #############################################
#Status Bar
def anzeige():
    os.system('cls')
    print()
    if flag_fighting == True:
        print("////////////////////////////////////////////////////////////////////////////////////////")
        print("|؏࿉࿈|\t" + p1.get_name() + " " + player_healthbar() + " HP: " + str(int(p1.hp)) + " / " + str(p1.maxhp) + "    Weapon: " + current_weapon.name + (("\tMana: " + str(p1.mana) + " / " + str(p1.maxmana)) if p1.mana > 0 else "" ))
        print("|༖༗࿇|\t" + current_enemy.get_name() + " " + enemy_healthbar() + " HP: " + str(current_enemy.hp) + " / " + str(current_enemy.maxhp))
        print(r"\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\")
        for i in buff_array:
            if i.counter > 0:
                print(f"⬆ {i.name} for {i.counter} rounds" )
    else:
        print("________________________________________________________________________________________")
        print("|؏࿉࿈|\t" + p1.get_name() + " HP: " + str(int(p1.hp)) + " / " + str(p1.maxhp) + "    Weapon: " + current_weapon.name + (("\tMana: " + str(p1.mana) + " / " + str(p1.maxmana)) if p1.mana > 0 else "" ) + "    Gold: " + str(p1.gold) )
        print("|༖༗࿇|\tPosition  X(⇄) : " + str(p1.x) + "  Y(⇅): " + str(p1.y) + "\t\tArea: " + current_world[p1.x][p1.y].name)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
 
def player_healthbar():    #returns healthbar as string ♡♥
    x = p1.hp/p1.maxhp
    x = int(x*10)
    s = x*"♥" + (10-x)*"♡"
    return s
 
def enemy_healthbar():    #returns healthbar as string ♡♥
    x = current_enemy.hp/current_enemy.maxhp
    x = int(x*10)
    s = x*"♥" + (10-x)*"♡"
    return s

# worldmap menu logic
def take_menu_command():
    sleep(0.1)
    anzeige()
    print("You are resting surrounded by a " +  get_current_tile_name() + ".")
    if p1.hp / p1.maxhp < 0.4 and get_current_tile_name().lower() == "grassland":
        print("You feel pretty tired... You could use a round of sleep..")
    sleep(0.1)
    print(" ( º ֊ º)ᕤ  What's next? You can move 'up/down/left/right' ,  see your 'items' , open the 'map', 'explore' your surrounding, 'talk' to someone, see your 'quests' ")
    print("or use the 'cauldron'" if cauldron.obtained == True else "")
    action = ""
    checks = ["item","items", "move", "sleep", "rest", "up", "down", "left", "right", "map", "talk", "debug", "explore", "quest", "quests", "cauldron", "dig", "exit"]  #array of possible menu commands for the while loop, all options need to be added
    while action.lower() not in checks:
        action = input()
        match action.lower():
            case "item":
                open_inventory()
            case "items":
                open_inventory()
            case "move":
                take_movement_command()
            case "sleep":
                rest()
            case "rest":
                rest()
            case "up":
                move_on_map("up")
            case "down":
                move_on_map("down")
            case "left":
                move_on_map("left")
            case "right":
                move_on_map("right")
            case "map":
                open_map()
            case "talk":
                talk()
            case "debug":
                debugging()
            case "explore":
                explore()
            case "quest":
                quest_log()
            case "quests":
                quest_log()
            case "cauldron":
                if cauldron.obtained == True:
                    open_cauldron()
            case "dig":
                dig()
            case "exit":
                leave()
            #if you put an option here, put it into "check" ! ! !
            case _:
                pass
    checkers = ["up", "down", "left", "right", "map", "item", "items"]        #list of commands that DON'T trigger ↩ input (it says "don't", i warned you)
    if action.lower() not in checkers:
        junk = input(" ↩ ")   

def leave():
    global current_world
    if current_world != worldmap:
        p1.x = p1.worldmap_x
        p1.y = p1.worldmap_y
        current_world = worldmap
        print(f"You left the {current_tile().caves.name}.")
    else:
        print("What are you trying to leave?")

worldmap[2][2].item = superpotion
#finding items on the ground
def dig():
    if current_tile().item != None:
        print(f"You digged the ground and found a {current_tile().item.name}!")
        current_tile().item.increase(1)
        current_tile().item = None
    else:
        print(f"You digged a hole. It's very deep.... Awesome!")

def explore():
        if get_current_tile_name() == "Smithy" and smithy_quest.ongoing == True and questflag_smith_dragon == False:
            smithy_quest_fight()
        elif current_tile().building != None:     #enter the building
            current_world[p1.x][p1.y].building.open()
        elif get_current_tile_name() == "Campfire":
            print("You see the smoke of a cozy campfire nearby. It seems like someone is resting there.")
        elif current_tile().caves != None:
            current_tile().caves.enter()
            
        else:
            print("You see a bug on the ground. It's dedication to just be a bug fills you with determination.")

def rest(): #sleep mechanic
    if p1.hp / p1.maxhp < 0.4:
        print("You lay down on the grass and watch the clouds. The wind is gently stroking your face. Your eyes feel heavy.")
        sleep(1)
        print("You take a nap.", end="\r")
        sleep(1)
        print("You take a nap..", end="\r")
        sleep(1)
        print("You take a nap...", end="\r")
        print(1)
        print("You feel refreshed!")
        sleep(1)
        p1.hp += p1.maxhp*0.3
    else:
        print("But I don't feel like sleeping.. I feel like adventuring!")
 
#movement logic
def take_movement_command():
    print("'Where do I feel like going?'")
    direction = ""
    while direction != "up" and direction != "down" and direction != "left" and direction != "right":
        direction = input("'up' 'down' 'left' or 'right'? \n")
        if direction == 'up' or direction =='down' or direction == 'left' or direction == 'right':
            move_on_map(direction)
        else:
            print("I need to keep moving..")
 
#moving on the map and checking for enemies or buildings
def move_on_map(direction):
    if direction.lower() == "up":
        try:
            if current_world[p1.x][p1.y+1].movable == True : #
                p1.y += 1
                move_north_animation()
            else:
                print("You run against the wall. Why tho?")
                okay()
        except :
            print("The world ends before your very eyes. You cannot move any further north.")
            okay()
    elif direction.lower() == "down":
        try:
            if p1.y > 1 and current_world[p1.x][p1.y-1].movable == True:
                p1.y -= 1    
                move_south_animation()
            else:
                print("You run against the wall. Why tho?")
                okay()
        except:    
            print("The world ends before your very eyes. You cannot move any further south.")
            okay()
    elif direction.lower() == "left":
        try:    
            if p1.x >1 and current_world[p1.x-1][p1.y].movable == True:
                p1.x -= 1
                move_west_animation()
            else:
                print("You run against the wall. Why tho?")    
                okay()
        except:    
            print("The world ends before your very eyes. You cannot move any further west.")
            okay()
       
    elif direction.lower() == "right":
        try:
            if current_world[p1.x+1][p1.y].movable == True : #
                p1.x += 1
                move_east_animation()
            else:
                print("You run against the wall. Why tho?")
                okay()
        except:    
            print("The world ends before your very eyes. You cannot move any further east.")
            okay()
    sleep(0.3)
    ground = current_world[p1.x][p1.y]   #checks if ground can spawn enemies
    if ground.spawns_enemy == True:
        global spawn_chance
        rng = randint(1, 100)
        if rng <= spawn_chance:               #rng check for monster spawning
            fight()
    if ground.building != None:     #if moving to a building ask to enter it ; probably to be removed later
            ground.building.open()
 
#some unicode examples: ֎ ۞ ۩ ༓ ༖ ྿ ࿄ ⌂ ⌘ ⌧ ⌲ ⌾ ⑇ ᧰ ࿏ ࿌ ♡ ◙ 
def open_map(): #map mechanic
    for i in range(6,-6,-1): #was (3,-4,-1)
        print("")
        for j in range(-6,6,1): #was (-3,4,1)
            try:
                if i == 0 and j == 0:
                    print("⌾", end = " ")
                elif p1.x + j < 1  or  p1.y + i < 1 :
                    print("⌧", end = " ")
                elif current_world[p1.x + j][p1.y + i].name.lower() == "shop" or current_world[p1.x + j][p1.y + i].name.lower() == "smithy":  #always show shop or smithy
                    print("۩", end = " ")

                elif current_world[p1.x + j][p1.y + i].building == witch_hut:    #witch hut
                    if grandma_quest.ongoing == True or witch.talked == True:
                        print("۩", end = " ")
                    else:
                        print("?", end = " ")
                elif current_world[p1.x + j][p1.y + i].building == fairy_fountain_1: #fairy fountain 1
                    if pendant1.obtained == True:
                        print("♡", end = " ")
                    else:
                        print("?", end = " ")
                elif current_world[p1.x + j][p1.y + i].building == fairy_fountain_2: #fairy fountain 2
                    if pendant2.obtained == True:
                        print("♡", end = " ")
                    else:
                        print("?", end = " ")
                elif current_world[p1.x + j][p1.y + i].npc != None:  # NPC , changes if talked to, works if no building to show
                    if  current_world[p1.x + j][p1.y + i].npc.talked == True:
                        print("ጰ", end = " ")
                    else:
                        print("?", end = " ")
                elif current_world[p1.x + j][p1.y + i].name.lower() == "grassland":  #default grassland
                    print("~", end = " ")
                elif current_world[p1.x + j][p1.y + i].caves != None:        #caves
                    print("◙", end = " ") 
                elif current_world[p1.x + j][p1.y + i].movable == False:
                    print("⌧", end = " ")
                elif current_world[p1.x + j][p1.y + i].name == "Tunnel":        #caveground tile
                    print("~", end = " ") 
                
            except:
                print("⌧", end = " ")
    print("")
    print("⌾ = Your Position\t ~ = Grassland \t\t ۩ = Shop")
    check = ["up", "down", "left", "right"]         #this last snipped makes, that you can give a move command while watching the map, but dont have to
    action = input("").lower()
    if action in check:
        move_on_map(action)
 
#asking for name
def askname():
        name = input("What is your name?\n")
        return name
######################################### fighting #########################################  

#player attack
def pattack():
    dmg = current_weapon.damage
    min= dmg *0.8
    max = dmg *1.2
    dmg = int(uniform(min, max))
    if attackup.counter > 0:
        dmg = int(dmg * (attackup.multiplicator + 1) )
    round(dmg, 0)
    #player crit mechanic          current modifiers: weapon.crit , whetstone from smithy quest
    crit_chance = current_weapon.crit + crit_bonus
    crit_roll = randint(1, 100)
    if crit_chance >= crit_roll:
        dmg *= 2                    #crit pierces enemy armor
        crit_animation(dmg)
    else:
        dmg -= current_enemy.defense    #regular attack has armor substraction
        pattack_animation(dmg)
    current_enemy.hp = current_enemy.hp - dmg
    global damage_done
    damage_done += dmg


#enemy attack
def eattack():
    dmg = current_enemy.atk
    min= dmg *0.8
    max = dmg *1.2
    dmg = int(uniform(min, max))
    if defenseup.counter > 0:
        dmg = int(dmg * defenseup.multiplicator)
    round(dmg, 0)
    p1.hp = p1.hp - dmg
    eattacK_animation(dmg)
 
 
#fighting logic
def fight(enemy = None):
    global flag_fighting
    flag_fighting = True
    if current_enemy.name == "empty":   #spawn slime if 1st fight
        enemy_spawn(slime)
    elif enemy == None:                 #or spawn random enemy if no parameter
        rando = get_enemy()
        enemy_spawn(rando)              
    else :
        enemy_spawn(enemy)              #else spawn certain monster
    print("")
    print (">>> A " + current_enemy.name + " invades your personal space. <<<")
    sleep(1)
  #looping the battle  
    while flag_fighting == True and current_enemy.hp > 0:
        anzeige()
        if take_fighting_command():     #if item is used True is returned and round continues , if False returned round doesnt continue
            if current_enemy.hp > 0:
                eattack()
        #checking if player died lmao
                if p1.hp <= 0:
                    losing()
            buffs_decrement_all()
    #after battle
    p1.gold += current_enemy.gold
    print("You won the battle! You got " + str(current_enemy.gold) + " Gold!")
    buffs_decrement_all(1000)
    loot_roll = randint(1,100)
    if current_enemy.loot_chance > loot_roll:
        current_enemy.loot.increase(current_enemy.lootammount)
        print(f"You found {current_enemy.lootammount} x {current_enemy.loot.name} !")
    global defeated_enemies
    defeated_enemies += 1
    flag_fighting = False
    junk = input("<<leave")

#take command
def take_fighting_command():
    action = input("What do you want to do? Options are : 'attack', 'items', 'watch' \n")
    if (action.lower() == "attack"):
        pattack()
    elif(action.lower() == "run"):
        print(p1.name + ": I shouldn't run from a Tutorial.")
    elif(action.lower() == "items" or action.lower() == "item"):
        return open_inventory()
    elif(action.lower() == "watch"):
        print("You watch the " + current_enemy.name + " doing it's " + current_enemy.name + " things.")
    elif action.lower() == "weeeg":
        current_enemy.hp = 0
        global flag_fighting
        flag_fighting = False
    else:
        print("What could you do in this situation?...")
        take_fighting_command() #I guess a recursion at this line should be fine??
    return True
 
def open_inventory():
    #print the inventory
    print("--------------Consumables--------------")
    for itm in inventory:
        if itm.quantity > 0:
            print(str(itm.quantity) + " x " + itm.get_name() + "\t Nr. " + str(itm.number) + "\t\tuse: " + itm.function )
    print("--------------Importants--------------")
    for i in baseitems:
        if i.obtained == True:
            print(i.get_name() + "\t" + i.function)
    print("--------------Weapons--------------")
    for i in weapons:
        if i.bagged == True:
            print(i.get_name() + "\t" + i.text)
    print("")
    print("You can use something by typing the name or number of the item \t return with 'exit' or '0'\n")
    #inventory screen waits for command; if item is succesfully used return True, if bag is exited return False so rounds in "take_fight_command()" arent used in vain if exited
    flag = True
    while flag == True :
        action = input()
        if action.lower() == "exit" or action.lower() == "0":
            flag = False
            return False
        for itm in inventory:
            if action.lower() == itm.name.lower():
                use_item(itm)
                sleep(1)
                flag = False
                return True
        for wpn in weapons:
            if action.lower() == wpn.name.lower() and wpn.bagged == True:
                print("You replaced your " + current_weapon.name + " with a " + wpn.name + ".")
                sleep(1)
                current_weapon.replace(wpn)
                return True
        try:
            action=int(action) 
            for i in inventory:
                if i.number == action:
                    use_item(i)
                    flag = False
                    return True
        except:
                pass
                            

def open_shop():
    speak("You see a little shop, in there seems to be a friendly elderly Lady. You enter and a chiming bell above the door gives you a cozy feeling.")
    speak("'Welcome, to my shop. Get some items here.'")
    sleep(1)
    print("Current gold:  " + str(p1.gold))
    print("________________________________________________________________________________________")
    print("UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU")
    for i in shop:
        print(i.get_name() + "\t" + str(i.value) + " Gold\t Nr. " + str(i.number) + "\t\t use:  " + i.function)
    print("________________________________________________________________________________________")
    global flag_shopping
    flag_shopping = True            #shopping flag 
    while flag_shopping == True :
        print("You can select items by typing the name, Nr. \t type '0' or 'exit' to go back.")
        action = input()
        if action == "0" or action.lower() == "exit":
            speak("You turn around, leave and slam the door as hard as you can for no reason at all. You hear a vase falling from a shelf behind you.")   
            flag_shopping = False
            return
        for itm in shop:
            if action.lower() == itm.name.lower():
                sure(itm)
        try:
            action=int(action)
            for itm in shop:
                if action == itm.number:
                    sure(itm)    
        except:
            action = ""

def open_witch_hut():
    speak("You see a little hut nearby. You could swear the roof is made of gingerbread. You leave some breadcrumbs on the ground to be sure and enter.")
    speak("'Welcome, to 'The Witchy'. I sell potions. No you can't eat the roof.'")
    sleep(1)
    print("Current gold:  " + str(p1.gold))
    print("________________________________________________________________________________________")
    print("UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU")
    for itm in witch_hut_items:
        print(itm.get_name() + "\t" + str(itm.value) + " Gold\t\t Nr. " + str(itm.number) + "\t\t use:  " + itm.function)
    print("________________________________________________________________________________________")
    global flag_shopping
    flag_shopping = True
    while flag_shopping == True :
        print("You can select items by typing the name, Nr. or type '0' to go back.")
        action = input()
        if action == "0" or action.lower() == "exit":
            speak("You follow the breadcrumbs and leave the hut. You are still raw.")
            flag_shopping = False
        for itm in witch_hut_items:
            if action.lower() == itm.name.lower():
                sure(itm)
        try:
            action=int(action)
            for itm in witch_hut_items:
                if action == itm.number:
                    sure(itm)    
        except:
            pass


#buying item
def sure(item):
    a = item
    if a.value <= p1.gold:
        # print("The " + a.name + " costs " + str(a.value) " gold. Do you want to buy it?\n")
        answer = ""
        while not(answer.lower() in yes_array or answer.lower() in no_array):
            answer = input(a.name + "? For " + str(a.value) +  " Gold? Do you want to buy it? 'Yes' or 'No'\n")
            if answer.lower() in yes_array:
                buy(item)
            elif answer.lower() in no_array:
                print("'Okay?...weird..'")
            else:
                print("'YES' or 'NO'?!\n")
    else:
        speak("'I think this is a bit too expensive sweety.' *The elderly Lady smiles slightly but lovely*")          




# assuring item buy
def buy(item):
    b = item
    amnt = -1
    while amnt < 0 :
        try:
            amnt = int(input("How many do you want to buy?\n"))
        except:
            print("I said HOW MANY?!\n")
    if amnt*b.value > p1.gold :
        print("You cant'even afford this... Stop wasting my time.")
    elif amnt == 1 :
        p1.gold -= b.value * amnt
        inventory[b.number].increase(amnt)
        print("You bought a " + b.name + ".")
    elif amnt > 0 :
        p1.gold -= b.value * amnt
        inventory[b.number].increase(amnt)
        print("You bought " + str(amnt) + "x "  + b.name + ".")
    print("You got " +  str(p1.gold) + " Gold left to spend.")

def sell_pawn_shop():
    global flag_shopping
    flag_shopping = True            #shopping flag 
    while flag_shopping == True :
        print("________________________________________________________________________________________")
        print("UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU")
        for itm in inventory:
            if itm.quantity > 0:
                print(str(itm.quantity) + " x " + itm.get_name() + "\t\t" +  str(int(itm.value/2)) + (4 - len(str(int(itm.value/2))))* " " + "Gold \t Nr. " + str(itm.number) + "\t\tuse: " + itm.function )    # (4 - len(str(int(itm.value/2))))* " " makes the space even depending on the digits of the gold value 
        print("________________________________________________________________________________________")
        print(f"Current gold : {p1.gold} ")
        print("You can select items by typing the name, Nr. \t type '0' or 'exit' to go back.")
        action = input()
        if action == "0" or action.lower() == "exit":
            speak("You value your items far too much to sell them for a price this low. Hoarding always pays off! You leave with your bag full of useless items.")   
            flag_shopping = False
            return
        for itm in inventory: 
            if action == itm.name.lower() and itm.quantity > 0:
                sell(itm)
        try:
            action=int(action)
            for itm in inventory:
                if action == itm.number and itm.quantity > 0:
                    sell(itm)        
        except:
            action = ""


def sell(itm):
    print("So you want to sell some " + itm.name + " , yes?")
    answer = input()
    if answer.lower() in yes_array:
        print("How many do you want to sell?")
        ammount = input()
        try:
            ammount = int(ammount)
        except:
            print("I was asking for a number...whatever. Wanna sell anything else?")
            return
        if ammount <= itm.quantity:
            print(f"Sell {ammount} x {itm.name} for {ammount*int(itm.value/2)} G?")
            answer2 = input()
            if answer2.lower() in yes_array or answer2 == "":
                itm.decrease(ammount)
                price =  int(itm.value/2) * ammount
                p1.gold += price
                print(f"Sold! Got {price} G!")
                okay()
                
            else:
                speak("....Jeez. Anything else?")
                return
        else:
            print("You don't have that many but fine. Wanna sell anything else?") #not enough of that item

    else:
        speak("Okay?...")   #not said "yes" to selling question

#enemy spawning logic
def enemy_spawn(new_enemy):
    global current_enemy
    current_enemy = new_enemy
    current_enemy.hp = new_enemy.maxhp
   
 
def losing(): #loosing logi with stats like: enemies defeated, damage done, unspent gold
    print("Oops. You died. :( ")
    sleep (2)
    print("Stats?? Sure, everybody loves stats. Here are some: ")
    print("Enemies defeated: "+ str(defeated_enemies))
    print("Damage done: " + str(damage_done))
    print("Gold you were too mean to spend: " + str(p1.gold))
    print("")
    print("I will end the game now")
    input()
    exit()


###############################################  conversations  ##############################################################
#function to print text spoken by npcs letter by letter, calling it speak() instead of print()
def speak(text):
    for x in text:
        if x == "." or x == "!" or x == "?":
            sleep(0.2)
        print(x, end ="", flush= True)
        sleep(textspeed)

    junk = input(" ↩ ")

def change_textspeed():
    global textspeed
    if textspeed != 0.005:
        textspeed = 0.005
        speak("People stfu now :P ")
    else:
        textspeed = 0.02
        speak("People talk faster again :P ")
        

def talk():     # talking function
    if current_tile().npc != None:
        print("You engage in a conversation with " + current_tile().npc.name + " : ")
        sleep(1)
        match current_tile().npc.name.lower():
            case "nancy":
                talk_nancy()
            case "grandma":
                talk_grandma()
            case "the smith":
                talk_smith()
            case "the witch":
                talk_witch()
    else:
        print("You have a nice time talking to yourself. Loneliness + 100")
    sleep(1)

#first fairy fountain
def open_fairy_fountain_1():
    if pendant1.obtained == False:
        speak("You see a fountain in the middle of a forest. You wonder why it sparkles glitter. While inspecting it further a fairy pops out of it.")
        speak("'Hello traveler. You seem like you fight a lot of the monsters around.' ")
        speak("'I love to heal people but there are so many monsters hurting them. Thanks for reducing their numbers.' ")
        speak("'Take this pendant. It will boost health and healing.'")
        print("You obtained a " + pendant1.name + ". Your maximum health raised." )
        sleep(1)
        p1.maxhp += 25
        p1.hp = p1. maxhp
        global healing_multiplicator
        healing_multiplicator += 0.2
        pendant1.obtained = True
        speak("'Maybe you will find my sister. I haven't talked to her in 1630 years but she could probably help you too.'")
    else:
        speak("'Hello Traveler. You defeated " + str(defeated_enemies) + " monsters! Let me heal you.'")
        p1.hp = p1.maxhp
        print("Your feel your health filling up!")    
 
#second fairy fountain
def open_fairy_fountain_2():
    if pendant2.obtained == False:
        speak("You are surrounded by the ruins of an old city. The fountain in the middle glows. While inspecting it a fairy pops out of it.")
        speak("'Hello traveler. I heard you cleared a lot of monsters near these ruins. ")
        speak("'I love to heal people but there are so many monsters hurting them. Thanks for Getting rid of 'em.' ")
        speak("'Take this pendant. It will boost health and healing.'")
        speak("You obtained a " + pendant2.name + ". Your maximum health raised." )
        sleep(1)
        p1.maxhp += 25
        p1.hp = p1. maxhp
        global healing_multiplicator
        healing_multiplicator += 0.2
        pendant2.obtained = True
        speak("'Have you heard of my sister? I haven't seen her in 1630 years.. She is so nice i bet she will help you. See ya.'")
    else:
        speak("'Hello Traveler. You defeated " + str(defeated_enemies) + " monsters! Let me heal you. Visit me here and then.'")
        p1.hp = p1.maxhp
        print("Your feel your health filling up!")
        speak("See ya!")    
    junk = input(">>leave")
 
def talk_nancy():
    if nancy.talked == False:
        speak("'Hello traveler, nice meeting you! You seem to fight a lot ! Always stay healthy!'")
        superpotion.increase(1)
        print("Nancy gave you a super potion!")
        speak("You should talk to people at least twice. Some guys have to tell a lot.")
        speak("'Feel free to rest with me " + p1.name + ". I could use some company!'")
        sleep(1)
        nancy.talked = True
    else:
        speak("'There you are again! Please take care of yourself. But not on my money, I need my potions.'")
        speak("'Feel free to rest if you feel low on health.")
        rest()

def talk_grandma():
    if grandma.talked == False:
        speak("'Hello sweety. Welcome to my shop. I recommend the cookies. But I also sell potions.'")
        speak("'I have some expired ones I can't sell anymore but they still do fine. You can have these if you want to.'")
        potion.increase(3)
        speak("You received 3 Potions")
        speak("'Stay safe out there. Or stay as long as you want sweetheart. Oh... where did I put the herbs?...'")
        grandma.talked = True
    else:
        speak("'Nice to see you again darling. Are you doing well? Sit down and relax a bit.'")
        if grandma_quest.done == False:
                grandma_quest_function()

        

def talk_smith():
    speak("'Talk to me if you want to buy a weapon. I'm busy here.'")
    if  smithy_quest.done == False:
        if smithy_quest.ongoing == False:
            speak("'... But you could also help me...There is a Baby Dragon in my backyard. It keeps setting my wood piles up on fire, this pest. Could you get rid of it?.. '")
            speak("But please care, even a baby dragon is kinda hard to fight! Better have potions..")
            smithy_quest.take()
        elif questflag_smith_dragon == True:
            speak("'The Drag-? OH! Thank you, I finally got rid of this thing. Take this as a reward'")
            whetstone.obtained = True
            print("You receive a Whetstone.")
            global crit_bonus
            crit_bonus += 5
            smithy_quest.finish()
            sleep(1)
            speak("'......Ok that's it. Stop staring at me. Bye'")
        else:
            speak("'Have you killed this thing already?'")

def talk_witch():
    global questflag_witch_herbs
    if witch.talked == False:
        speak("'Hello my tast- handsome child. I sell REAL potions here! And also ingredients..'")
        speak("'I'm also looking for a student. It might get patched in one day. <|:^) '")
        speak("'Well it's your lucky day! You may bugfix it!'")
        cauldron.obtained = True
        speak("You obtained the cauldron!!!!!!")
        sleep(2)
        speak("'You may throw up to 3 things in it! Just fill it up with Healing Herbs.... Or... A Potion and Healing Herbs?... I can't remember... I KNOW IT'S MY JOB!' ")
        witch.talked = True
    else:
        speak("'There you are again sweet, SWEET young child. You look starved! I hope you are eating a LOT.'")
    if grandma_quest.ongoing == True and questflag_witch_herbs == False:
        speak("'Hm? Healing Herbs? It's 5 Gold per He-... For my cousin? AGAIN?! She should take her business more serious. She keeps on running out of stock all the time..Take these'")
        speak("You received 5 healing herbs. SAVE THEM FOR GRANDMA!")
        healingherb.increase(5)
        questflag_witch_herbs = True
    

############################################### quests ##############################################################

def smithy_quest_fight():
    speak("You see a tiny Dragon near the pile of wood behind the smithy. Fire is shooting out of it's nose. It is time to fight this thing before it starts a wildfire.'")
    enemy_spawn(dragon)
    fight(dragon)
    global questflag_smith_dragon
    questflag_smith_dragon = True
    speak("You defeated the dragon..You should talk to the smith.")

def grandma_quest_function():
    if grandma_quest.ongoing == False:
        speak("'..My poor back. The road will kill me......Where I am heading? To my cousin. I am out of healing herbs so I can't brew new potions.'")
        speak("'You would help me? Oh darling you don't need to-... Well fine. I can't afford saying no with my back. Take care my handsome hero.")
        grandma_quest.take()
    elif healingherb.quantity >= 5:
        speak("'Oh you got the herbs for me... You are incredible darling! Wait here I will brew some potions for you aswell..'")
        print("You couldn't watch grandma work so much. You helped her in the store while waiting.")
        sleep(2)
        healingherb.decrease(5)
        superpotion.increase(3)
        speak("'Thank you for everything darling. Take these Super Potions for the hustle. And some money for cleaning the store.'")
        p1.gold += 100
        grandma_quest.finish()
    else:
        speak("'I can't let you walk all the way to my cousin without proper rest. You know sometimes monsters can carry herbs aswell!'")

# flags
questflag_smith_dragon = False
questflag_witch_herbs = False
###############################################  ascii art and animations stuff  ##############################################################


def cauldron_animation():
    for i in range(4):
        if i % 2 == 0:
            os.system('cls')
            print("              ("          ,  )
            print("               )  )"       , )
            print("           ______(____"    , )
            print("          (___________)"  , )
            print("           /         \\"  , )
            print("          /           \\"  , )
            print("         |             |"  , )
            print("     ____\\             /____"  , )
            print("    ()____'.__     __.'____()"  , )
            print("         .'` .'```'. `-."  , )
            print("        ().'`       `'.()"  , )
        if i % 2 == 1:
            sleep(0.7)
            os.system('cls')

            print("               )  )     "  , )
            print("                 (      "   , )
            print("           _____(_____  "  , )
            print("          (___________)" , )
            print("           /         \\" , )
            print("          /           \\",  )
            print("         |             |" , )
            print("     ____\\             /____" , )
            print("    ()____'.__     __.'____()",  )
            print("         .'` .'```'. `-." , )
            print("        ().'`       `'.()" , )

            sleep(0.7)

def crit_animation(damage = ""):
    x = 70      #lenght of cut
    figure = "( ◡_◡́)--▬▬ι═══════ﺤ"
    figure_open_eye = "( •_•̀)--▬▬ι═══════ﺤ"
    for _ in range(2):
        for i in range(10):
            print(int((x/2))*" " + i*"/", end = "\r")
            sleep(0.004)
    print((x+10)*" ", end= "\r")        
    sleep(0.5)
    print(x*"-", end= "")
    print(figure, end = "\r")
    sleep(0.23)
    for i in range(x+1):
        print(i * " " + (x-i)*"-" + figure, end = "\r", flush = True)
        sleep(0.001)
    sleep(0.35)
    print(x*" " + figure_open_eye, end ="\r", flush = True)
    sleep(0.6)
    print(40*" " + "CRIT ! " + str(damage) + " damage!" , end ="\r", flush = True)
    sleep(0.5)
    print("")

def pattack_animation(damage = "some"):
    array = [" ( /ಠ益ಠ)ノ "," (\\ ಠ益ಠ)  "," ( /ಠ益ಠ)/  "," ( ᴖಠ益ಠ)ᴖ  "," ( ᴖಠ益ಠ)ᴖ ⇲"," ( ᴖಠ益ಠ)ᴖ *"," ( ᴖಠ益ಠ)ᴖ ⌑"," ( ᴖಠ益ಠ)ᴖ  "] 
    for i in array:
        print(i, end = "\r",flush = True)
        if i == " ( /ಠ益ಠ)ノ " or i == " (\\ ಠ益ಠ)  ":
            sleep(0.22)
        else:
            sleep(0.045)
    sleep(0.3)
    x = int((damage /p1.maxhp)*10)
    s = " " + x*"♥" 
    if x == 0:
        s = " ♡"
    print(" ( ᴖಠ益ಠ)ᴖ  \t dealt " + str(damage) + s + " damage!" , end ="\r", flush = True)
    sleep(0.5)
    print("")

def eattacK_animation(damage = ""):
    array = [" ( ๐ Д ๐ )  ", " (┳ Д ┳  )¤¤", " (┳ Д ┳  )° ", " (┳ Д ┳  )³ ", " (┳ Д ┳  )  ", " ( ┳ Д ┳ )  ", " (  ┳ Д ┳)  "]
    for i in array:
        print (i, end = "\r", flush = True)
        if i == " ( ๐ Д ๐ )  " or i == " (┳ Д ┳  )  ":
            sleep(0.45)
        elif i == " ( ┳ Д ┳ )":
            sleep(0.07)
        else:
            sleep(0.05)
    sleep(0.3)
    x = int((damage /p1.maxhp)*10)
    s = " " + x*"♥"
    if x == 0:
        s = " ♡"
    print(" (  ┳ Д ┳) \t took " + str(damage) + s +" damage!" , end ="\r", flush = True)
    sleep(0.5)
    print("")

def move_north_animation():
    a = [" ┌(      )┘ \tYou moved north."," └(      )┐ \tYou moved north."]
    for _ in range(3):
        for i in a:
            print(i, end = "\r")
            sleep(0.27)
    print("")

def move_south_animation():
    a = ["  (.‿  . )\ \tYou moved south."," /( . ‿ .)  \tYou moved south."]
    for _ in range(3):
        for i in a:
            print(i, end = "\r")
            sleep(0.27)
    print("")

def move_east_animation():
    a=[" (  _ ^0) \tYou moved east."," ( _ ^0^) \tYou moved east."," (  _ ^0) \tYou moved east."," (   _ ^) \tYou moved east."," (    _ ) \tYou moved east.",]
    for _ in range(3):
        for i in a:
            if i == " ( _ ^0^) \tYou moved east." or i == "  (    _ ) \tYou moved east.":
                print(i, end = "\r")
                sleep(0.25)
            else:
                print(i, end = "\r")
                sleep(0.1)
    print("")

def move_west_animation():
    a=[" (w^ _  ) \tYou moved east."," (^w^ _ ) \tYou moved east."," (w^ _  ) \tYou moved east."," (^ _   ) \tYou moved east."," ( _    ) \tYou moved east.",]
    for _ in range(3):
        for i in a:
            if i == " (^w^ _ ) \tYou moved east." or i == " ( _    ) \tYou moved east.":
                print(i, end = "\r")
                sleep(0.25)
            else:
                print(i, end = "\r")
                sleep(0.1)
    print("")


###############################################  debugging  ##############################################################

def debugging():        #taking debug option
    action = print("What do you want to do?")
    action = input("Options are: 'item' , 'teleport' , 'fight' , 'gold' , 'heal' , 'mana', 'buff', 'stfu', 'repel' , 'cauldron' , 'sell' \n")
    action = action.lower()
    match action:
        case "teleport":
            teleport_debug()
        case "fight":
            fight()
        case "gold":
            p1.gold += 1000
            print("You magically find 1000 gold on the ground!")
        case "heal":
            p1.hp = p1.maxhp
            print("You fully healed.")
        case "mana":
            p1.maxmana = 100
            p1.mana = p1.maxmana
            print("Your have mana and filled it up!")
        case "buff":
            for i in buff_array:
                i.buff(10)
            print("You feel DAMN buffed!")
        case "stfu":
            change_textspeed()
        case "cauldron":
            cauldron.obtained = True
            print("A cauldron spawned magically in your pocket.")
        case "item":
            a = input("Which item?")
            for b in inventory:
                if a.lower() == b.name.lower(): 
                    b.increase(99)
                    print(f"You found a bunch of {b.name} !")
        case "repel":
            global spawn_chance
            spawn_chance = 0  if spawn_chance == 40 else 40
            print(f"The spawn chance changed to {spawn_chance} %.") 
        case "sell":
            sell_pawn_shop()
        case _:
            print("Fine. Keep your debugging for yourself then.")
        

def teleport_debug():       #teleport to a certain coordinate
    x = int(input("x coordinate? : "))
    y = int(input("y coordinate? : "))
    try:
        if current_world[x][y].movable == True:
            p1.x = x     
            p1.y = y
            print(f"You teleported to [{x}] [{y}].")
        else : print("invalid")
    except:
        print("Well thats a terrible coordinate, i should stay here")

############################################### Convenience code #########################################################
def set_numbers(array:list):    #im tired of numbering the items manually, here is a function
    j = 0
    for i in array:
        i.number = j
        j+=1        

set_numbers(inventory) #set numbers on all items
set_numbers(weapons)   #set numbers on all weapons
set_numbers(enemies)   #set numbers on all enemies

def okay():
    junk = input(" ↩ ")


current_world = worldmap        #current_world checks whatever world you are in right now, it changes depending wheter you are in the worldmap or eg. in a cave or smn
########################################################################################################################


#main
print("Hi! Welcome to my Text RPG.")
 # sleep(1)
print("This is the first Program I have written. It's mainly to try out coding.")
# sleep(1)
print("Hope u have fun!")
print("Let's create your Character!")
# sleep(1)
 
#creating Player , Enemy, etc -instances        
p1 = player(askname(), 100 ,100, 0, 2 , 2, 0, 0)
current_weapon = woodensword
current_enemy = enemy("empty", 0, 0, 0, 0)
 
# sleep(1)
print ("Hi " + p1.name + ".")
# sleep(1)
print ("The adventure is about to start!")
# sleep(1)
print("let me prepare some things..")
# sleep(2)
anzeige()
# sleep(1)
print("^ That's your Bar. It will show stuff like your HP and coordinates on the map.")
# sleep(1)
# print("Let's start with a fight! A Slime will do it")
# print("...")
# # fight()
# # print("Wonderfull. You defeated your first enemy. As you saw you get gold to spend.")
 
print ("Explore the map! If you have too much Gold , try to open the map and visit the houses. Have fun!")
while True:     #game loop
    take_menu_command()
 
anzeige()
print ("end of code")