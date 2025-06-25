#class for tiles, also contains the world generation

if __name__ == "__main__":
    #debugger silencer
    from core.variables import *
    from core.variables import *
    from classes.Player import player
    from classes.Building import *
    from classes.Tile import *
    p1 = player("", 0,0,0,1,1,0,0)
    from copy import *
    
from classes.Cave import *
from classes.Item import *
from classes.Npc import *
from classes.Building import *
from core.variables import *

class tile:
    def __init__(self, name, spawns_enemy, building, npc:npc = None, item:item = None, caves = None, movable = True):
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

#creating some cave-tiles
caveground = tile("Tunnel",True, None, )
empty = tile("empty",False, None,None,None,None,False)
cave1_tile = tile("Tunnel entrance", False, None, None, None,)   # overworld tile for cave1


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
