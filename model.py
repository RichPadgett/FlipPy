import os, sys
import Tkinter as tk
import tkMessageBox as tm
import fnmatch as fn
import glob
import re
import icons.Logo
import icons.Loading
import subprocess
from PIL import Image
import settings
import tagFinder
from xml.sax import parse
import time

images = ['*.gif', '*.png', '*.ppm', '*.jpg', '*.GIF']

class Model(object):
  def __init__(self, dir):
    self.dir = dir
    self.tagFind = None
    self.flipImg = []
    self.flipRate = []
    self.activefolder = None
    self.setpath = None
    self.dRate = 0
    self.loadSettings()
    self.loadLogo()
    self.writeSettings = []
    self.loadBool = False

  def loadSavedFolder(self):
    if os.path.isdir(self.activefolder):
      print "autoloading last saved folder: ", self.activefolder
      self.loadImages(self.activefolder)
      self.loadBool = True
    else: print "No Previously saved Folders"

  # grab any desired tags and save the data to a model variable 
  # tagFind is the Tag Handler
  def loadSettings(self):
    self.setpath = os.path.dirname(settings.__file__) 
    self.setpath = os.path.join(self.setpath, "settings.xml")
    self.tagFind = tagFinder.TagInfoHandler("FrameRate")
    parse(self.setpath, self.tagFind)  
    self.dRate = float(self.tagFind.getContent())
    self.tagFind = tagFinder.TagInfoHandler("Folder")
    parse(self.setpath, self.tagFind)
    self.activefolder = str(self.tagFind.getContent())
    if os.path.isdir(self.activefolder):
      self.loadBool = True

  # First 2 lines create a XMLSetting object and add to writeSettings list
  # Write Settings list is then written to disk each with a tag and data
  def saveSettings(self):
    rate = tagFinder.XMLSettings("FrameRate", str(self.dRate))
    self.writeSettings.append(rate)
    if self.activefolder != None:
      folder = tagFinder.XMLSettings("Folder", str(self.activefolder))
      self.writeSettings.append(folder)
    
    #write the document from the list to the filepath
    self.tagFind.writeXML(self.setpath, self.writeSettings)

  def loadImages(self, dir):
    self.flipImg = []
    imgFiles = []
    self.activefolder = dir
    files = os.listdir(dir)
    
    #append the full path of selected folder images
    for image in images:
      [imgFiles.append(os.path.join(dir, file)) for file in files if fn.fnmatch(file, image)]
     
    #Resize the images if the width is greater than 1000
    for x in imgFiles:
      check = Image.open(x)
      if  check.size[0] > 1000:
        params = ['convert', x, '-resize', '50%', x]
        subprocess.call(params, shell=True)

    #Sort the images
    sortedImgs = imgFileSort(files)
    [self.flipImg.append(os.path.join(dir, file)) for file in sortedImgs]
  
  def loadLogo(self):
    path = os.path.abspath(os.path.dirname(icons.Logo.__file__))
    self.Logo = []
    for x in range(73):
      name = "FLIP-Py" + str(x) + ".png"
      img = (os.path.join(path, name))
      self.Logo.append(img)
     
    self.flipImg = self.Logo
    
    pathRate = os.path.abspath(os.path.dirname(icons.Loading.__file__))
    self.flipRate = []
    for x in range(1,9):
      name2 = "ld" + str(x) + ".png"
      img = (os.path.join(pathRate, name2))
      self.flipRate.append(img)

def imgFileSort(files):
  sortedImgs = sorted(files, key=lambda x: (int(re.sub('\D','',x)),x)) 
  return sortedImgs
  
if __name__ == "__main__":
  m = Model(os.getcwd())
  print "Model instantiated:, ",m
