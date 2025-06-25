if __name__ == "__main__":
    #debugger silencer
    from core.variables import *
    from classes.Cave import *
    from classes.Item import inventory
    from random import *
from classes.Item import *

#enemy list for iteration
enemies = []
current_enemy = None

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
        enemies.append(self)


    def heal(self, value):
        self.hp += value
        if self.hp > self.maxhp:    #anti overheal
            self.hp = self.maxhp

    def get_name(self):         #get the name with the right \t format
        x = 1-(len(self.name) // 8)
        y = self.name + x*"\t" + "    "
        return y

#creating some enemys                #lootchances are in % x 100 (natural numbers idk)
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


enemies_cave1 = [dummy, slime, bat]

#return one enemy of this array
def get_enemy():
    global current_world
    if current_world == cave1_map:
        r = enemies_cave1[randint(1,len(enemies_cave1)-1)]    
    else:
        r = enemies[randint(1,len(enemies)-1)]
    return r


#enemy spawning logic
def enemy_spawn(new_enemy):
    current_enemy = new_enemy
    current_enemy.hp = new_enemy.maxhp


def enemy_healthbar():    #returns healthbar as string ♡♥
    x = current_enemy.hp/current_enemy.maxhp
    x = int(x*10)
    s = x*"♥" + (10-x)*"♡"
    return s
