#!/usr/bin/python

import graphicslib, menulib

from Tkinter import *

if __name__ == '__main__':
    # main widget
    root = Tk()
    
    # Board widget 
    BoardApp = graphicslib.GoBoard(root)

    # Menu widget
    MenuApp = menulib.MenuBar(root)

    # Main loop
    root.mainloop()

