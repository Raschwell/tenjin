cardlist = []

def start():
    iter_cardlist = iter(cardlist)

    Card = next(iter_cardlist)

    revealed = 0 #to prevent reveal spamming  

    import tkinter as tk

    def verify():
        nonlocal Card
        nonlocal revealed
        if revealed == 0:
            print(EntryField.get())
            if EntryField.get() == Card.answer:
                tk.Label(AnsFrame, text='Correct').pack()
                ask_to_reveal()
            else:
                tk.Label(AnsFrame, text='Nope. Press <Control_L><r> to reveal',\
                font = ('times', 12, 'bold')).pack()

    def ask_to_reveal():
        nonlocal AnsFrame
        AnsFrame.destroy()
        AnsFrame = tk.Frame(Root)
        AnsFrame.pack()
        nonlocal Card
        tk.Label(AnsFrame, text=Card.answer, font = ('times', 12, 'bold')).pack()
        EntryField.delete(0,len(EntryField.get()))
        EntryField['state'] = tk.DISABLED
        nonlocal revealed
        revealed = 1
        def fun(i):
            rate(i)
        for i in range(0,6):
            _1 = tk.Frame(AnsFrame)
            _1.pack(side=tk.LEFT)
            tk.Label(_1, text = '5')\
              .pack(side=tk.TOP)
            tk.Button(_1, text = str(i),\
                      command = lambda i=i: fun(i))\
              .pack(side=tk.TOP)

    def rate(x):
        nonlocal revealed
        nonlocal AnsFrame
        if revealed == 1:
            print(Card, 'scored', x)
            Card.set_interval(x)
            revealed = 0
            AnsFrame.destroy()
            AnsFrame = tk.Frame(Root)
            AnsFrame.pack()
            EntryField['state'] = tk.NORMAL
            if x in [0,1,2]:
                cardlist.append(Card)
            try:
                nonlocal Card
                Card = next(iter_cardlist)
                QLab['text'] = Card.question
            except StopIteration:
                EntryField.destroy()
                QLab['text'] = 'You\'re done'
                Root.bind('<KP_Enter>', lambda dummy: Root.destroy())
                Root.bind('<Return>', lambda dummy: Root.destroy())
                Root.bind('<space>', lambda dummy: Root.destroy())

    Root = tk.Tk()
    QLab = tk.Label(Root, text = Card.question)
    QLab.pack()
    QLab['font'] = ('times', 20, 'bold')
    EntryField = tk.Entry(Root)
    EntryField.pack()
    EntryField.focus()

    for x in range(0,6):
        Root.bind('<KP_'+str(x)+'>', lambda dummy, x=x: rate(x))
        Root.bind(str(x), lambda dummy, x = x: rate(x))
    Root.bind('<KP_Enter>', lambda dummy: verify())
    Root.bind('<Return>', lambda dummy: verify())
    Root.bind('<Control_L><r>', lambda dummy: ask_to_reveal())

    AnsFrame = tk.Frame(Root)
    AnsFrame.pack()

    Root.mainloop()
