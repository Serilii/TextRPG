#common libraries 
from random import *
from time import *
from copy import *
import os

#importing core setup (like needed variables)
from core.variables import *

#importing classes
from classes.Item import *
from classes.Building import *
from classes.Cave import *
from classes.Tile import *
from classes.Alchemy import *
from classes.Baseitem import *
from classes.Buff import *
from classes.Enemy import *
from classes.Npc import *
from classes.Player import *
from classes.Quest import *
from classes.Weapon import *


from core.animations import *
from core.imports import *
from core.variables import *
from core.visuals import *


from logic.battle import *
from logic.conversations import *
from logic.debugging import *
from logic.fairy_fountain_logics import *
from logic.shop_logics import *

cave1_map = [[deepcopy(empty) for x in range(10)] for y in range(10)]   #10 x 10 array with all empty tiles
for i in cave1_map:                          #a line of caveground
    i[4] = deepcopy(caveground)

cave1_map[9][4].item = attackpotion

cave1 = cave("Tunnel", 1, 4,cave1_map, enemies_cave1 )

worldmap[1][8] = cave1_tile