if __name__ == "__name__":
    from starting_variables import *
    from main import *
    from main import speak
    from main import sell_pawn_shop

# from main import speak
####################################### class for weapons ####################################
class weapon:
    def __init__(self, name, damage, crit, price, text)  :
        self.name = name
        self.damage = damage
        self.crit = crit
        self.price = price
        self.number = 0
        self.text = text
        self.bagged = False

    def replace(self, weapon):
        global current_weapon
        weapons[current_weapon.number].bagged = True
        current_weapon = weapon
        weapon.bagged = False  

    def get_name(self):         #get the name with the right \t format
        x = 2-(len(self.name) // 8)
        y = self.name + x*"\t"
        return y

#creating weapons
dummy = weapon("dummy", 0, 0, 0, "")
woodensword = weapon("Wood Sword", 13, 5, 40, "A sword made of wood. Good for training")
baseballbat = weapon("Baseball Bat", 29, 1, 180, "Higher base damage. Also good for homeruns")
katana = weapon("Katana", 50, 20, 600, "Damage, Crit, Anime")
bow = weapon("Bow", 13, 60, 80, "Lower Damage but High Critical")
steelsword = weapon("Steel Sword", 20, 8, 150,  "Solid Weapon to fight solid monsters" )
axe = weapon("Axe", 38, 10, 280, "Nice for chopping trees. Also good for chopping evil.")
spear = weapon("Spear", 27, 25, 250, "Good range, Nice crits. Throwing things is awesome." )

#packing weapons into array
weapons = [dummy, woodensword, baseballbat, katana, bow, steelsword, axe, spear]
smithy = [woodensword, baseballbat, katana, bow, steelsword, axe, spear]

#opening smithy
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


