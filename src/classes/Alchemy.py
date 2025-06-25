#contains everything alchemy related:
#   "recipy" class
#   "cauldron" action and its according crafting algorythm

if __name__ == "__main__":
    #debugger silencer
    from core.variables import *
    from classes.Item import *
    import os
    from time import *
    from src.main import *
    p1 = player("", 0,0,0,1,1,0,0)

from classes.Item import *

#putting all recipies into list for iteration
recipy_book  = []

class recipy:
    def __init__(self, name, first: item, second: item, third: item , product:item, product_ammount):
        self.name = name
        self.ingredients = [first, second, third]
        self.product = product
        self.product_ammount = product_ammount
        recipy_book.append(self)

    def check(self, blob):
        rezept = self.ingredients.copy()     # = recipy array
        topf = blob.copy()                  # = input array
        for i in topf:              #checks if parameter array and this recipy array are the same by deleting same items and checking if array is emtpy
            if i in rezept:
                    rezept.remove(i)
        if rezept == []:
            cauldron_animation()
            print("")
            for i in self.ingredients:
                i.decrease(1)
            self.product.increase(self.product_ammount)
            return True
        else:
            return False
            

#safe the recipies with their parameter
potion_recipy = recipy("Potions", healingherb, healingherb, healingherb, potion, 5 )
super_potion_recipy = recipy("Super Potions", potion, healingherb, healingherb, superpotion, 4 )
defense_potion_recipy = recipy("Defense Potion", potion, stone, stone, defensepotion, 1)
attack_potion_recipy = recipy("Attack Potion", potion, batfang, batfang, attackpotion, 2)



def open_cauldron():        #cauldrons crafting logic!
    flag_alchemy = True
    ingredients = []
    while flag_alchemy == True and len(ingredients) < 3 :     #starting alchemy loop
        cauldron_list()
        print("")
        print("What do you want to throw into the cauldron? \t '0' or 'exit' to leave")
        if ingredients != []:
            print("currently in the cauldron: ", end = "" )        #printing the current things in the cauldron
            for j in ingredients:
                print(j.name, end = " , ", flush = True)
        
        action = input()  # naming the ingredient
        print("", end = "\r")
        if action == "0" or action.lower() == "exit":           #exit cauldron
            for h in ingredients:
                h.increase(1)
            cauldron_list()
            flag_alchemy = False
            return
        for k in inventory:
            if action.lower() == k.name.lower() and k.quantity > 0:
                ingredients.append(k)
                k.decrease(1)
    print("")
    for i in recipy_book:                                       #check if ingredients check with a recipy
        if i.check(ingredients) :
            print(f"You crafted {i.product_ammount} x {i.name}!")
            print("")
            return
    speak("...Your ingredients swim around, unwilling to to do anything remarkably...")
    for e in ingredients:
        e.increase(1)       # this line makes that insuccesfull crafting gives items back. If someone would just delete it....
    cauldron_list()
    sleep(1)        
    
def cauldron_list():        #needed for the open cauldron function, it's here for convenience bc i need it again at the end without looping again uwu
    os.system('cls')
    print("-------------- Ingredientes --------------")
    for itm in inventory:
        if itm.quantity > 0:
            print(str(itm.quantity) + " x " + itm.get_name() + "\t\tuse: " + itm.function )     

def cauldron_animation():
    for i in range(4):
        if i % 2 == 0:
            os.system('cls')
            print("              ("          ,  )
            print("               )  )"       , )
            print("           ______(____"    , )
            print("          (___________)"  , )
            print("           /         \\"  , )
            print("          /           \\"  , )
            print("         |             |"  , )
            print("     ____\\             /____"  , )
            print("    ()____'.__     __.'____()"  , )
            print("         .'` .'```'. `-."  , )
            print("        ().'`       `'.()"  , )
        if i % 2 == 1:
            sleep(0.7)
            os.system('cls')

            print("               )  )     "  , )
            print("                 (      "   , )
            print("           _____(_____  "  , )
            print("          (___________)" , )
            print("           /         \\" , )
            print("          /           \\",  )
            print("         |             |" , )
            print("     ____\\             /____" , )
            print("    ()____'.__     __.'____()",  )
            print("         .'` .'```'. `-." , )
            print("        ().'`       `'.()" , )

            sleep(0.7)
