# logic for all kinds of shops.
# refactoring needed for cleaner overview and new shops

if __name__ == "__main__":
    #debugger silencer
    from core.variables import *
    from classes.Player import *
    p1 = player("", 0,0,0,1,1,0,0)
    from src.main import *
    from classes.Enemy import *
    from classes.Buff import *
    from classes.Building import *
    from core.visuals import *

from classes.Item import *
from classes.Weapon import *

smithy = [woodensword, baseballbat, katana, bow, steelsword, axe, spear]
shop = [potion, stone, bottle, superpotion ]
witch_hut_items = [healingherb, attackpotion, defensepotion]


##################################### smithy #################################
def open_smithy():
    global flag_shopping
    speak("The further you follow the rising smoke the louder the sound of hammering metal gets. A silent man is heating up the forge. You enter. ")
    speak("'Welcome. I sell weapons.")
    sleep(1)
    flag_shopping = True
    while flag_shopping == True :
        print("")
        print("Current gold:  " + str(p1.gold))
        print("________________________________________________________________________________________")
        print("UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU")
        for i in smithy:
            print(i.get_name() + "\t" + str(i.price) + " Gold     \tNr. " + str(i.number) + "\t\t use:  " + i.text)
        print("________________________________________________________________________________________")
        print("You can buy weapons by typing the name or Nr. \t type '0' or 'exit' to go leave.")
        action = input()
        if action == "0" or action.lower() == "exit":
            speak("As the smith hammers the steel a spark flies into your eye. One of your eyes whitnesses you leaving the smithy. Ouch..")   
            flag_shopping = False
            return
        if action.lower() == "sell":
            sell_pawn_shop()
        for wpn in smithy:
            if action.lower() == wpn.name.lower():
                buy_weapon(wpn)
        try:
            action=int(action)
            for wpn in smithy:
                if action == wpn.number:
                    buy_weapon(wpn)
        except:
            pass    

def buy_weapon(wpn):
    a = wpn
    if a.bagged == False and current_weapon.name != a.name :        
        if a.price <= p1.gold:
                q = ""
                while not(q.lower() in yes_array or q.lower() in no_array) :
                    q = input("Do you want to buy the " + a.name + "? 'Yes' or 'No'?\n")
                    if q.lower() in yes_array:
                        current_weapon.replace(a)
                        p1.gold -= a.price
                        print("You bought and equiped a " + a.name)
                        sleep(0.5)
                    elif q.lower() in no_array:
                        print("Then don't waste my time!")
        else:
            speak("You can't afford this. *The smith exhales loduly*")    
    else:
        print("You already have this weapon.")


########################################## shop ######################################

def open_shop():
    global flag_shopping
    flag_shopping = True            #shopping flag 
    speak("You see a little shop, in there seems to be a friendly elderly Lady. You enter and a chiming bell above the door gives you a cozy feeling.")
    speak("'Welcome, to my shop. Get some items here.'")
    sleep(1)
    while flag_shopping == True :
        print("Current gold:  " + str(p1.gold))
        print("________________________________________________________________________________________")
        print("UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU")
        for i in shop:
            print(i.get_name() + "\t" + str(i.value) + " Gold\t Nr. " + str(i.number) + "\t\t use:  " + i.function)
        print("________________________________________________________________________________________")
        print("You can buy items by typing the name, Nr. \t type '0' or 'exit' to go back.")
        action = input()
        if action == "0" or action.lower() == "exit":
            speak("You turn around, leave and slam the door as hard as you can for no reason at all. You hear a vase falling from a shelf behind you.")   
            flag_shopping = False
            return
        if action.lower() == "sell":
            sell_pawn_shop()
        for itm in shop:
            if action.lower() == itm.name.lower():
                sure(itm)
        try:
            action=int(action)
            for itm in shop:
                if action == itm.number:
                    sure(itm)    
        except:
            action = ""


################################# with hut ##################################


def open_witch_hut():
    global flag_shopping
    flag_shopping = True
    speak("You see a little hut nearby. You could swear the roof is made of gingerbread. You leave some breadcrumbs on the ground to be sure and enter.")
    speak("'Welcome, to 'The Witchy'. I sell potions. No you can't eat the roof.'")
    sleep(1)
    while flag_shopping == True :
        print("")
        print("Current gold:  " + str(p1.gold))
        print("________________________________________________________________________________________")
        print("UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU")
        for itm in witch_hut_items:
            print(itm.get_name() + "\t" + str(itm.value) + " Gold\t\t Nr. " + str(itm.number) + "\t\t use:  " + itm.function)
        print("________________________________________________________________________________________")
        print("You can buy items by typing the name, Nr. or type '0' to go back.")
        action = input()
        if action == "0" or action.lower() == "exit":
            speak("You follow the breadcrumbs and leave the hut. You are still raw.")
            flag_shopping = False
        if action.lower() == "sell":
            sell_pawn_shop()        
        for itm in witch_hut_items:
            if action.lower() == itm.name.lower():
                sure(itm)
        try:
            action=int(action)
            for itm in witch_hut_items:
                if action == itm.number:
                    sure(itm)    
        except:
            pass






# assuring item buy
def buy(item):
    b = item
    amnt = -1
    while amnt < 0 :
        try:
            amnt = int(input("How many do you want to buy?\n"))
        except:
            print("I said HOW MANY?!\n")
    if amnt*b.value > p1.gold :
        print("You cant'even afford this... Stop wasting my time.")
    elif amnt == 1 :
        p1.gold -= b.value * amnt
        inventory[b.number].increase(amnt)
        print("You bought a " + b.name + ".")
    elif amnt > 0 :
        p1.gold -= b.value * amnt
        inventory[b.number].increase(amnt)
        print("You bought " + str(amnt) + "x "  + b.name + ".")
    print("You got " +  str(p1.gold) + " Gold left to spend.")



def sell(itm):
    print("So you want to sell some " + itm.name + " , yes?")
    answer = input()
    if answer.lower() in yes_array:
        print("How many do you want to sell?")
        ammount = input()
        try:
            ammount = int(ammount)
        except:
            print("I was asking for a number...whatever. Wanna sell anything else?")
            return
        if ammount <= itm.quantity:
            print(f"Sell {ammount} x {itm.name} for {ammount*int(itm.value/2)} G?")
            answer2 = input()
            if answer2.lower() in yes_array or answer2 == "":
                itm.decrease(ammount)
                price =  int(itm.value/2) * ammount
                p1.gold += price
                print(f"Sold! Got {price} G!")
                okay()
                
            else:
                speak("....Jeez. Anything else?")
                return
        else:
            print("You don't have that many but fine. Wanna sell anything else?") #not enough of that item

    else:
        speak("Okay?...")   #not said "yes" to selling question
        
        
        
############################# pawn shop (experimental) #################################
        
def sell_pawn_shop():
    if selling_permission.obtained == False:
        print("You feel too embarassed to ask.. (๑﹏๑//) ")
        return
    global flag_shopping
    flag_shopping = True            #shopping flag 
    while flag_shopping == True :
        print("________________________________________________________________________________________")
        print("UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU")
        for itm in inventory:
            if itm.quantity > 0:
                print(str(itm.quantity) + " x " + itm.get_name() + "\t\t" +  str(int(itm.value/2)) + (4 - len(str(int(itm.value/2))))* " " + "Gold \t Nr. " + str(itm.number) + "\t\tuse: " + itm.function )    # (4 - len(str(int(itm.value/2))))* " " makes the space even depending on the digits of the gold value 
        print("________________________________________________________________________________________")
        print(f"Current gold : {p1.gold} ")
        print("You can sell items by typing the name, Nr. \t type '0' or 'exit' to go back.")
        action = input()
        if action == "0" or action.lower() == "exit":   
            return
        for itm in inventory: 
            if action == itm.name.lower() and itm.quantity > 0:
                sell(itm)
        try:
            action=int(action)
            for itm in inventory:
                if action == itm.number and itm.quantity > 0:
                    sell(itm)        
        except:
            action = ""

#buying item
def sure(item):
    a = item
    if a.value <= p1.gold:
        # print("The " + a.name + " costs " + str(a.value) " gold. Do you want to buy it?\n")
        answer = ""
        while not(answer.lower() in yes_array or answer.lower() in no_array):
            answer = input(a.name + "? For " + str(a.value) +  " Gold? Do you want to buy it? 'Yes' or 'No'\n")
            if answer.lower() in yes_array:
                buy(item)
            elif answer.lower() in no_array:
                print("'Okay?...weird..'")
            else:
                print("'YES' or 'NO'?!\n")
    else:
        speak("'I think this is a bit too expensive sweety.' *The elderly Lady smiles slightly but lovely*")          
