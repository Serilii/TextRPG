if __name__ == "__main__":
    #debugger silencer
    from core.variables import *
    from classes.Player import *
    p1 = player("", 0,0,0,1,1,0,0)
    from src.main import *
    from classes.Enemy import *
    from core.animations import *
    from classes.Baseitem import *
    from core.variables import *

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
                            
