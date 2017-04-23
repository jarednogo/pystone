#!/usr/bin/python

import sgfparse
import tkFileDialog
from Tkinter import *

class MenuBar():
    def __init__(self, root):
        # First order of business, for later access
        self.root = root
    
        # create a top-level menu
        menubar = Menu(root)
        menubar.label = "menu"
    
        # create a pulldown menu
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.menu_open)
        filemenu.add_command(label="Save", command=self.menu_save)
    
        # add filemenu to the menu bar
        menubar.add_cascade(label="File", menu=filemenu)

        # Test menu
        #testmenu = Menu(menubar, tearoff=0)
        #testmenu.add_command(label="Click", command=self.test)
        #menubar.add_cascade(label="Testme", menu=testmenu)
    
        # display the menu
        self.root.config(menu=menubar)


    # MENU functions
    ################
    def menu_open(self):
        name = tkFileDialog.askopenfilename(\
                filetypes=(("Smart Game Format (SGF)","*.sgf"),\
                ("All files", "*.*")))
        print(name)
        keys,moves = sgfparse.process(name)
        for key in keys:
            print(key, keys[key])
        print(moves)

    def menu_save(self):
        canvas = None
        for item in self.root.children.values():
            if item.label == "canvas":
                canvas = item
        assert canvas is not None
        #print(canvas)
        #print(canvas.meta)
        # canvas.meta is the board from the GoBoard class
        moves = canvas.meta.MOVES
        #print(moves)
        name = tkFileDialog.asksaveasfilename(\
                filetypes=(("Smart Game Format (SGF)","*.sgf"),\
                ("All files", "*.*")))
        sgfparse.write(name, moves)
 
    ###############

    
