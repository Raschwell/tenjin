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
            if Card.answer == '[IMG]':
                Card.Aphoto = tk.PhotoImage(file="/var/tenjin/img/{}.A.png".format(Card.ID))
                AnsLab = tk.Label(AnsFrame, image = Card.Aphoto)
            else:
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
                if Card.question == '[IMG]':
                    Card.Qphoto = tk.PhotoImage(file="/var/tenjin/img/{}.Q.png".format(Card.ID))
                    QLab['text'] = ""
                    QLab['image'] = Card.Qphoto
                else:
                    QLab['text'] = Card.question
                    QLab['image'] = ""

            except StopIteration:
                Revealer.destroy()
                QLab['image'] = ""
                QLab['text'] = 'You\'re done'
                Root.bind('<KP_Enter>', lambda dummy: Root.destroy())
                Root.bind('<Return>', lambda dummy: Root.destroy())
                Root.bind('<space>',lambda dummy: Root.destroy())

    def edit_mode():

      QLab['text'] = ''
      QEntry = tk.Entry(QFrame)
      QEntry.pack(fill=tk.X)
      QEntry.insert(0, Card.question)
      nonlocal AnsFrame
      AnsFrame.destroy()
      AnsFrame = tk.Frame(Root)
      AnsFrame.pack(fill=tk.X)
      AEntry = tk.Entry(AnsFrame)
      AEntry.pack(fill=tk.X)
      AEntry.insert(0, Card.answer)
      Root.bind('<Return>', lambda dummy: send_edits())
      Root.bind('<space>', lambda dummy: print(''))
      Root.bind('e', lambda dummy: print(''))
      def send_edits():
        Card.question = QEntry.get()
        Card.answer = AEntry.get()
        AnsFrame.destroy()
        QEntry.pack_forget()
        Root.bind('<Return>', lambda dummy: rev_ans())
        Root.bind('e', lambda dummy: edit_mode())
        QLab['text'] = Card.question

    def fdel():
      Card.schedule = 10**12
      Card.same_day = 0
      Card.PIC = 1

    Root = tk.Tk()
    QFrame = tk.Frame()
    QFrame.pack(fill=tk.X)
    QLab = tk.Label(QFrame, text = Card.question)
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
    Root.bind('<Control_L>e', lambda dummy: edit_mode())
    Root.bind('<Control_L>d', lambda dummy: fdel())
    Root.mainloop()
