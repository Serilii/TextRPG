if __name__ == "__main__":
    #debugger silencer
    from core.variables import *
    from classes.Item import *

baseItems = []

class baseitem:
    def __init__(self, name, function):
        self.name = name
        self.function = function
        self.obtained = False
        baseItems.append(self)

    def get_name(self): #get the name with the right \t format
        x = 2-(len(self.name) // 8)
        y = self.name + x*"\t"
        return y

pendant1 = baseitem("Fairy Pendant", "A fairy shaped Pendant emitting a slight glow. Raises health and boosts healing.")
pendant2 = baseitem("Heart Pendant", "A heart shaped Pendant emitting a slight glow. Raises health and boosts healing.")
artifact = baseitem("Artifact ", "A weird stone you found in your pocket. It tickles when you touch it.")
artifact.obtained = True
whetstone = baseitem("Whetstone", "A chonky little whetstone for your weapons. The sharpness increases your crit chance.")
cauldron = baseitem("Cauldron", "You can craft stuff in this. Very handy! Very witchy..")
selling_permission = baseitem("Merchant Certificate", "Allows you to sell items. Half the price is all you manage tho..")
