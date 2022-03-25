import numpy as np
from tkinter import HORIZONTAL, Frame, Tk, Label, Button, Text
from tkinter.ttk import Scale, Label, Separator

class Application(Frame):              
    def __init__(self, master=None):
        Frame.__init__(self, master) 
        self.position = [0, 0, 0]
        self.orienation = [0, 0, 0]
        self.grid()
        self.stepbuttonlist = []   
        self.scalelist = []                   
        self.createWidgets()

    def createWidgets(self):

        # x slider
        self.xscalelabel = Label(self, text='x_pos:  ' + '{:,f}'.format(self.position[0]))
        self.xscalelabel.grid(row=2, column=1)
        self.xscale = Scale(self, from_=-0.02, to=0.02, orient='horizontal',command=self.xslider_changed, length=200)
        self.xscale.grid(row=3, column=1, columnspan=3)
        self.xsep = Separator(self, orient='horizontal')
        self.xsep.grid(row=4, columnspan=7, sticky='ew')
        
        # y slider
        self.yscalelabel = Label(self, text='y_pos:  ' + '{:,f}'.format(self.position[1]))
        self.yscalelabel.grid(row=5, column=1)
        self.yscale = Scale(self, from_=-0.02, to=0.02, orient='horizontal',command=self.yslider_changed, length=200)
        self.yscale.grid(row=6, column=1, columnspan=3)
        self.ysep = Separator(self, orient='horizontal')
        self.ysep.grid(row=7, columnspan=7, sticky='ew')

        # z slider
        self.zscalelabel = Label(self, text='z_pos:  ' + '{:,f}'.format(self.position[2]))
        self.zscalelabel.grid(row=8,column=1)
        self.zscale = Scale(self, from_=-0.04, to=0.04, orient='horizontal',command=self.zslider_changed, length=200)
        self.zscale.grid(row=9, column=1 , columnspan=3)
        self.zsep = Separator(self, orient='horizontal')
        self.zsep.grid(row=10, columnspan=7, sticky='ew')

        # roll slider
        self.rollscalelabel = Label(self, text = 'roll:  ' + '{:,f}'.format(self.orienation[0]))
        self.rollscalelabel.grid(row = 11, column = 1)
        self.rollscale = Scale(self, from_=-np.pi / 4, to=np.pi / 4, orient='horizontal', command=self.rollsilder_changed, length=200)
        self.rollscale.grid(row = 12, column = 1, columnspan = 3)
        self.rollsep = Separator(self, orient='horizontal')
        self.rollsep.grid(row=13, columnspan=7, sticky='ew')

        # pitch slider
        self.pitchscalelabel = Label(self, text='pitch:  ' + '{:,f}'.format(self.orienation[1]))
        self.pitchscalelabel.grid(row=14, column=1)
        self.pitchscale = Scale(self, from_=-np.pi / 4, to=np.pi / 4, orient='horizontal', command=self.pitchslider_changed, length=200)
        self.pitchscale.grid(row=15, column=1, columnspan=3)
        self.pitchsep = Separator(self, orient='horizontal')
        self.pitchsep.grid(row=16, columnspan=7, sticky='ew')

        # yaw slider
        self.yawscalelabel = Label(self, text='yaw:  ' + '{:,f}'.format(self.orienation[2]))
        self.yawscalelabel.grid(row=17, column=1)
        self.yawscale = Scale(self, from_=-np.pi / 4, to=np.pi / 4, orient='horizontal', command=self.yawslider_changed, length=200)
        self.yawscale.grid(row=18, column=1, columnspan=3)
        self.yawsep = Separator(self, orient='horizontal')
        self.yawsep.grid(row=19, columnspan=7, sticky='ew')


        self.quitButton = Button(self, text='Quit',
            command=self.quit) # exits background (gui) thread
        self.quitButton.grid(row=1,column=0)    
        self.sendButton = Button(self, text='Send',command=lambda: self.senddata())         
        self.sendButton.grid(row=1,column=6) 

        # Text input box
        self.xtextbox = Text(self, height=1, width=5)
        self.xtextbox.grid(row=2,column=3)
        
        self.ytextbox = Text(self, height=1, width=5)
        self.ytextbox.grid(row=5,column=3)
        
        self.ztextbox = Text(self, height=1, width=5)
        self.ztextbox.grid(row=8,column=3)
        
        self.rolltextbox = Text(self, height=1, width=5)
        self.rolltextbox.grid(row=11,column=3)
        
        self.pitchtextbox = Text(self, height=1, width=5)
        self.pitchtextbox.grid(row=14,column=3)
        
        self.yawtextbox = Text(self, height=1, width=5)
        self.yawtextbox.grid(row=17,column=3)

        # Add extra spacing between separators
        self.grid_rowconfigure(4, minsize=10)
        self.grid_rowconfigure(7, minsize=10)
        self.grid_rowconfigure(10, minsize=10)
        self.grid_rowconfigure(13, minsize=10)
        self.grid_rowconfigure(16, minsize=10)

        self.scalelist.append(self.xscale)
        self.scalelist.append(self.yscale)
        self.scalelist.append(self.zscale)
        self.scalelist.append(self.rollscale)
        self.scalelist.append(self.pitchscale)
        self.scalelist.append(self.yawscale)

        for i in range(6):
            slider = self.scalelist.pop(0)
            posstepbutton = Button(self, text='+',command=lambda: self.stepslider(slider,'+'))
            posstepbutton.grid(row=3*(i+1), column=6)
            negstepbutton = Button(self, text='-',command=lambda: self.stepslider(slider,'-'))
            negstepbutton.grid(row=3*(i+1), column=0)
            self.stepbuttonlist.append(posstepbutton)
            self.stepbuttonlist.append(negstepbutton)

    def xslider_changed(self, event):  
        self.position[0] = self.xscale.get()
        self.xscalelabel.configure(text = 'xpos:  ' + '{:,f}'.format(self.position[0]))
    
    def yslider_changed(self, event):  
        self.position[1] = self.yscale.get()
        self.yscalelabel.configure(text = 'ypos:  ' + '{:,f}'.format(self.position[1]))

    def zslider_changed(self, event):  
        self.position[2] = self.zscale.get()
        self.zscalelabel.configure(text = 'zpos:  ' + '{:,f}'.format(self.position[2]))

    def rollsilder_changed(self, event):
        self.orienation[0] = self.rollscale.get()
        self.rollscalelabel.configure(text = 'roll:  ' + '{:,f}'.format(self.orienation[0]))

    def pitchslider_changed(self, event):
        self.orienation[1] = self.pitchscale.get()
        self.pitchscalelabel.configure(text = 'pitch:  ' + '{:,f}'.format(self.orienation[1]))

    def yawslider_changed(self, event):
        self.orienation[2] = self.yawscale.get()
        self.yawscalelabel.configure(text = 'yaw:  ' + '{:,f}'.format(self.orienation[2]))
    
    def stepslider(self, scale, msg):
        if msg == '+':
            scale.set(scale.get() + 0.01)

        if msg == '-':
            scale.set(scale.get() - 0.01)

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
