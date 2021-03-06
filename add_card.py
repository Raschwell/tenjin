#!/usr/bin/local/python3

import configparser
import sys

#ID = sys.argv[1]
#cardtype = sys.argv[2]
#question = sys.argv[3]
#answer = sys.argv[4]
#specific = sys.argv[5:]

def addcard(ID,cardtype,question,answer):
    config = configparser.ConfigParser()
    config.read_file(open('/usr/home/dennis/.config/tenjin/config'))
    location = config['Main']['location']

    carddb = configparser.ConfigParser()

    carddb.read_file(open(location))
    if ID not in carddb:
        carddb[ID] = {'type' : cardtype, 'question' : question, 'answer' : answer}
        print('Added new card:', ID)
        with open(location, 'w') as configfile:
            carddb.write(configfile)
    else:
        print('CardID already in use')

