import time as t

class Card():
    def __init__(self,question,ans):
        self.fails = 0
        self.leech = 0
        self.times_crammed = 0
        self.reps = 0
        self.question = question
        self.ans = ans
        self.scheduled = t.time()
        self.interval = 0
        self.max_interval = 915
#        self.last_interval = 0
        self.ease = 2.5
        self.same_day = 1 #if true, intervals are in minutes
    def set_interval(self,rating):
        self.set_ease(rating)
        if rating == 0: #^set ease nevertheless, you failed w 2.5, after all
            self.interval = 0
            self.fails += 1
        else:
            try:
#                self.last_interval = self.interval
                self.interval = \
                [10,30,60,240,480,1,4][[0,1,2,3,4,5,6].index(self.reps)]
                #if reps < 7, defaults
            except:
#                self.last_interval = self.interval
                if not self.ease < 0:
                    if not rating == 1 : #don't expand schedule on bad answer
#                        self.interval = self.last_interval * self.ease
                        self.interval *= self.ease
                        if self.interval < 1: self.interval = 1
                else:
                    self.interval = 1; self.ease = 2
            finally:
                self.reps += 1
                if self.reps > 5: self.same_day = 0
                if self.fails > 6:
                    self.leech = 1
        if self.max_interval and self.interval > self.max_interval:
            self.interval = self.max_interval
        self.schedule_fun()
    def set_ease(self,rating):
        self.ease += (0.1 - (5 - rating) * (0.08 \
                          + (5 - rating) * 0.02))  #courtesy of supermemo
        if self.ease > 2.5 : self.ease = 2.5
        if self.ease < 1.5 : self.leech = 1
    def schedule_fun(self):
        if not self.same_day:
            multiplier = 86400 #seconds in a day
        else:
            multiplier = 60 #seconds in a min
        self.scheduled += self.interval * multiplier

#class FlashCard(Card):

#carddict = {'FlashCard': FlashCard}
int_list = open('samplelist.intervals')
cardlist = open('samplelist')
cardlist = cardlist.read()
cardlist = cardlist.split('*')

for x in range(len(cardlist)):
    cardlist[x] = cardlist[x].rstrip().split('\n')

cardlist.pop(0) #remove empty string


#for card in cardslist:
#    if t.time() > card.schedule:
#        cardtypes[card.cardtype].append(card)

#for types in cardtypes:
#    types.scheduled = len(cardtypes)
#    if types:
#       push all to corresponding module
        
