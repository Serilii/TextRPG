if __name__ == "__main__":
    #debugger silencer
    from core.variables import *
    from classes.Player import player
    from time import *
    p1 = player("", 0,0,0,1,1,0,0)


def pattack_animation(damage = "some"):
    array = [" ( /ಠ益ಠ)ノ "," (\\ ಠ益ಠ)  "," ( /ಠ益ಠ)/  "," ( ᴖಠ益ಠ)ᴖ  "," ( ᴖಠ益ಠ)ᴖ ⇲"," ( ᴖಠ益ಠ)ᴖ *"," ( ᴖಠ益ಠ)ᴖ ⌑"," ( ᴖಠ益ಠ)ᴖ  "] 
    for i in array:
        print(i, end = "\r",flush = True)
        if i == " ( /ಠ益ಠ)ノ " or i == " (\\ ಠ益ಠ)  ":
            sleep(0.22)
        else:
            sleep(0.045)
    sleep(0.3)
    x = int((damage /p1.maxhp)*10)
    s = " " + x*"♥" 
    if x == 0:
        s = " ♡"
    print(" ( ᴖಠ益ಠ)ᴖ  \t dealt " + str(damage) + s + " damage!" , end ="\r", flush = True)
    sleep(0.5)
    print("")

def eattacK_animation(damage = ""):
    array = [" ( ๐ Д ๐ )  ", " (┳ Д ┳  )¤¤", " (┳ Д ┳  )° ", " (┳ Д ┳  )³ ", " (┳ Д ┳  )  ", " ( ┳ Д ┳ )  ", " (  ┳ Д ┳)  "]
    for i in array:
        print (i, end = "\r", flush = True)
        if i == " ( ๐ Д ๐ )  " or i == " (┳ Д ┳  )  ":
            sleep(0.45)
        elif i == " ( ┳ Д ┳ )":
            sleep(0.07)
        else:
            sleep(0.05)
    sleep(0.3)
    x = int((damage /p1.maxhp)*10)
    s = " " + x*"♥"
    if x == 0:
        s = " ♡"
    print(" (  ┳ Д ┳) \t took " + str(damage) + s +" damage!" , end ="\r", flush = True)
    sleep(0.5)
    print("")

def move_north_animation():
    a = [" ┌(      )┘ \tYou moved north."," └(      )┐ \tYou moved north."]
    for _ in range(3):
        for i in a:
            print(i, end = "\r")
            sleep(0.27)
    print("")

def move_south_animation():
    a = ["  (.‿  . )\ \tYou moved south."," /( . ‿ .)  \tYou moved south."]
    for _ in range(3):
        for i in a:
            print(i, end = "\r")
            sleep(0.27)
    print("")

def move_east_animation():
    a=[" (  _ ^0) \tYou moved east."," ( _ ^0^) \tYou moved east."," (  _ ^0) \tYou moved east."," (   _ ^) \tYou moved east."," (    _ ) \tYou moved east.",]
    for _ in range(3):
        for i in a:
            if i == " ( _ ^0^) \tYou moved east." or i == "  (    _ ) \tYou moved east.":
                print(i, end = "\r")
                sleep(0.25)
            else:
                print(i, end = "\r")
                sleep(0.1)
    print("")

def move_west_animation():
    a=[" (w^ _  ) \tYou moved east."," (^w^ _ ) \tYou moved east."," (w^ _  ) \tYou moved east."," (^ _   ) \tYou moved east."," ( _    ) \tYou moved east.",]
    for _ in range(3):
        for i in a:
            if i == " (^w^ _ ) \tYou moved east." or i == " ( _    ) \tYou moved east.":
                print(i, end = "\r")
                sleep(0.25)
            else:
                print(i, end = "\r")
                sleep(0.1)
    print("")


def crit_animation(damage = ""):
    x = 70      #lenght of cut
    figure = "( ◡_◡́)--▬▬ι═══════ﺤ"
    figure_open_eye = "( •_•̀)--▬▬ι═══════ﺤ"
    for _ in range(2):
        for i in range(10):
            print(int((x/2))*" " + i*"/", end = "\r")
            sleep(0.004)
    print((x+10)*" ", end= "\r")        
    sleep(0.5)
    print(x*"-", end= "")
    print(figure, end = "\r")
    sleep(0.23)
    for i in range(x+1):
        print(i * " " + (x-i)*"-" + figure, end = "\r", flush = True)
        sleep(0.001)
    sleep(0.35)
    print(x*" " + figure_open_eye, end ="\r", flush = True)
    sleep(0.6)
    print(40*" " + "CRIT ! " + str(damage) + " damage!" , end ="\r", flush = True)
    sleep(0.5)
    print("")