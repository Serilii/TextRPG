if __name__ == "__main__":
    #debugger silencer
    from core.visuals import *
    from classes.Tile import *
    from classes.Quest import *

def talk():     # talking function
    if current_tile().npc != None:
        print("You engage in a conversation with " + current_tile().npc.name + " : ")
        sleep(1)
        match current_tile().npc.name.lower():
            case "nancy":
                talk_nancy()
            case "grandma":
                talk_grandma()
            case "the smith":
                talk_smith()
            case "the witch":
                talk_witch()
    else:
        print("You have a nice time talking to yourself. Loneliness + 100")
    sleep(1)


def talk_nancy():
    if nancy.talked == False:
        speak("'Hello traveler, nice meeting you! You seem to fight a lot ! Always stay healthy!'")
        superpotion.increase(1)
        print("Nancy gave you a super potion!")
        speak("You should talk to people at least twice. Some guys have to tell a lot.")
        speak("'Feel free to rest with me " + p1.name + ". I could use some company!'")
        sleep(1)
        nancy.talked = True
    else:
        speak("'There you are again! Please take care of yourself. But not on my money, I need my potions.'")
        speak("'Feel free to rest if you feel low on health.")
        rest()

def talk_grandma():
    if grandma.talked == False:
        speak("'Hello sweety. Welcome to my shop. I recommend the cookies. But I also sell potions.'")
        speak("'I have some expired ones I can't sell anymore but they still do fine. You can have these if you want to.'")
        potion.increase(3)
        speak("You received 3 Potions")
        speak("'Stay safe out there. Or stay as long as you want sweetheart. Oh... where did I put the herbs?...'")
        grandma.talked = True
    else:
        speak("'Nice to see you again darling. Are you doing well? Sit down and relax a bit.'")
        if grandma_quest.done == False:
                grandma_quest_function()

        

def talk_smith():
    speak("'Talk to me if you want to buy a weapon. I'm busy here.'")
    if  smithy_quest.done == False:
        if smithy_quest.ongoing == False:
            speak("'... But you could also help me...There is a Baby Dragon in my backyard. It keeps setting my wood piles up on fire, this pest. Could you get rid of it?.. '")
            speak("But please care, even a baby dragon is kinda hard to fight! Better have potions..")
            smithy_quest.take()
        elif questflag_smith_dragon == True:
            speak("'The Drag-? OH! Thank you, I finally got rid of this thing. Take this as a reward'")
            whetstone.obtained = True
            print("You receive a Whetstone.")
            global crit_bonus
            crit_bonus += 5
            smithy_quest.finish()
            sleep(1)
            speak("'......Ok that's it. Stop staring at me. Bye'")
        else:
            speak("'Have you killed this thing already?'")

def talk_witch():
    global questflag_witch_herbs
    if witch.talked == False:
        speak("'Hello my tast- handsome child. I sell REAL potions here! And also ingredients..'")
        speak("'I'm also looking for a student. It might get patched in one day. <|:^) '")
        speak("'Well it's your lucky day! You may bugfix it!'")
        cauldron.obtained = True
        speak("You obtained the cauldron!!!!!!")
        sleep(2)
        speak("'You may throw up to 3 things in it! Just fill it up with Healing Herbs.... Or... A Potion and Healing Herbs?... I can't remember... I KNOW IT'S MY JOB!' ")
        witch.talked = True
    else:
        speak("'There you are again sweet, SWEET young child. You look starved! I hope you are eating a LOT.'")
    if grandma_quest.ongoing == True and questflag_witch_herbs == False:
        speak("'Hm? Healing Herbs? It's 5 Gold per He-... For my cousin? AGAIN?! She should take her business more serious. She keeps on running out of stock all the time..Take these'")
        speak("You received 5 healing herbs. SAVE THEM FOR GRANDMA!")
        healingherb.increase(5)
        questflag_witch_herbs = True
    
