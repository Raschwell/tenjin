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

def start():

    for Card in cardlist:
        Card.question = str_to_list(Card.question)
        Card.answer = str_to_list(Card.answer)
        Card.qa = list(zip(Card.question,Card.answer))

    def make_shortcuts():
        nonlocal choice
        nonlocal question
        nonlocal answer
        choice = random.choice(range(len(Card.qa)))
        question = Card.qa[choice][0]
        answer = Card.qa[choice][1]

    iter_cardlist = iter(cardlist)

    Card = next(iter_cardlist)

    revealed = 0 #to prevent reveal spamming

    import tkinter as tk
    import random
    import threading
    import time

    has_time = 2
    def timer():
        nonlocal has_time
        nonlocal Timer
        while has_time:
            time.sleep(1)
            has_time -= 1
            print(has_time)
            Timer['text'] = has_time
        else:
            nonlocal AnsFrame
            AnsFrame = tk.Frame(Root)
            AnsFrame.pack()
            pop_ratings()

    def start_timer():
        has_time = 2
        timetrack = threading.Thread()
        timetrack.run = timer
        Timer['text'] = has_time
        timetrack.start()

    choice = random.choice(range(len(Card.qa)))
    question = Card.qa[choice][0]
    answer = Card.qa[choice][1]
  
    def set_key(x):
#        nonlocal Root
        if x + 1 == len(answer):
            Root.bind(answer[x], lambda dummy : do_next(x))
        elif x + 2 == len(answer):
            Root.bind(answer[x+1], lambda dummy: do_next(x + 1))
            Root.bind(answer[x], lambda dummy : 'pass' )
        else:
            Root.bind(answer[x+1], lambda dummy: set_key(x + 1))
            print(x+1,answer[x+1])
            Root.bind(answer[x], lambda dummy : 'pass' )
    
    def do_next(x):
        nonlocal question
        nonlocal answer
        nonlocal choice
        Root.bind(answer[x], lambda dummy: print('Nothing'))
        choice = random.choice(list(set(range(len(Card.qa)))-{choice}))
        question = Card.qa[choice][0]
        QLab['text'] = question
        answer = Card.qa[choice][1]
        set_key(0)

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

    def pop_ratings():
        def fun(i):
            rate(i)
        for i in range(0,6):
            nonlocal AnsFrame
            _ = tk.Frame(AnsFrame)
            _.pack(side=tk.LEFT)
            tk.Label(_, text = '5')\
              .pack(side=tk.TOP)
            tk.Button(_, text = str(i),\
                      command = lambda i=i: fun(i))\
              .pack(side=tk.TOP)

    def rate(x):
        nonlocal revealed
        Card.set_interval(x)
        revealed = 0
        AnsFrame.destroy()
        if x in [0,1,2]:
            cardlist.append(Card)
        try:
            nonlocal Card
            Card = next(iter_cardlist)
            QLab['text'] = question
        except StopIteration:
            Revealer.destroy()
            QLab['text'] = 'You\'re done'
            Root.bind('<KP_Enter>', lambda dummy: Root.destroy())
            Root.bind('<Return>', lambda dummy: Root.destroy())
            Root.bind('<space>',lambda dummy: Root.destroy())
        start_timer()

        

    Root = tk.Tk()
    Timer = tk.Label(Root)
    Timer.pack()
    start_timer()
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
    for key in Card.answer:
        Root.bind(key, lambda dummy: fail())
    set_key(0)
    Root.mainloop()
