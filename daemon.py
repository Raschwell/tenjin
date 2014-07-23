import time as t
import random

max_interval = 915

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
        self.ease = ease
        self.same_day = same_day #if true, intervals are in minutes
        self.ID = ID
    def set_interval(self,rating):
        if self.PIC:
            self.set_ease(rating)
            if rating in [0,1]: #set ease nevertheless
                self.interval = 1            #you failed w 2.5, after all
                self.reps += 1
        if not (rating in [0,1,2] and not self.PIC):
            try:
                self.interval = [60,240,1,4][self.reps]
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
                if self.reps > 2: self.same_day = 0
        if self.interval > max_interval:
            self.interval = max_interval
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
        self.scheduled = t.time() + self.interval * multiplier

class FlashCard(Card):
    def do_cards():
        try:
            for x in FlashCard.carddict.values():#these should'nt be dicts anymore
                flashcard.cardlist.append(x)

            if flashcard.cardlist:
                call(["notify-send", "You've got flashcards to attend to!"])
                dummy = s.accept() #wait for input
                global carddb
                carddb = configparser.ConfigParser()
                carddb.read_file(open(location))


            flashcard.start()

            for card in FlashCard.carddict.values():
                make_changes(card)

            commit_changes()
            flashcard.cardlist = []
        except StopIteration:
            pass

    def handler(card):
        if card not in FlashCard.carddict:
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
            FlashCard.carddict.update({card: FlashCard(ID,question,answer,interval,\
                                              reps,schedule,fails,\
                                              leech,ease,same_day,PIC)})


class EntryCard(Card):
    def do_cards():
        try:
            for x in EntryCard.carddict.values():
                entrycard.cardlist.append(x)

            if entrycard.cardlist:
                call(["notify-send", "You've got entrycards to attend to!"])
                dummy = s.accept() #wait for input

            entrycard.start()

            for card in EntryCard.carddict.values():
                make_changes(card)

            commit_changes()
            entrycard.cardlist = []
        except StopIteration:
            pass

    def handler(card):
        if card not in EntryCard.carddict:
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
            EntryCard.carddict.update({card: EntryCard(ID,question,answer,interval,\
                                              reps,schedule,fails,\
                                              leech,ease,same_day,PIC)})

class KeyDrill(Card):
    def do_cards():
        try:
            for x in KeyDrill.carddict.values():
                keydrill.cardlist.append(x)

            if keydrill.cardlist:
                call(["notify-send", "You've got keydrills to attend to!"])
                dummy = s.accept() #wait for input

            keydrill.start()

            for card in KeyDrill.carddict.values():
                make_changes(card)

            commit_changes()
            keydrill.cardlist = []
        except StopIteration:
            pass

    def handler(card):
        if card not in KeyDrill.carddict:
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
            KeyDrill.carddict.update({card: KeyDrill(ID,question,answer,interval,\
                                              reps,schedule,fails,\
                                              leech,ease,same_day,PIC)})




def commit_changes():
    with open(location, 'w') as configfile:
        carddb.write(configfile)

def check_schedules():

    EntryCard.carddict = {}
    FlashCard.carddict = {}
    KeyDrill.carddict = {}


    for x in carddb.sections():
        if float(carddb[x]['schedule']) < t.time():
            eval(carddb[x]['type']).handler(x)

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
    carddb[card.ID]['question'] = str(card.question)
    carddb[card.ID]['answer'] = str(card.answer)

from subprocess import call

do_cardtype = [FlashCard.do_cards, EntryCard.do_cards, KeyDrill.do_cards]

import configparser
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
    t.sleep(1)

