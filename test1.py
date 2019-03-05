from Tkinter import *
import time


def onGo():
    for i in range(50):
        t.insert(END, 'a_' + str(i))
        time.sleep(0.1)
        t.update()


root = Tk()
t = Text(root)
t.pack()
goBtn = Button(text="Go!", command=onGo)
goBtn.pack()
root.mainloop()