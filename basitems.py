if __name__ == "__name__":
    from starting_variables import *
    from main import *



####################################### class for base items ####################################
class baseitem:
    def __init__(self, name, function):
        self.name = name
        self.function = function
        self.obtained = False

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
#put your base items into here!!!! :
baseitems = [artifact, pendant1, pendant2, whetstone, cauldron]

