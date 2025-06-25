# visual elements / GUI elements
#   hp-bar
#   text generation / -speed  

if __name__ == "__main__":
    #debugger silencer
    from src.core.variables import *
    from classes.Player import *
    p1 = player("", 0,0,0,1,1,0,0)
    from src.main import *
    from classes.Enemy import *
    from classes.Buff import *

import os


# ###############################################  Status Bar  ##############################################
def anzeige():
    os.system('cls')
    x = len(p1.name) - len(current_enemy.name)  
    x = -x if x < 0 else 0                          
    y = len(current_enemy.name) - len(p1.name)
    y = -y if y < 0 else 0                          #these 4 lines determine the distance needed to display Enemy name and Player name in on row
    a = len(p1.name) - len("Position")  
    a = -a if a < 0 else 0
    b =  len("Position") - len(p1.name)
    b = -b if b < 0 else 0

    print()
    if flag_fighting == True:
        print("////////////////////////////////////////////////////////////////////////////////////////")
        print("|؏࿉࿈|\t" + p1.name + (x+4)* " " + player_healthbar() + " HP: " + str(int(p1.hp)) + " / " + str(p1.maxhp) + "    Weapon: " + current_weapon.name + (("\tMana: " + str(p1.mana) + " / " + str(p1.maxmana)) if p1.mana > 0 else "" ))
        print("|༖༗࿇|\t" + current_enemy.name + (y+4)* " " + enemy_healthbar() + " HP: " + str(current_enemy.hp) + " / " + str(current_enemy.maxhp))
        print(r"\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\")
        for i in buff_array:
            if i.counter > 0:
                print(f"⬆ {i.name} for {i.counter} rounds" )
    else:
        print("________________________________________________________________________________________")
        print("|؏࿉࿈|\t" + p1.name + (a+4)*" " + "HP: " + str(int(p1.hp)) + " / " + str(p1.maxhp) + "    Weapon: " + current_weapon.name + (("\tMana: " + str(p1.mana) + " / " + str(p1.maxmana)) if p1.mana > 0 else "" ) + "    Gold: " + str(p1.gold) )
        print("|༖༗࿇|\tPosition"+ (b+4)*" " + "X(⇄) : " + str(p1.x) + "  Y(⇅): " + str(p1.y) + "\t\tArea: " + current_world[p1.x][p1.y].name)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


###############################################  conversations  ##############################################################
# letters appear one by one, so it looks like a spoken npc text
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
        