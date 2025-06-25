#some debugging tools 

if __name__ == "__main__":
    #debugger silencer
    from src.main import *
    from src.core.visuals import *
    from src.logic.shop_logics import *

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
            selling_permission.obtained = True
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
