#!/usr/bin/python

import boardlib
import tkFileDialog
from Tkinter import *

class GoBoard():
    def __init__(self, root):
        # First order of business, for later access
        self.root = root

        # Constants
        self.SQ = 28
        
        # WIDTH should be odd
        self.WIDTH = 3
        self.OFFSET = 100
        self.STAR = 3
        self.CURFILL = 1
        self.COLORS = ["white", "black"]
        
        # Stone radius
        self.RADIUS = self.SQ/2 - 1
        
        # Board length
        self.LENGTH = self.SQ*18
        
        # Red crosses
        self.CROSSES = []
        
        # Stones
        # Use a dictionary to access stones (ints) via coordinates (tuples)
        # Learned: tuples are hashable, and lists are NOT
        self.STONES = {}
        
        # The board and the moves
        self.BOARD = boardlib.make_board()
        self.MOVES = []

        # canvas widget
        self.canvas = Canvas(root, width=self.LENGTH + 2*self.OFFSET, \
                height=self.LENGTH + 2*self.OFFSET)
        self.canvas.label = "canvas"
        self.canvas.meta = self
        self.canvas.pack()
    
        # Horizontals
        for i in xrange(19):
            self.draw_offset_line(0, i*self.SQ, self.LENGTH, i*self.SQ)
    
        # Verticals
        for i in xrange(19):
            self.draw_offset_line(i*self.SQ, 0, i*self.SQ, self.LENGTH)
    
        # Star points
        star_coords = [3,9,15]
        for p1 in star_coords:
            for p2 in star_coords:
                self.star(self.b2c(p1), self.b2c(p2))
    
        # Test circle
        self.cursor = self.bstone(-self.SQ,-self.SQ)
    
        # bind callbacks
        self.canvas.bind('<Motion>', self.motion)
        self.canvas.bind('<ButtonRelease-1>', self.left_click)
        self.canvas.bind('<Button-3>', self.right_click_down)
        self.canvas.bind('<ButtonRelease-3>', self.right_click_up)


    
    # DRAWINGS
    ###############
    def draw_offset_line(self, x1, y1, x2, y2):
        return self.canvas.create_line(x1 + self.OFFSET, y1 + self.OFFSET, x2 + self.OFFSET, y2 + self.OFFSET,\
                width=self.WIDTH)
    
    def create_circle(self, x,y,r, **kwargs):
        return self.canvas.create_oval(x-r, y-r, x+r, y+r, **kwargs)
    
    def bstone(self, x,y):
        return self.create_circle(x,y, self.RADIUS,\
                width=self.WIDTH, fill="black")
    
    def wstone(self,x,y):
        return self.create_circle(x,y, self.RADIUS,\
                width=self.WIDTH, fill="white")
    
    def stone(self, x, y, color):
        if color % 2 == 1:
            return self.bstone(x, y)
        else:
            return self.wstone(x, y)
    
    def star(self, x,y):
        return self.create_circle(x,y, self.STAR, width=self.WIDTH, fill="black")
    
    def cross(self, x, y, color):
        V = self.canvas.create_line(x - self.RADIUS, y, x + self.RADIUS, y, width=self.WIDTH, fill=color)
        H = self.canvas.create_line(x, y - self.RADIUS, x, y + self.RADIUS, width=self.WIDTH, fill=color)
        return (V,H)
    
    def red_cross(self, x, y):
        return self.cross(x, y, "red")
    
    def yellow_cross(self, x, y):
        return self.cross(x, y, "yellow")
    #############
    
    
    
    
    
    
    
    # COORDINATE FUNCTIONS
    #######################
    # Converts board coordinates to canvas coordinates
    def b2c(self, i):
        return i*self.SQ + self.OFFSET
    
    # Converts canvas coordinates to board coordinates
    def c2b(self, x):
        return int(round((float((self.bound(x) - self.OFFSET))/self.SQ)))
    
    # Ensure it's within the board
    def bound(self, x):
        xboard = x
        if xboard < self.OFFSET:
            xboard = self.OFFSET
        elif xboard > self.OFFSET + self.LENGTH:
            xboard = self.OFFSET + self.LENGTH
    
        return xboard
    
    def snap(self, x):
        return self.c2b(x)*self.SQ + self.OFFSET
    ######################
    
    
    
    # MISC 
    ###############
    def remove_stones(self):
        # Remove stones of the opposite color with 0 libs (black = 1, white = 2)
        OPP = self.opp_color()
    
        # Gather group reps
        reps = boardlib.get_all_reps(self.BOARD)
    
        # For each rep, check the color
        for rep in reps:
            if self.BOARD[rep[0]][rep[1]] == OPP:
                # If it's the right color, check the libs
                grp, libs = boardlib.get_group(self.BOARD, rep[0], rep[1])
    
                # If it has 0 libs, then delete them all!
                if len(libs) == 0:
                    for node in grp:
                        # Delete the canvas object
                        self.canvas.delete(self.STONES[node[0],node[1]])
    
                        # Delete it off the logical board
                        self.BOARD[node[0]][node[1]] = 0
    
    # Maps CURFILL to either 1 (black) or 2 (white)
    def cur_color(self):
        return 2 - (self.CURFILL % 2)
    
    # Maps CURFILL to opposite of cur_color
    def opp_color(self):
        return 2 - ((self.CURFILL + 1) % 2)
    
    # So, if a stone is capturing a group, then it's not a suicide move
    # If it captures even a SINGLE stone, then it's not a suicide move
    def suicide(self, i,j):
        temp = boardlib.copy_board(self.BOARD)
        cur = self.cur_color()
        opp = self.opp_color()
    
        temp[i][j] = cur
        grp,libs = boardlib.get_group(temp, i, j)
    
        # If we get 0 libs, it's a POTENTIAL suicide move
        if len(libs) == 0:
            # Let's check the neighbors for capturing first...
            nbd = boardlib.get_neighbors(i,j)
            for nbr in nbd:
                if temp[nbr[0]][nbr[1]] == opp:
                    opp_grp, opp_libs = boardlib.get_group(temp, nbr[0], nbr[1])
                    if len(opp_libs) == 0:
                        print("Capturing move!")
                        return False
            print("Suicide move!")
            return True
        return False

    # Helper functions for black and white stones
    def place_stone(self, i,j, color):
        i_,j_ = self.b2c(i), self.b2c(j)

        # Update the stones dictionary (and place the stone)
        self.STONES[i,j] = self.stone(i_,j_,color)

        # Update the board (black = 1, white = 2)
        self.BOARD[i][j] = color
            
        # Also update the move
        self.MOVES.append((i,j))
    
        # Remove stones
        self.remove_stones()
    ################################





     
    # CALLBACKS
    #################
    def motion(self, event):
        x,y = event.x, event.y
        if x != self.bound(x) or y != self.bound(y):
            self.canvas.coords(self.cursor, -self.SQ, -self.SQ, 0, 0)
        else:
            x,y = self.snap(event.x), self.snap(event.y)
            #print(event.x, event.y)
            self.canvas.coords(self.cursor, x-self.RADIUS, y-self.RADIUS, \
                    x+self.RADIUS, y+self.RADIUS)
            color = self.COLORS[self.CURFILL % 2]
            self.canvas.itemconfig(self.cursor, fill=color)
    

    def left_click(self, event):
        i_,j_ = self.snap(event.x), self.snap(event.y)
        i, j = self.c2b(event.x),self.c2b(event.y)
    
        # Black = 1, whte = 2
        cur = self.cur_color()

        # Make sure we're within bounds
        if self.bound(event.x) != event.x or self.bound(event.y) != event.y:
            return
    
        # Should also make sure that it wouldn't have zero libs...
        if self.suicide(i,j):
            return
    
        if not self.BOARD[i][j]:
            # Place black stone
            self.place_stone(i,j,cur)
    
            # Increment color
            self.CURFILL += 1
    
    def right_click_down(self, event):
        i, j = self.c2b(event.x), self.c2b(event.y)
        
        # Light up clicked stone
        # In fact, light up entire group!!!
        grp,libs = boardlib.get_group(self.BOARD, i, j)
    
        for point in libs:
            i_,j_ = self.b2c(point[0]), self.b2c(point[1])
            # FYI, the cross is a pair of ints (hence the +=)
            self.CROSSES += self.yellow_cross(i_, j_)
        for point in grp:
            i_,j_ = self.b2c(point[0]), self.b2c(point[1])
            self.CROSSES += self.red_cross(i_, j_)
    
    def right_click_up(self, event):
        # Delete all crosses
        for item in self.CROSSES:
            self.canvas.delete(item)
        
        # Reset crosses
        self.CROSSES = []
    #####################

