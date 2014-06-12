from subprocess import check_output, call
import uuid
import os

markers = ["[IMG]"]

Q = str(check_output(["zenity","--entry","--text=Question"]).lstrip().rstrip()).strip("b'")
A = str(check_output(["zenity","--entry","--text=Answer"]).lstrip().rstrip()).strip("b'")
ID = str(uuid.uuid4())

import add_card

if Q in markers and A not in markers:
    if Q == '[IMG]':
        call(["scrot", "-s", "/var/tenjin/img/{}.Q.png".format(ID)])
        qtype = 'Img'
    if A == '[IMG]':
        call(["scrot", "-s", "/var/tenjin/img/{}.A.png".format(ID)])
        atype = 'Img'

add_card.addcard(ID,"FlashCard",Q,A)
