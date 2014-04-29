cardlist = [] #let's just assume it is a 1 list for a while

def str_to_list(list_):
    list_ = list_.replace('\n', '')
    list_ = list(eval(list_))
    for x in range(len(list_)):
        try:
            list_[x] = str_to_list(list_[x])
        except:
            pass
    return(list_)

#is one drill a session more realistic, or shall it be split?

def start():

    for card in cardlist:
        card.keytext = str_to_list( card.keytext)
        card.keys = str_to_list(card.keys)
        card.qa = list(zip(card.keytext,card.keys))

    iter_cardlist = iter(cardlist)

    Card = next(iter_cardlist)

    revealed = 0 #to prevent reveal spamming

    import tkinter as tk
    import random
    import threading
    import time

    has_time = 60

    def timer():
        nonlocal has_time
        nonlocal Timer
        while has_time:
            time.sleep(1)
            has_time -= 1
            Timer['text'] = has_time
        else:
            rev_ans()

    timetrack = threading.Thread()
    timetrack.run = timer

    choice = random.choice(range(len(card.qa)))
#    choice = random.choice(Card.qa)
    question = card.qa[choice][0]
#    question = choice[0]
#    answer = choice[1]
    answer = card.qa[choice][1]
  
    def set_key(x):
        nonlocal Root
        def p_d(a): #don't you dare leave this one in
            print(a)
            nonlocal x
            a(x + 1)
        if x + 1 == len(answer):
            Root.bind(answer[x], lambda dummy : do_next(x))
            print('I am trying!')
        elif x + 2 == len(answer):
            Root.bind(answer[x+1], lambda dummy: p_d(do_next))
            print(x+1,answer[x+1],'last')
            Root.bind(answer[x], lambda dummy : print('I do nothing'))
        else:
            Root.bind(answer[x+1], lambda dummy: p_d(set_key))
            print(x+1,answer[x+1])
            Root.bind(answer[x], lambda dummy : print('I do nothing'))
    
    def do_next(x):
        nonlocal question
        nonlocal answer
        nonlocal choice
        print('I am doing the next!')
        Root.bind(answer[x], lambda dummy: print('Terminating myself'))
#        choice = random.choice(card.qa)
        choice = random.choice(list(set(range(len(card.qa)))-{choice}))
        question = card.qa[choice][0]
#        question = choice[0]
        QLab['text'] = question
        answer = card.qa[choice][1]
#        answer = choice[1]
        set_key(0)
#        Root.bind(answer[0],lambda dummy: set_key(0))

    def rev_ans():
        nonlocal revealed
        if revealed == 0:
            revealed = 1
            nonlocal AnsFrame
            AnsFrame = tk.Frame(Root)
            AnsFrame.pack()
            AnsLab = tk.Label(AnsFrame, text = answer)
            AnsLab['font'] = ('times', 15, 'bold')
            AnsLab['height'] = 3
            AnsLab.pack() 


#            def fun(i):
#                rate(i)
#            for i in range(0,6):
#                _ = tk.Frame(AnsFrame)
#                _.pack(side=tk.LEFT)
#                tk.Label(_, text = '5')\
#                  .pack(side=tk.TOP)
#                tk.Button(_, text = str(i),\
#                          command = lambda i=i: fun(i))\
#                  .pack(side=tk.TOP)


    def rate(x):
        nonlocal revealed
        if revealed == 1:
#            print(Card, 'scored', x)
#            Card.set_interval(x)
            revealed = 0
            AnsFrame.destroy()
            if x in [0,1,2]:
                cardlist.append(Card)
            try:
#                nonlocal Card
                Card = next(iter_cardlist)
                QLab['text'] = question
            except StopIteration:
                Revealer.destroy()
                QLab['text'] = 'You\'re done'
                Root.bind('<KP_Enter>', lambda dummy: Root.destroy())
                Root.bind('<Return>', lambda dummy: Root.destroy())
                Root.bind('<space>',lambda dummy: Root.destroy())

    Root = tk.Tk()
#    Timer = tk.Label(Root, text = 'has_time')
#    Timer.pack
    Timer = tk.Label(Root, text = has_time)
    Timer.pack()
    timetrack.start()
    QLab = tk.Label(Root, text = question)
    QLab.pack()
    QLab['font'] = ('times', 20, 'bold')
    Revealer = tk.Button(Root, text = "Reveal", command = rev_ans)
    Revealer.pack()
    AnsFrame = tk.Frame(Root)

    for x in range(0,6):
        Root.bind('<KP_'+str(x)+'>', lambda dummy, x=x: rate(x))
        Root.bind(str(x), lambda dummy, x=x: rate(x))
    Root.bind('<KP_Enter>', lambda dummy: do_next(0))
    Root.bind('<Return>', lambda dummy: do_next(0))
    Root.bind('<space>', lambda dummy: do_next(0))
    for key in Card.keys:
        Root.bind(key, lambda dummy: fail())
    set_key(0)
    Root.mainloop()
