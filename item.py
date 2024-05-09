if __name__ == "__main__":
    from starting_variables import *
    from main import *


####################################### class for regular items ####################################
class item:
    
    name = ""
    value = 0
    quantity = 0
    healing = 0
    function = ""
    number = 0
    potion = False

    
    def __init__(self, name, value, quantity, healing, function : str, potion = False):
        self.name = name
        self.value = value
        self.quantity = quantity
        self.healing = healing
        self.function = function
        self.number = 0
        self.potion = potion

    def increase(self, ammount):
        self.quantity += ammount

    def decrease(self, ammount):
        if self.quantity >= ammount:
            self.quantity -= ammount
        else:
            self.quantity = 0
    def heal(self):
        if self.quantity > 0:
            self.decrease(1)
            heal = int(self.healing * healing_multiplicator)
            p1.hp += heal
            if p1.hp > p1.maxhp:        #anti overheal
                p1.hp = p1.maxhp
            print("You used a " + self.name + ". You restored " + str(heal) + " health.")
        else:
            print("You are out of that item!")

    def get_name(self): #get the name with the right \t format
        x = 2-(len(self.name) // 8)
        if 7 < (len(self.name)) < 12:       #item names between 8 and 12 letters arent formatted right without this line
            x += 1
        y = self.name + x*"\t"
        return y


#creating some items
dummy = item("Dummy", 0, 0, 0, "", 0)
potion = item("Potion", 10, 5, 50, "Restores health\t", True)
testitem = item("item with loooooong name", 0, 0, 0, "hard to pronounce")
stone = item("Stone",1, 4, 0, "Looks very throwable" ,)
bottle = item("Empty bottle", 1, 0, 0, "I don't remember drinking this..")
superpotion = item("Super Potion", 35, 1, 100, "Restores even more health")
healingherb = item("Healing Herb", 3, 5, 5, "Used to brew potions" )
attackpotion = item("Attack Potion", 50, 0, 0, "Buffs Attack for 5 rounds", True )
defensepotion = item("Defense Potion", 50, 1, 0, "Buffs defense for 5 rounds", True)
batfang = item("Bat Fang", 10, 0, 0, "A hand full of sharp Bat fangs")
slime_item = item("Slime", 3, 0, 0, "Is this...the corpse?!..",)


#define using item
def use_item(item):
    global flag_fighting
    if item.quantity > 0:   #checking if item quantity is > 0
    
        if item.healing > 0:    #healing if healing item
            item.heal()

        #using Stone
        elif item.name.lower() == "stone":
            if flag_fighting == True:
                item.decrease(1)
                current_enemy.hp -= 10
                print("You threw the Stone and hit an eye. The " + current_enemy.name + " lost 10 HP. Maybe you should use your weapons.") #if fighting
            else:
                print("You hold the stone very tight. It almost cut your finger.")    #if not fighting
        
        elif item.potion == True: #using potion
            if flag_fighting == True: #if fighting
                use_potion(item)    
            else:
                print(f"The {item.name} looks bomb but let's wait for the thirst of war.") #if not fighting

        else:       #default flavour text if item has no healing or certain use
            print("You throw the " + item.name + " very hard on the ground. It shatters into a million pieces. You don't know what you expected. You collect the pieces and glue them together.")
    else:       #quantity is 0
        print("I have none of that.")
    junk = input(" ↩ ")

def use_potion(ptn):
    match ptn.name.lower():
        case "attack potion":
            attackpotion.decrease(1)
            attackup.buff(6)
            print("You gobbled the Attack Potion and raised your attack for 5 rounds!")
        case "defense potion":
            defensepotion.decrease(1)
            defenseup.buff(6)
            print("You devoured the Defense Potion and hardened your skin for 5 rounds!")
