import Tkinter as tk
import model, view
import tkFont
import tkMessageBox
import ttk as ttk
import controller
import os
from PIL import ImageTk
import threading
import time

class NotAController(object):
  pass

class View(object):
  def __init__(self, controller):
    self.controller = controller
    self.root = tk.Tk()
    self.t = None
    self.t2 = None
    self.root.bind('<Escape>', lambda event: self.saveOnClose())
    self.root.protocol("WM_DELETE_WINDOW", self.saveOnClose)
    self.root.configure(bg = "#EFF5FF", bd=5, relief=tk.FLAT)
    self.root.title('FLIP-PY GIFANIMATOR')
    self.myFont = tkFont.Font(family="Ubuntu-Mono", size=14)
    self.makeMenu()
    self.makeView()

  # Save data on any close option
  def saveOnClose(self):
    self.controller.saveXMLData()
    self.root.destroy()

  def makeMenu(self):
    self.menuPanel = tk.Frame(height=20)
    self.menuPanel.configure(bg="#EFF5FF")

    #File Menu Button Icon
    flIcon = tk.PhotoImage(file="icons/fil.png")
    self.btFile = tk.Menubutton(self.menuPanel, image=flIcon,\
                                font=self.myFont, text="File", compound=tk.LEFT)
    self.btFile.image = flIcon
    self.btFile.configure(bg="#EFF5FF")
    self.btFile.config(menu=self.btFile)
    fileMenu = tk.Menu(self.btFile, tearoff=0)
    fileMenu.add_command(label="Load", font=self.myFont,\
                         command=self.controller.load)
    fileMenu.add_command(label="Load Intro", font=self.myFont,\
                         command=self.controller.loadLogo)
    fileMenu.add_command(label="User Guide", font=self.myFont,\
                         command=self.controller.userGuide)
    fileMenu.add_command(label="Kill", font=self.myFont,\
                         command=self.root.quit)
    self.btFile.config(menu=fileMenu)
    
    #Editor Selection Menu
    edIcon = tk.PhotoImage(file="icons/immag.png")
    self.btEdit = tk.Menubutton(self.menuPanel, image=edIcon,\
                                font=self.myFont, text="Convert",compound=tk.LEFT)
    self.btEdit.image = edIcon
    self.btEdit.configure(bg="#EFF5FF")
    self.btEdit.config(menu=self.btEdit)

    #Convert Format
    editBar = tk.Menu(self.btEdit, tearoff=0)
    editBar.config(bg="#EFF5FF", relief=tk.FLAT)
    convertMenu = tk.Menu(editBar, tearoff=0)
    convertMenu.add_command(label="GIF", font=self.myFont,\
                         command = lambda: self.controller.convert("GIF"))
    convertMenu.add_command(label="PNG", font=self.myFont,\
                         command = lambda: self.controller.convert("PNG"))
    convertMenu.add_command(label="JPG", font=self.myFont,\
                         command = lambda: self.controller.convert("JPG"))
    editBar.add_cascade(menu=convertMenu, font=self.myFont, label="File Type")

    #Resize Images
    sizeMenu = tk.Menu(editBar, tearoff=0)
    sizeMenu.add_command(label="25%", font=self.myFont,\
                         command = lambda: self.controller.percent(25))
    sizeMenu.add_command(label="50%", font=self.myFont,\
                         command = lambda:self.controller.percent(50))
    sizeMenu.add_command(label="75%", font=self.myFont,\
                         command = lambda:self.controller.percent(75))
    sizeMenu.add_command(label="125%", font=self.myFont,\
                         command = lambda:self.controller.percent(125))
    sizeMenu.add_command(label="150%", font=self.myFont,\
                         command = lambda:self.controller.percent(150))
    sizeMenu.add_command(label="175%", font=self.myFont,\
                         command = lambda:self.controller.percent(175))
    editBar.add_cascade(menu=sizeMenu, font=self.myFont, label="Re-Size")

    #Resketch Images
    drawMenu = tk.Menu(editBar, tearoff=0)
    drawMenu.add_command(label="Pencil", font=self.myFont,command = lambda:\
                         self.controller.transpose("Sketch"))
    drawMenu.add_command(label="Charcoal",font=self.myFont, command = lambda:\
                         self.controller.transpose("Charcoal"))
    drawMenu.add_command(label="Emboss", font=self.myFont, command = lambda:\
                         self.controller.transpose("Emboss"))
    drawMenu.add_command(label="High Contrast", font=self.myFont, command = lambda:\
                         self.controller.transpose("Contrast"))
    drawMenu.add_command(label="Black Vignette", font=self.myFont, command = lambda:\
                         self.controller.transpose("BlackVignette"))
    drawMenu.add_command(label="Transparent Vignette", font=self.myFont, command = lambda:\
                         self.controller.transpose("TransparentVignette"))
    drawMenu.add_command(label="Polaroid", font=self.myFont, command = lambda:\
                         self.controller.transpose("Polaroid"))
    editBar.add_cascade(menu=drawMenu, font=self.myFont, label="Re-Sketch")
                    
    #Generate Animation
    generateMenu = tk.Menu(editBar, tearoff=0)
    generateMenu.add_command(label="GIFAnimation File", font=self.myFont,command = lambda:\
                         self.controller.gifanimate("Loop"))
    editBar.add_cascade(menu=generateMenu, font=self.myFont, label="Generate")
    self.btEdit.config(menu=editBar)

  def makeView(self):
    #main center view
    screen = tk.PhotoImage(file="icons/Logo/FLIP-Py0.png")
    self.viewer = tk.Label(width=900, height=660, image=screen)
    self.viewer.image = screen
    self.viewer.configure(bg="#000000")

    #thin left edge
    ltPanel = tk.Frame(width=5)
    ltPanel.configure(bg="#EFF5FF")

    #thin right edge
    rtPanel = tk.Frame(width=5)
    rtPanel.configure(bg="#EFF5FF")

    #between viewer and progress bar
    separator = tk.Frame(bg="#EFF5FF", height=5, bd=1, relief=tk.SUNKEN)

    #panel progress bar sits on above bottom panel
    progPanel = tk.Frame(height=10)
    progPanel.configure(bg="#EFF5FF")
    
    #Progress Bar, sits above bottom panel
    self.progBar = ttk.Progressbar(progPanel, orient='horizontal',\
                                   mode='determinate')
    #Bottom Frame, Play, Strop
    bmPanel = tk.Frame(height=35)
    bmPanel.configure(bg="#EFF5FF")
    
    #Play Button
    playIcon = tk.PhotoImage(file="icons/play.png")
    btPlay = tk.Button(bmPanel, image=playIcon)
    btPlay.image = playIcon
    btPlay.configure(bg="#EFF5FF", command=self.thread)

    #Loop Button
    loopIcon = tk.PhotoImage(file="icons/single.gif")
    self.btLoop = tk.Button(bmPanel, image=loopIcon)
    self.btLoop.bind("<Button-1>", self.controller.loop)
    self.btLoop.image = loopIcon
    self.btLoop.configure(bg="#EFF5FF")


    #Stop Button
    stopIcon = tk.PhotoImage(file="icons/stop.png")
    btStop = tk.Button(bmPanel, image=stopIcon)
    btStop.image = stopIcon
    btStop.configure(bg="#EFF5FF", command=self.controller.stop)

    #Step Left Button, Bottom Panel
    ltIcon = tk.PhotoImage(file="icons/rewind.png")
    stepLt = tk.Button(bmPanel, image=ltIcon)
    stepLt.image = ltIcon
    stepLt.configure(bg="#EFF5FF", command=self.controller.stepLt)

    #Step Right Button, Bottom Panel
    rtIcon = tk.PhotoImage(file="icons/fastforward.png")
    stepRt = tk.Button(bmPanel, image=rtIcon)
    stepRt.image = rtIcon
    stepRt.configure(bg="#EFF5FF", command=self.controller.stepRt)


    #Frame Rate Indicator that shows frame rate and autoloads saved Giffy
    rateInd = tk.PhotoImage(file="icons/Loading/ld1.png")
    self.btInd = tk.Button(bmPanel, image=rateInd)
    self.btInd.image = rateInd
    self.btInd.configure(bg="#EFF5FF", command=self.controller.autoLoad)

    #Frame Rate Selector
    rateVar = tk.StringVar(bmPanel)
    rateVar.set(self.controller.model.dRate)
    self.frmRate1 = tk.Spinbox(bmPanel, from_=0, to=9, increment=.005,\
                               font=self.myFont, format="%0.3f", wrap=True)
    self.frmRate1.bind("<Return>", self.controller.frameUpdate)
    self.frmRate1.bind("<KP_Enter>", self.controller.frameUpdate)
    self.frmRate1.configure(bg="#EFF5FF", width=5, textvariable=rateVar,\
                            command=self.controller.frameRate)
    
    #Frame Rate Labels
    lblRate = tk.Label(bmPanel, font=self.myFont, text="Refresh-Rate")
    lblRate.configure(bg="#EFF5FF")
    lblSec = tk.Label(bmPanel, font=self.myFont, text="s")
    lblSec.configure(bg="#EFF5FF")

    #Panel Packing Order Matters
    self.menuPanel.pack(side=tk.TOP, fill=tk.X)
    self.btFile.pack(side=tk.LEFT)
    self.btEdit.pack(side=tk.LEFT)
    ltPanel.pack(side=tk.LEFT, fill=tk.Y)
    rtPanel.pack(side=tk.RIGHT, fill=tk.Y)
    self.viewer.pack(side=tk.TOP,expand=True, fill=tk.BOTH)
    self.progBar.pack(expand=True, side=tk.TOP, fill=tk.BOTH)
    btPlay.pack(side=tk.LEFT)
    self.btLoop.pack(side=tk.LEFT)
    btStop.pack(side=tk.LEFT)
    stepLt.pack(side=tk.LEFT)
    stepRt.pack(side=tk.LEFT)
    lblSec.pack(side=tk.RIGHT)
    self.btEdit.pack(side=tk.LEFT)
    self.frmRate1.pack(side=tk.RIGHT)
    self.btInd.pack(side=tk.RIGHT)
    lblRate.pack(side=tk.RIGHT)
    bmPanel.pack(side=tk.BOTTOM, fill=tk.X)
    progPanel.pack(side=tk.BOTTOM, fill=tk.X)
    separator.pack(side=tk.BOTTOM, fill=tk.X)
 
  def thread(self):
    if self.t == None or not self.t.isAlive(): 
      self.t = threading.Thread(target=self.controller.play)
      self.t.daemon = True
      self.t.start()

  def thread2(self):
    if self.t2 == None or not self.t2.isAlive():
      self.controller.model.loadSettings()
      self.t2 = threading.Thread(target=self.controller.rateIndicator)
      self.t2.loadB = True
      self.t2.daemon = True
      self.t2.start()

  def display(self, img, fR):
    newimg = ImageTk.PhotoImage(ImageTk.Image.open(img))
    self.viewer.configure(image=newimg)
    self.viewer.image=newimg
    self.root.update_idletasks()
    time.sleep(float(fR))
   
  def displayFrmRate(self, img, fR, frame):
    newimg = ImageTk.PhotoImage(ImageTk.Image.open(img))
    self.btInd.configure(image=newimg)
    self.btInd.image=newimg
    self.root.update_idletasks()
    time.sleep(fR)
    
if __name__ == "__main__":
  view = View(NotAController())
  tk.mainloop()
