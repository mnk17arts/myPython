# simple calculator
# code by @mnk17arts

from tkinter import *
import time
def click(event):
    global scvalue
    #event.widget.cget ()
    text = event.widget.cget("text")
    if text == "=":
        #.isdigit() ....returns boolean
        if scvalue.get().isdigit():
            value = int(scvalue.get())
        else:
            #if error is generated...
            try:
                #eval()....evaluates...
                value = eval(screen.get())

            except Exception as e:
                print(e)
                value = "Error"

        #.set().. sets the value.....
        scvalue.set(value)
        #.update().... updates..
        screen.update()
        if value=="Error":
            time.sleep(0.8)
            scvalue.set("")
            screen.update()
            

    elif text == "ClearScreen":
        scvalue.set("")
        screen.update()
    elif text=="C":
        list=screen.get()
        print(len(list))
        newlist=""
        for i in range (len(list)-1):
            newlist+=list[i]
        scvalue.set(newlist)
        screen.update()

    else:
        scvalue.set(scvalue.get() + text)
        screen.update()

root = Tk()
root.geometry("470x1000")
root.title("Calculator By MNK17ARTS")
root.iconphoto(True,PhotoImage(file="icon3.png"))

scvalue = StringVar()
scvalue.set("")
screen = Entry(root, textvar=scvalue, font="lucida 40 bold",bg="black",fg="green",insertbackground="green",borderwidth=3,relief="groove")
screen.pack(fill=X, ipadx=10, pady=2, padx=2)
Label(root,text="Simple Calculator ®",bg="grey").pack(fill=X)
TEXT=["9","8","7","6","5","4","3","2","1","*","0","+","-","%","/","=",".","C"]
for j in range(6):
    f = Frame(root, bg="grey15")
    for i in range(3):
        b = Button(f, text=TEXT[i+3*j], padx=50,     pady=12, font="lucida 35 bold",bg="black",fg="yellow",borderwidth=15,relief=RAISED)
        b.pack(side=LEFT, padx=1, pady=1)
        b.bind('<Button-1>', click)
    f.pack(fill=X)

f=Frame(root,bg="grey15")

b=Button(f,text="ClearScreen",font="lucida 15 bold",bg="black",fg="yellow",padx=50,pady=50,borderwidth=15,relief=RAISED)
b.pack(side=LEFT,fill=Y)
b.bind('<Button-1>',click)

b=Button(f,text="EXIT",font="lucida 35 bold",bg="black",fg="red",padx=50,pady=50,borderwidth=15,relief=RAISED)
b.pack(fill=X)
b.bind('<Button-1>',exit)

f.pack(fill=X)

root.mainloop()
