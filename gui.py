import numpy as np
from tkinter import Frame, Tk, Label, Button, Text
from tkinter.ttk import Scale, Label

class Application(Frame):              
    def __init__(self, master=None):
        Frame.__init__(self, master) 
        self.position = [0, 0, 0]
        self.orienation = [0, 0, 0]
        self.grid()                       
        self.createWidgets()

    def createWidgets(self):

        # x slider
        self.xscale = Scale(self, from_=-0.02, to=0.02, orient='horizontal',command=self.xslider_changed)
        self.xscale.grid(row=2, column=1, columnspan=3)
        self.xscalelabel = Label(self, text='x_pos: ' + '{:,f}'.format(self.position[0]))
        self.xscalelabel.grid(row=3, column=1)
        
        # y slider
        self.yscale = Scale(self, from_=-0.02, to=0.02, orient='horizontal',command=self.yslider_changed)
        self.yscale.grid(row=4, column=1, columnspan=3)
        self.yscalelabel = Label(self, text='y_pos:' + '{:,f}'.format(self.position[1]))
        self.yscalelabel.grid(row=5, column=1)

        # z slider
        self.zscale = Scale(self, from_=-0.04, to=0.04, orient='horizontal',command=self.zslider_changed)
        self.zscale.grid(row=6, column=1 , columnspan=3)
        self.zscalelabel = Label(self, text='z_pos: ' + '{:,f}'.format(self.position[2]))
        self.zscalelabel.grid(row=7,column=1)

        # roll slider
        self.rollscale = Scale(self, from_=-np.pi / 4, to=np.pi / 4, orient='horizontal', command=self.rollsilder_changed)
        self.rollscale.grid(row = 8, column = 1, columnspan = 3)
        self.rollscalelabel = Label(self, text = 'roll: ' + '{:,f}'.format(self.orienation[0]))
        self.rollscalelabel.grid(row = 9, column = 1)

        # pitch slider
        self.pitchscale = Scale(self, from_=-np.pi / 4, to=np.pi / 4, orient='horizontal', command=self.pitchslider_changed)
        self.pitchscale.grid(row=10, column=1, columnspan=3)
        self.pitchscalelabel = Label(self, text='pitch: ' + '{:,f}'.format(self.orienation[1]))
        self.pitchscalelabel.grid(row=11, column=1)

        # yaw slider
        self.yawscale = Scale(self, from_=-np.pi / 4, to=np.pi / 4, orient='horizontal', command=self.yawslider_changed)
        self.yawscale.grid(row=12, column=1, columnspan=3)
        self.yawscalelabel = Label(self, text='yaw: ' + '{:,f}'.format(self.orienation[2]))
        self.yawscalelabel.grid(row=13, column=1)

        self.quitButton = Button(self, text='Quit',
            command=self.quit) # exits background (gui) thread
        self.quitButton.grid(row=1,column=0)    
        self.sendButton = Button(self, text='Send',command=lambda: self.senddata())         
        self.sendButton.grid(row=1,column=6) 

        # Text input box
        self.xtextbox = Text(self, height=1, width=5)
        self.xtextbox.grid(row=3,column=3)
        
        self.ytextbox = Text(self, height=1, width=5)
        self.ytextbox.grid(row=5,column=3)
        
        self.ztextbox = Text(self, height=1, width=5)
        self.ztextbox.grid(row=7,column=3)
        
        self.rolltextbox = Text(self, height=1, width=5)
        self.rolltextbox.grid(row=9,column=3)
        
        self.pitchtextbox = Text(self, height=1, width=5)
        self.pitchtextbox.grid(row=11,column=3)
        
        self.yawtextbox = Text(self, height=1, width=5)
        self.yawtextbox.grid(row=13,column=3)

    def xslider_changed(self, event):  
        self.position[0] = self.xscale.get()
        self.xscalelabel.configure(text = 'xpos: ' + '{:,f}'.format(self.position[0]))
    
    def yslider_changed(self, event):  
        self.position[1] = self.yscale.get()
        self.yscalelabel.configure(text = 'ypos: ' + '{:,f}'.format(self.position[1]))

    def zslider_changed(self, event):  
        self.position[2] = self.zscale.get()
        self.zscalelabel.configure(text = 'zpos: ' + '{:,f}'.format(self.position[2]))

    def rollsilder_changed(self, event):
        self.orienation[0] = self.rollscale.get()
        self.rollscalelabel.configure(text = 'roll: ' + '{:,f}'.format(self.orienation[0]))

    def pitchslider_changed(self, event):
        self.orienation[1] = self.pitchscale.get()
        self.pitchscalelabel.configure(text = 'pitch: ' + '{:,f}'.format(self.orienation[1]))


    def yawslider_changed(self, event):
        self.orienation[2] = self.yawscale.get()
        self.yawscalelabel.configure(text = 'yaw: ' + '{:,f}'.format(self.orienation[2]))
    
    def senddata(self):

        try:
            self.xscale.set(float(self.xtextbox.get("1.0","end-1c")))
        except ValueError:
            self.xscale.set(0)

        try:    
            self.yscale.set(float(self.ytextbox.get("1.0","end-1c")))
        except ValueError:
            self.yscale.set(0)

        try:
            self.zscale.set(float(self.ztextbox.get("1.0","end-1c")))
        except ValueError:
            self.zscale.set(0)

        try:
            self.rollscale.set(float(self.rolltextbox.get("1.0","end-1c")))
        except ValueError:
            self.rollscale.set(0)

        try:        
            self.pitchscale.set(float(self.pitchtextbox.get("1.0","end-1c")))
        except ValueError:
            self.pitchscale.set(0)

        try:    
            self.yawscale.set(float(self.yawtextbox.get("1.0","end-1c")))
        except ValueError:
            self.yawscale.set(0)

    def get_position(self):
        return self.position

    def get_orientation(self):
        return self.orienation  
