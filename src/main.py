
############################################################################# Interlude ############################################################################################

# Welcome. What you see here is the very first project with which I learned the basics of programing. 
# You might find some weird code snippets here or there because I learn the best by doing it myself.
# To run the application in the current state clone the repo and run it in your IDE's terminal. Sounds weird but you will probably enjoy some minor animations ;)

####################################################################################################################################################################################
#ideas : magic system, defensive options (shields, dodges), option to show enemy stats

from core.imports import *



#asking for name
def askname():
        name = input("What is your name?\n")
        return name
    
p1 = player(askname(), 100 ,100, 0, 2 , 2, 0, 0)



####################################### class for base items ####################################


####################################### class for buildings ####################################



####################################### class for caves #####################################

####################################### class for NPCs #####################################

####################################### class for tiles ####################################




############################################ class for quests #############################################

############################################ class for buffs #############################################

############################################ alchemy #############################################

############################################ functions #############################################



def help_actions():
    speak("some easy commands you can try: up/down/left/right , explore , talk , map , items , quests")

# worldmap menu logic
def take_menu_command():
    sleep(0.1)
    anzeige()
    print("You are resting surrounded by a " +  get_current_tile_name() + ".")
    if p1.hp / p1.maxhp < 0.4 and get_current_tile_name().lower() == "grassland":
        print("You feel pretty tired... You could use a round of sleep..")
    sleep(0.1)
    print(" ( º ֊ º)ᕤ  What's next? Say 'help' if you need some!")
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
            case "help" :
                help_actions()
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


######################################### fighting #########################################  









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

###############################################  debugging  ##############################################################

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

