if __name__ == "__main__":
    #debugger silencer
    from core.variables import *
    from classes.Player import player
    p1 = player("", 0,0,0,1,1,0,0)
    from src.main import *
    from classes.Item import *
    from classes.Cave import *
    from classes.Enemy import *

from copy import *
from classes.Tile import empty
from classes.Tile import *



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



