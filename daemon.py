import time as t
import random

class Card():
    def __init__(self,ID,question = '' ,answer = '' ,interval = 0, reps = 0,scheduled = t.time(), fails = 0, leech = 0, ease = 2.5, same_day = 1, PIC = 0):
        self.PIC = 0 #passed initial 'cram', just so that you recognize it next time
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
        if self.PIC:
            self.set_ease(rating)
        if rating in [0,1] and self.PIC: #set ease nevertheless
            self.interval = 0            #you failed w 2.5, after all
            self.fails += 1
            self.reps += 1
        if rating in [0,1,2] and not self.PIC:
            pass
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
                if not self.PIC : self.PIC = 1
                if self.PIC:
                    self.reps += 1
                if self.reps > 5: self.same_day = 0
                if self.fails > 7:
                    self.leech = 1
        if self.max_interval and self.interval > self.max_interval:
            self.interval = self.max_interval
        self.interval *= random.randrange(900,1100)/1000 #generate some noise]
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
    pass

class EntryCard(Card):
    pass

class KeyDrill(Card):
    pass

def commit_changes():
    with open(location, 'w') as configfile:
        carddb.write(configfile)

def check_schedules():
    fcarddict = {}
    entrycarddict = {}
    keydrilldict = {}

    def flashcard_handler(card):
        nonlocal fcarddict
        if card not in fcarddict:
            question = carddb[card]['question']
            answer = carddb[card]['answer']
            interval = float(carddb[card]['interval'])
            reps = int(carddb[card]['reps'])
            schedule = float(carddb[card]['schedule'])
            if schedule == 0:
                schedule = t.time()
            fails = int(carddb[card]['fails'])
            leech = int(carddb[card]['leech'])
            ease = float(carddb[card]['ease'])
            same_day = int(carddb[card]['same_day'])
            PIC = int(carddb[card]['PIC'])
            ID = card
            fcarddict.update({card: FlashCard(ID,question,answer,interval,\
                                              reps,schedule,fails,\
                                              leech,ease,same_day,PIC)})

    def entrycard_handler(card):
        nonlocal entrycarddict
        if card not in entrycarddict:
            question = carddb[card]['question']
            answer = carddb[card]['answer']
            interval = float(carddb[card]['interval'])
            reps = int(carddb[card]['reps'])
            schedule = float(carddb[card]['schedule'])
            if schedule == 0:
                schedule = t.time()
            fails = int(carddb[card]['fails'])
            leech = int(carddb[card]['leech'])
            ease = float(carddb[card]['ease'])
            same_day = int(carddb[card]['same_day'])
            PIC = int(carddb[card]['PIC'])
            ID = card
            entrycarddict.update({card: EntryCard(ID,question,answer,interval,\
                                              reps,schedule,fails,\
                                              leech,ease,same_day,PIC)})


    def keydrill_handler(card):
        nonlocal keydrilldict
        if card not in keydrilldict:
            question = carddb[card]['question']
            answer = carddb[card]['answer']
            interval = float(carddb[card]['interval'])
            reps = int(carddb[card]['reps'])
            schedule = float(carddb[card]['schedule'])
            if schedule == 0:
                schedule = t.time()
            fails = int(carddb[card]['fails'])
            leech = int(carddb[card]['leech'])
            ease = float(carddb[card]['ease'])
            same_day = int(carddb[card]['same_day'])
            PIC = int(carddb[card]['PIC'])
            ID = card
            keydrilldict.update({card: KeyDrill(ID,question,answer,interval,\
                                              reps,schedule,fails,\
                                              leech,ease,same_day,PIC)})


    cardhandler = {'FlashCard' : flashcard_handler,\
                   'EntryCard' : entrycard_handler,\
                   'KeyDrill' : keydrill_handler}

    for x in carddb.sections():
        if float(carddb[x]['schedule']) < t.time():
            print(float(carddb[x]['schedule']),t.time())
            cardhandler[carddb[x]['type']](x)

    return({'fcards': fcarddict,\
            'entrycards' : entrycarddict,\
            'keydrills' : keydrilldict\
          }) #add other types later

import flashcard
import entrycard
import keydrill

def make_changes(card):
    carddb[card.ID]['interval'] = str(card.interval)
    carddb[card.ID]['reps'] = str(card.reps)
    carddb[card.ID]['schedule'] = str(card.scheduled)
    carddb[card.ID]['fails'] = str(card.fails)
    carddb[card.ID]['leech'] = str(card.leech)
    carddb[card.ID]['ease'] = str(card.ease)
    carddb[card.ID]['same_day'] = str(card.same_day)
    carddb[card.ID]['PIC'] = str(card.PIC)

from subprocess import call

def do_fcards():
    try:
        for x in do_us['fcards'].values():
            flashcard.cardlist.append(x)

        if flashcard.cardlist:
            call(["notify-send", "You've got flashcards to attend to!"])
            dummy = s.accept() #wait for input

        flashcard.start()

        for card in do_us['fcards'].values():
            make_changes(card)

        commit_changes()
        flashcard.cardlist = []
    except StopIteration:
        pass

def do_entrycards():
    try:
        for x in do_us['entrycards'].values():
            entrycard.cardlist.append(x)

        if entrycard.cardlist:
            call(["notify-send", "You've got entrycards to attend to!"])
            dummy = s.accept() #wait for input

        entrycard.start()

        for card in do_us['entrycards'].values():
            make_changes(card)

        commit_changes()
        entrycard.cardlist = []
    except StopIteration:
        pass

def do_keydrills():
    try:
        for x in do_us['keydrills'].values():
            keydrill.cardlist.append(x)

        if keydrill.cardlist:
            call(["notify-send", "You've got keydrills to attend to!"])
            dummy = s.accept() #wait for input

        keydrill.start()

        for card in do_us['keydrills'].values():
            make_changes(card)

        commit_changes()
        keydrill.cardlist = []
    except StopIteration:
        pass


do_cardtype = [do_fcards, do_entrycards, do_keydrills]

"""import configparser
import os
config = configparser.ConfigParser()
config.read_file(open(os.getenv('HOME')+'/.config/tenjin/config'))
location = config['Main']['location']
carddb = configparser.ConfigParser()
carddb.read_file(open(location))

import socket
HOST = 'localhost'
PORT = 61375
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

while 1:
    carddb.read_file(open(location))
    do_us = check_schedules()
    for func in do_cardtype:
        func()
    t.sleep(300)
"""

def str_to_list(list_):
#     list_ = list_.replace('\n', '')
    list_ = list(eval(list_))
    for x in range(len(list_)):
        try:
            list_[x] = str_to_list(list_[x])
        except:
            pass
    return(list_)
