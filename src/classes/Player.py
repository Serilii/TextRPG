if __name__ == "__main__":
    #debugger silencer
    from core.variables import *
    from classes.Player import player
    p1 = player("", 0,0,0,1,1,0,0)

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


def player_healthbar():    #returns healthbar as string ♡♥
    x = p1.hp/p1.maxhp
    x = int(x*10)
    s = x*"♥" + (10-x)*"♡"
    return s
