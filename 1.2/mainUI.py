import tkinter as tk
from tkinter import ttk

class But_print:
     def __init__(self):
          self.but = ttk.Button(root)
          self.but["text"] = "Печать"
          self.but.bind("<Button-1>",self.printer)
          self.but.pack()
     def printer(self,event):
          print ("Как всегда очередной 'Hello World!'")
 
root = tk.Tk()
fra1 = tk.Frame(root,width=500,height=100,bg="darkred")
fra2 = tk.Frame(root,width=300,height=200,bg="green",bd=20)
fra3 = tk.Frame(root,width=500,height=150,bg="darkblue")

sca1 = tk.Scale(fra3, orient = tk.HORIZONTAL, length = 300,
          from_ = 0,to = 3000,tickinterval = 500,resolution = 5)
sca1.pack()


ent1 = tk.Entry(fra2,width=20)
ent1.pack()

obj = But_print()

fra1.pack()
fra2.pack()
fra3.pack()

root.mainloop()