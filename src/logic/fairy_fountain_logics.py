if __name__ == "__main__":
    #debugger silencer
    from core.visuals import *

#first fairy fountain
def open_fairy_fountain_1():
    if pendant1.obtained == False:
        speak("You see a fountain in the middle of a forest. You wonder why it sparkles glitter. While inspecting it further a fairy pops out of it.")
        speak("'Hello traveler. You seem like you fight a lot of the monsters around.' ")
        speak("'I love to heal people but there are so many monsters hurting them. Thanks for reducing their numbers.' ")
        speak("'Take this pendant. It will boost health and healing.'")
        print("You obtained a " + pendant1.name + ". Your maximum health raised." )
        sleep(1)
        p1.maxhp += 25
        p1.hp = p1. maxhp
        global healing_multiplicator
        healing_multiplicator += 0.2
        pendant1.obtained = True
        speak("'Maybe you will find my sister. I haven't talked to her in 1630 years but she could probably help you too.'")
    else:
        speak("'Hello Traveler. You defeated " + str(defeated_enemies) + " monsters! Let me heal you.'")
        p1.hp = p1.maxhp
        print("Your feel your health filling up!")    

#second fairy fountain
def open_fairy_fountain_2():
    if pendant2.obtained == False:
        speak("You are surrounded by the ruins of an old city. The fountain in the middle glows. While inspecting it a fairy pops out of it.")
        speak("'Hello traveler. I heard you cleared a lot of monsters near these ruins. ")
        speak("'I love to heal people but there are so many monsters hurting them. Thanks for Getting rid of 'em.' ")
        speak("'Take this pendant. It will boost health and healing.'")
        speak("You obtained a " + pendant2.name + ". Your maximum health raised." )
        sleep(1)
        p1.maxhp += 25
        p1.hp = p1. maxhp
        global healing_multiplicator
        healing_multiplicator += 0.2
        pendant2.obtained = True
        speak("'Have you heard of my sister? I haven't seen her in 1630 years.. She is so nice i bet she will help you. See ya.'")
    else:
        speak("'Hello Traveler. You defeated " + str(defeated_enemies) + " monsters! Let me heal you. Visit me here and then.'")
        p1.hp = p1.maxhp
        print("Your feel your health filling up!")
        speak("See ya!")    
    junk = input(">>leave")
