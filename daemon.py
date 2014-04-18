import time as t

class Card():
    def __init__(self,ID,question,answer,interval = 0, reps = 0,scheduled = t.time(), fails = 0, leech = 0, ease = 2.5, same_day = 1):
        self.fails = fails
        self.leech = leech
        self.reps = reps
        self.question = question
        self.answer = answer
        self.scheduled = scheduled
        self.interval = interval
        self.max_interval = 915
        self.ease = ease
        self.same_day = same_day #if true, intervals are in minutes
        self.ID = ID
    def set_interval(self,rating):
        self.set_ease(rating)
        if rating == 0: #^set ease nevertheless, you failed w 2.5, after all
            self.interval = 0
            self.fails += 1
        else:
            try:
                self.interval = \
                [10,30,60,240,480,1,4][[0,1,2,3,4,5,6].index(self.reps)]
                #if reps < 7, defaults
            except:
                if not self.ease < 0:
                    if not rating == 1 : #don't expand schedule on bad answer
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
        self.schedule_func()
    def set_ease(self,rating):
        self.ease += (0.1 - (5 - rating) * (0.08 \
                          + (5 - rating) * 0.02))  #courtesy of supermemo
        if self.ease > 2.5 : self.ease = 2.5
        if self.ease < 1.5 : self.leech = 1
    def schedule_func(self):
        if not self.same_day:
            multiplier = 86400 #seconds in a day
        else:
            multiplier = 60 #seconds in a min
        self.scheduled += self.interval * multiplier

class FlashCard(Card):
    def start_rep(self):
        if not flashcard:
            import flashcard
            flashcard.cardlist = cardlist['FlashCard']
            flashcard.start()
        
import configparser
carddb = configparser.ConfigParser()
cardz = open('cards.db', 'r+')
carddb.read_file(cardz)

def commit_changes():
    config.write(carddb)

def check_schedules():
    fcarddict = {}

    def flashcard_handler(card):
        nonlocal fcarddict
        if card not in fcarddict:
            question = carddb[card]['question']
            answer = carddb[card]['answer']
            interval = float(carddb[card]['interval'])
            reps = int(carddb[card]['reps'])
            schedule = int(carddb[card]['schedule'])
            fails = int(carddb[card]['fails'])
            leech = int(carddb[card]['leech'])
            ease = float(carddb[card]['ease'])
            same_day = int(carddb[card]['same_day'])
            ID = card
            fcarddict.update({card: FlashCard(ID,question,answer,interval,\
                                              reps,schedule,fails,\
                                              leech,ease,same_day)})
            print(fcarddict.keys(),fcarddict.values())

    cardhandler = {'FlashCard' : flashcard_handler}

    for x in carddb.sections():
        if float(carddb[x]['interval']) < t.time():
            cardhandler[carddb[x]['type']](x)

    return({'fcards': fcarddict}) #add other types later

do_us = check_schedules()

import flashcard

for x in do_us['fcards'].values():
    flashcard.cardlist.append(x)

flashcard.start()

for x in do_us['fcards'].values():
    print(x.interval)
