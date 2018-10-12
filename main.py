#!/usr/bin/python

import os,sys
import Tkinter as tk
import include.controller
import flipbooks

if __name__ == "__main__":
  dir = os.path.abspath(os.path.dirname(flipbooks.__file__))
  c = include.controller.Controller(dir)

  tk.mainloop()
