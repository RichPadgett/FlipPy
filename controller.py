import os,sys
import model, view
import Tkinter as tk
import tkMessageBox as tm
import subprocess
from PIL import ImageTk
import tkFileDialog

class Controller(object):
  def __init__(self, dir):
    self.model = model.Model(dir)
    self.view = view.View(self)
    self.Stop = False
    self.frame = 0
    self.len = len(self.model.flipImg)
    self.loop = False
    self.fast = False
    self.view.thread()
    self.view.thread2()
    
  def saveXMLData(self):
    self.model.saveSettings()

  def userGuide(self):
    print "Opening User Manual ..."
    subprocess.call(['gedit', "include/USERMANUAL.txt"])

  def stepLt(self):
    if self.frame != 0: 
      self.view.display(self.model.flipImg[self.frame],float(self.model.dRate))
      self.view.progBar.step(-(float(100)/self.len))
      self.frame = self.frame - 1
    
  def stepRt(self):
    if self.frame == self.len: self.frame = 0
    self.view.display(self.model.flipImg[self.frame], float(self.model.dRate))
    self.view.progBar.step(float(100)/self.len)
    self.frame = self.frame + 1

  def load(self):

    if self.loop == True:
      self.loop = False
      icn = ImageTk.PhotoImage(ImageTk.Image.open("icons/single.gif"))
      self.view.btLoop.configure(image=icn)
      self.view.btLoop.image=icn
      self.view.root.update_idletasks()
    self.Stop = True
    self.view.root.update_idletasks()
    while self.frame > 0:
       self.view.progBar.step(-(float(100)/self.len))
       self.frame = self.frame - 1   
    dirname = tkFileDialog.askdirectory()
    if dirname != ():
      if os.path.isdir(dirname):
        self.model.loadImages(dirname)
        self.display()

  def display(self):
    self.view.display(self.model.flipImg[0], self.model.dRate) 
    self.len = len(self.model.flipImg)
    
  def rateIndicator(self):
    len = 8
    frame = 0
    while frame < len:
      self.view.displayFrmRate(self.model.flipRate[frame],\
                               float(self.model.dRate), frame)
      frame = (frame + 1)%8

  def autoLoad(self):
    self.model.loadSavedFolder()
    if self.model.loadBool:
      self.display()
      self.view.t2.loadB = False

  def loadLogo(self):
     self.model.loadLogo()
     self.play()

  def frameRate(self):
    self.model.dRate = self.view.frmRate1.get()
    
  def frameUpdate(self, event):
    self.frameRate()

  def play(self):
   self.Stop = False
   self.len = len(self.model.flipImg)
   while self.frame < self.len and not self.Stop: 
     self.view.display(self.model.flipImg[self.frame], float(self.model.dRate))
     self.view.progBar.step(float(100)/self.len)
     self.frame = self.frame + 1
      
   if self.frame == self.len: 
     self.view.progBar.stop()
     self.frame = 0

   if self.loop == True:
     self.play()    
   
  def loop(self, event):
    if self.loop == False:
      self.loop = True
      icn = ImageTk.PhotoImage(ImageTk.Image.open("icons/loop.gif"))
    else: 
      self.loop = False
      icn = ImageTk.PhotoImage(ImageTk.Image.open("icons/single.gif"))
    event.widget.configure(image=icn)
    event.widget.image=icn
    self.view.root.update_idletasks()

  def stop(self):
    self.Stop = True 

  #Convert File Format of Whole Folder, Only Gifs Animate
  def convert(self, filetype):
    name = os.path.split(self.model.activefolder)[1]
    dir = os.path.dirname(self.model.activefolder)
    dir = os.path.join(dir,  filetype + "_" + name)
    if not os.path.exists(dir):
      os.mkdir(dir)
    print "Converting ..."  
    for x in self.model.flipImg:
      if filetype == "GIF":
        params = ['convert', x, os.path.join(dir,\
                 os.path.split(os.path.splitext(x)[0])[1] + ".gif")]
        subprocess.call(params)
      if filetype == "PNG":
        params = ['convert', x, os.path.join(dir,\
                 os.path.split(os.path.splitext(x)[0])[1] + ".png")]
        subprocess.call(params)
      if filetype == "JPG":
        params = ['convert', x, os.path.join(dir,\
                 os.path.split(os.path.splitext(x)[0])[1] + ".jpg")]
        subprocess.call(params)
    print "Conversion Complete, Check Following Directory For Your Sketches:"  
    print dir
    self.model.loadImages(dir)
    self.display()


  #Resize the whole Folder to a new Size
  def percent(self, percent): 
    name = os.path.split(self.model.activefolder)[1]
    dir = os.path.dirname(self.model.activefolder)
    dir = os.path.join(dir, str(percent) + "%_" + name)
    if not os.path.exists(dir):
      os.mkdir(dir)
    print "Converting ..."  
    for x in self.model.flipImg:
       params = ['convert', x, '-resize', str(percent) + "%",\
                 os.path.join(dir, os.path.split(x)[1])]
       subprocess.call(params)
       
    print "Resize Complete, Check Following Directory For Your Sketches:"  
    print dir
    self.model.loadImages(dir)
    self.display()

  #Re-Sketch the Whole Folder to a new type
  def transpose(self, effect): 
    if os.path.isabs( self.model.activefolder):
      name = os.path.split(self.model.activefolder)[1]
      dir = os.path.dirname(self.model.activefolder)
      dir = os.path.join(dir, str(effect)+ "_" + name)
      if not os.path.exists(dir):
        os.mkdir(dir)
      print "converting ..."  
      for x in self.model.flipImg:
         if effect == "Sketch":
           params = ['convert', x, "-colorspace", "gray", "-sketch", "0x20+120",\
                   os.path.join(dir, os.path.split(x)[1])]
         elif effect == "Charcoal":
           params = ['convert', x, "-charcoal", "2",\
                   os.path.join(dir, os.path.split(x)[1])]
         elif effect == "Emboss":
           params = ['convert', x, "-emboss", "0x.5",\
                   os.path.join(dir, os.path.split(x)[1])]
         elif effect == "Contrast":
           params = ['convert', x, "-fx",\
                     "(1.0/(1.0+exp(10.0*(0.5-u)))-0.006693)*1.00922503",\
                   os.path.join(dir, os.path.split(x)[1])]
         elif effect == "BlackVignette":
           params = ['convert', x, "-background", "black","-vignette","0x2",\
                   os.path.join(dir, os.path.split(x)[1])]
         elif effect == "TransparentVignette":
           params = ['convert', x,"-alpha", "Set", "-background",\
                     "none","-vignette","0x2",\
                   os.path.join(dir, os.path.split(x)[1])]
         elif effect == "Polaroid":
           params = ['convert', x, "-bordercolor",\
                     "white", "-background", "black","+polaroid",\
                   os.path.join(dir, os.path.split(x)[1])]
         subprocess.call(params)
      print "Re-Sketch Complete, Check Following Directory For Your Sketches:"  
      print dir
      self.model.loadImages(dir)
      self.display()

    else:
      tm.showinfo("Notification", "Load a Flipbook through File, Load,\
                  Flipbooks. Then Choose the Flipbook you want to work on.")
     
  #Create A Single File That is Animated GIF
  def gifanimate(self, command):
    if self.model.flipImg[0].endswith(".gif") or\
       self.model.flipImg[0].endswith(".GIF") or\
       self.model.flipImg[0].endswith(".miff"):
      name = os.path.split(self.model.activefolder)[1]
      dir = os.path.dirname(self.model.activefolder)
      dir = os.path.join(dir, "Animation_" + name)
      if not os.path.exists(dir):
        os.mkdir(dir)
      print "converting ..."
      params = ['convert',"-delay", str(self.model.dRate)]
      for x in self.model.flipImg:
        params.append(x)
      params.append("-loop")
      params.append("0")
      params.append(os.path.join(dir, os.path.split(self.model.flipImg[0])[1]))
      subprocess.call(params)
      print "Animation Done! Check Following Directory For Your Animation: "
      print dir
      f = os.listdir(dir)
      subprocess.call(["eog", os.path.join(dir, f[0])])

    else: tm.showinfo("Notification", "Animation Not Created,\
                      Please Convert FlipBook to GIF.\
                      located under Convert -> File Type")
    

if __name__ == "__main__":
  c = Controller("Test")
  print "model is: ", c.model
  print "view is:  ", c.view
