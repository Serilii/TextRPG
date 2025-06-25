
class buffs:
    def __init__(self, name : str ,  raising):
        self.name = name
        self.multiplicator = raising
        self.counter = 0

    def buff(self, rounds):
        self.counter += rounds

    def decrement(self, rounds = 1):    #reduce remaining rounds by 'rounds' (default 1)
            self.counter -= rounds
            if self.counter < 0:        #no negative rounds allowed!
                self.counter = 0


attackup = buffs( "Attack Up" , 0.5 )       # checked in pattack()
defenseup = buffs("Defense Up", 0.5)        # checked in eattack() , halves taken dmg for now since there is no defense value lmao

buff_array = [attackup, defenseup]

def buffs_decrement_all(rounds = 1):
    for bfs in buff_array:
        bfs.decrement(rounds)
