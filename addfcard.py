from subprocess import check_output, call
import uuid
import os

question = str(check_output(["zenity","--entry","--text=Question"]).lstrip().rstrip()).strip("b'")
answer = str(check_output(["zenity","--entry","--text=Answer"]).lstrip().rstrip()).strip("b'")
ID = str(uuid.uuid4())

import add_card

add_card.addcard(ID,"FlashCard",question,answer)
