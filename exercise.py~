cardlist = []

def start():
    iter_cardlist = iter(cardlist)

    Card = next(iter_cardlist)

    revealed = 0 #to prevent reveal spamming

    import tkinter as tk

    def rev_ans():
        nonlocal revealed
        if revealed == 0:
            revealed = 1
            nonlocal AnsFrame
            AnsFrame = tk.Frame(Root)
            AnsFrame.pack()
            AnsLab = tk.Label(AnsFrame, text = Card.answer)
            AnsLab['font'] = ('times', 15, 'bold')
            AnsLab['height'] = 3
            AnsLab.pack() 
            def fun(i):
                rate(i)
            for i in range(0,6):
                _ = tk.Frame(AnsFrame)
                _.pack(side=tk.LEFT)
                tk.Label(_, text = '5')\
                  .pack(side=tk.TOP)
                tk.Button(_, text = str(i),\
                          command = lambda i=i: fun(i))\
                  .pack(side=tk.TOP)

    def rate(x):
        nonlocal revealed
        if revealed == 1:
            print(Card, 'scored', x)
            Card.set_interval(x)
            revealed = 0
            AnsFrame.destroy()
            if x in [0,1,2]:
                cardlist.append(Card)
            try:
                nonlocal Card
                Card = next(iter_cardlist)
                QLab['text'] = Card.question
            except StopIteration:
                Revealer.destroy()
                QLab['text'] = 'You\'re done'
                Root.bind('<KP_Enter>', lambda dummy: Root.destroy())
                Root.bind('<Return>', lambda dummy: Root.destroy())
                Root.bind('<space>',lambda dummy: Root.destroy())

    Root = tk.Tk()
    QLab = tk.Label(Root, text = Card.question)
    QLab.pack()
    QLab['font'] = ('times', 20, 'bold')
    Revealer = tk.Button(Root, text = "Reveal", command = rev_ans)
    Revealer.pack()
    AnsFrame = tk.Frame(Root)

    for x in range(0,6):
        Root.bind('<KP_'+str(x)+'>', lambda dummy, x=x: rate(x))
        Root.bind(str(x), lambda dummy, x=x: rate(x))
    Root.bind('<KP_Enter>', lambda dummy: rev_ans())
    Root.bind('<Return>', lambda dummy: rev_ans())
    Root.bind('<space>', lambda dummy: rev_ans())
    Root.mainloop()
