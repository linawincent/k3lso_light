from tkinter import Frame, Tk, Label, Button
from tkinter.ttk import Scale, Label

class GUI:
    def __init__(self, master):
        self.master = master
        master.title("code leaks")

        self.label = Label(master, text="let the game begin!")
        self.label.pack()

        self.greet_button = Button(master, text="Welcome", command=self.greet)
        self.greet_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

    def greet(self):
        print("welcome !")

class Application(Frame):              
    def __init__(self, master=None):
        Frame.__init__(self, master)   
        self.grid()                       
        self.createWidgets()

    def printHello(self):
        print("Hello")

    def createWidgets(self):
        # xslider
        self.xscale = Scale(self, from_=-0.02, to=0.02, orient='horizontal',command=self.xslider_changed)
        self.xscale.grid(row=2,column=1)
        self.xscalelabel = Label(self, text='x_pos')
        self.xscalelabel.grid(row=3,columnspan=3)

        # yslider
        self.yscale = Scale(self, from_=-0.02, to=0.02, orient='horizontal',command=self.yslider_changed)
        self.yscale.grid(row=4,column=1)
        self.yscalelabel = Label(self, text='y_pos')
        self.yscalelabel.grid(row=5,columnspan=3)

        # zslider
        self.zscale = Scale(self, from_=-0.02, to=0.02, orient='horizontal',command=self.zslider_changed)
        self.zscale.grid(row=6,column=1)
        self.zscalelabel = Label(self, text='z_pos')
        self.zscalelabel.grid(row=7,columnspan=3)

        self.quitButton = Button(self, text='Quit',
            command=self.quit) # exits background (gui) thread
        self.quitButton.grid(row=1,column=6)    
        self.printButton = Button(self, text='Print',command=lambda: self.printHello())         
        self.printButton.grid(row=1,column=0) 

    def xslider_changed(self,event):  
        print(self.xscale.get())
    
    def yslider_changed(self,event):  
        print(self.xscale.get())

    def zslider_changed(self,event):  
        print(self.xscale.get())

