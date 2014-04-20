import configparser
import sys

ID = sys.argv[1]
cardtype = sys.argv[2]
question = sys.argv[3]
answer = sys.argv[4]
specific = sys.argv[5:]

carddb = configparser.ConfigParser()

carddb.read_file(open('cards.db'))
if ID not in carddb:
    carddb[ID] = {'type' : cardtype, 'question' : question, 'answer' : answer}
    print('Added new card:', ID)
    with open('cards.db', 'w') as configfile:
        carddb.write(configfile)
else:
    print('CardID already in use')
