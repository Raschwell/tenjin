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

def rev_ans():
    global revealed
    if revealed == 0:
        revealed = 1
        global AnsFrame
        AnsFrame = Frame(Root)
        AnsFrame.pack()
        AnsLab = Label(AnsFrame, text = answer)
        AnsLab['font'] = ('times', 15, 'bold')
        AnsLab['height'] = 3
        AnsLab.pack()
        def fun(i):
            rate(QLab['text'], i)
        for i in range(1,6):
            _ = Frame(AnsFrame)
            _.pack(side=LEFT)
            Label(_, text = '5')\
                .pack(side=TOP)
            Button(_, text = str(i),\
                   command = lambda i=i: fun(i))\
            .pack(side=TOP)
#            _['relief'] = FLAT


def rate(q,x):
    global revealed
    if revealed == 1:
        print(q, 'scored', x)
        revealed = 0
        AnsFrame.destroy()
        if x == 1:
            questions.append(q)
            answers.append(questions.index(q))
        global question
        global answer
        try:
            QLab['text'] = next(iter_q)
            answer = next(iter_a)
        except StopIteration:
            Revealer.destroy()
            QLab['text'] = 'You\'re done'
            Root.bind('<KP_Enter>', lambda dummy: Root.quit())
            
        

Root = Tk()
QLab = Label(Root, text = question)
QLab.pack()
QLab['font'] = ('times', 20, 'bold')
Revealer = Button(Root, text = "Reveal", command = rev_ans)
Revealer.pack()

for x in range(1,6):
    Root.bind('<KP_'+str(x)+'>', lambda dummy, x=x: rate(QLab['text'], x))

Root.bind('<KP_Enter>', lambda dummy: rev_ans())
Root.mainloop()
