if __name__ == "__main__":
    #debugger silencer
    from src.main import *
    from core.variables import *
    from src.logic.shop_logics import *
    from src.logic.fairy_fountain_logics import *

building_list = []

class building:
    def __init__(self, name):
        self.name = name
        building_list.append(self)

    def open(self):
        print("There is a " + self.name + " nearby.")
        action = ""
        while not(action.lower() in yes_array or action.lower() in no_array):
            action = input("Do you want to enter? 'Yes' or 'No'\n")
            if action.lower() in yes_array:
                match self.name.lower() :
                    case "smithy":  open_smithy()
                    case "shop":   open_shop()
                    case "forest fountain": open_fairy_fountain_1()
                    case "ruin fountain":   open_fairy_fountain_2()
                    case "witch hut":   open_witch_hut()

#creating the buildings and tiles
smithy_shop = building("Smithy")
shop1 = building("Shop")
fairy_fountain_1 = building("Forest Fountain")
fairy_fountain_2 = building("Ruin Fountain")
witch_hut = building("Witch Hut")