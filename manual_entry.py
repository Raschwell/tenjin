#questions = ['Question 1', 'Question 2', 'Question 3']
questions = ['Question ' + str(i) for i in range(3)]
iter_q = iter(questions)
#answers = ['Answer 1', 'Answer 2', 'Answer 3']
answers = ['Answer ' + str(i) for i in range(3)]
iter_a = iter(answers)

question = next(iter_q)
answer = next(iter_a)
revealed = 0 #to prevent reveal spamming

from tkinter import *

def verify():
    global revealed
    global AnsFrame
    if revealed == 0:
        global _
        print(EntryField.get())
        if EntryField.get() == answer:
            Label(AnsFrame, text='Correct').pack()
            ask_to_reveal()
        else:
                Label(AnsFrame, text='Nope. Press <Control_L><r> to reveal',\
                font = ('times', 12, 'bold')).pack()
                



def ask_to_reveal():
    global AnsFrame
    AnsFrame.destroy()
    AnsFrame = Frame(Root)
    AnsFrame.pack()
    Label(AnsFrame, text=answer, font = ('times', 12, 'bold')).pack()
    EntryField.delete(0,len(EntryField.get()))
    EntryField['state'] = DISABLED
    global revealed
    revealed = 1
    def fun(i):
        rate(QLab['text'], i)
    for i in range(1,6):
        _1 = Frame(AnsFrame)
        _1.pack(side=LEFT)
        Label(_1, text = '5')\
            .pack(side=TOP)
        Button(_1, text = str(i),\
               command = lambda i=i: fun(i))\
        .pack(side=TOP)
    

def rate(q,x):
    global revealed
    global AnsFrame
    if revealed == 1:
        print(q, 'scored', x)
        revealed = 0
        AnsFrame.destroy()
        AnsFrame = Frame(Root)
        AnsFrame.pack()
        EntryField['state'] = NORMAL
        if x == 1:
            questions.append(q)
            answers.append(questions.index(q))
        global question
        global answer
        try:
            QLab['text'] = next(iter_q)
            answer = next(iter_a)
        except StopIteration:
            EntryField.destroy()
            QLab['text'] = 'You\'re done'
            Root.bind('<KP_Enter>', lambda dummy: Root.quit())
            Root.bind('<Return>', lambda dummy: Root.quit())
            Root.bind('<space>', lambda dummy: Root.quit())
        

Root = Tk()
QLab = Label(Root, text = question)
QLab.pack()
QLab['font'] = ('times', 20, 'bold')
EntryField = Entry(Root)
EntryField.pack()
EntryField.focus()

for x in range(1,6):
    Root.bind('<KP_'+str(x)+'>', lambda dummy, x=x: rate(QLab['text'], x))
for x in range(1,6):
    Root.bind(str(x), lambda dummy, x = x: rate(QLab['text'], x))
Root.bind('<KP_Enter>', lambda dummy: verify())
Root.bind('<Return>', lambda dummy: verify())

Root.bind('<Control_L><r>', lambda dummy: ask_to_reveal())

AnsFrame = Frame(Root)
AnsFrame.pack()

Root.mainloop()
