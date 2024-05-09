from enemies import *
from Baseitems import *
from item import *
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


#put your base items into here!!!! :
baseitems = [artifact, pendant1, pendant2, whetstone, cauldron]

#packing every item into inventory
inventory = [dummy, potion, testitem, stone, bottle, superpotion, healingherb, attackpotion, defensepotion, batfang, slime_item]

shop = [potion, stone, bottle, superpotion ]
witch_hut_items = [healingherb, attackpotion, defensepotion]
