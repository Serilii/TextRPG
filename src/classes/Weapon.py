weapons = []

class weapon:
    def __init__(self, name, damage, crit, price, text)  :
        self.name = name
        self.damage = damage
        self.crit = crit
        self.price = price
        self.number = 0
        self.text = text
        self.bagged = False
        weapons.append(self)
        

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
