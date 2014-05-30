cardlist = []

def start():
    import tkinter as tk
    import random
    

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

    def rate(score):
        nonlocal revealed
        if revealed == 1:
            print(Card, 'scored', x)
            Card.set_interval(score)
            revealed = 0
            AnsFrame.destroy()

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
