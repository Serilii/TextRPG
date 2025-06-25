
class quest:
    def __init__(self, name, text):
        self.name = name
        self.ongoing = False
        self.done = False
        self.text = text

    def take(self):
        self.ongoing = True
        print("You took the quest '" + self.name + "'")

    def finish(self):
        self.ongoing = False
        self.done = True
        print("You finished the quest '" + self.name + "'")

    def get_name(self):         #get the name with the right \t format
        x = 3-(len(self.name) // 8)
        y = self.name + x*"\t"
        return y
    
    def get_done(self):
        if self.done == True:
            return " ☑ done "
        elif self.ongoing == True:
            return " ☐ going on"
        else:
            return ""
# creating quests
        
smithy_quest = quest("Smithy's Quest", "Kill the baby Dragon by the smithy so it can't burn the wood." )
grandma_quest = quest("Good Boi", "Bring grandma 5 healing herbs")

quests = [smithy_quest, grandma_quest]

def quest_log():
    print("-------------------------Quest Log-------------------------")
    for q in quests:
        if q.ongoing == True or q.done == True:
            print(q.get_name() + "\t" + q.get_done() + "\t\t" +  q.text )
    print("-----------------------------------------------------------")
