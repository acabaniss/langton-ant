import matplotlib
matplotlib.use('TkAgg')
import pylab as pl
# import necessary modules
import random as rd
import numpy as np
import scipy as sp

# define model parameters
gridsize = 80 #size of each side of the grid
start = 10000 #how many time steps to run in the background before beginning
wraps = 1 #whether the world wraps or the boundaries are fixed; can also be true/false

#internal variables
north, east, south, west = xrange(4) #set the variables for the ant heading
movement = [(0,-1),(1,0),(0,1),(-1,0)] #get the movements needed for each direction
arrows = ['v','>','^','<'] #the plotting variables for the ant
white, black = xrange(2) # set the variables for the cells in the world

#check inputs for consistency
assert(gridsize > 10)
assert(type(gridsize) == int)
assert(wraps == 1 | wraps == 0)
assert(type(start) == int)

#Define the object classes: world (ca grid) and langton (Langton's ant)
class world(object): #Define the environment/world class
    def __init__(self,gridsize,setup = 'blank'): #set up the grid of the environment
        self.gridsize = gridsize
        self.config = np.zeros((gridsize,gridsize))
        self.setup = setup #there are two setup modes, random and blank; blank is default
        for i, j in [(x,y) for x in xrange(gridsize) for y in xrange(gridsize)]: #populate the world according to the initial conditions
            if self.setup == 'random':
                self.config[j,i] = rd.choice(black,white)
            elif self.setup == 'blank':
                self.config[j,i] = white

class langton(object): #Define the ant class
    def __init__(self,w,x,y,h=north): #setup the ant
        self.x = x # x and y set the initial coordinates of the ant; these are always integer between 0 and world.gridsize - 1 inclusive
        self.y = y
        self.w = w #w is a reference to the world instance
        self.h = h #h is the NESW heading as defined above
    def move(self): #move according to the current heading
            self.x += movement[self.h][0] #move forward according to the heading, x
            self.y += movement[self.h][1] #move forward according to the heading, y
    def update(self):
        #implement the movement rules
        if self.w.config[self.y,self.x] == black: #if the current cell is black, then:
            self.h = (self.h - 1) % 4 #rotate left 90
            self.w.config[self.y,self.x] = white # set the current cell to white
            self.move()
        else: # if the current cell is white, then:
            self.h = (self.h + 1) % 4 # rotate right 90
            self.w.config[self.y,self.x] = black #set the current cell to black
            self.move() 
            
#Define the three functions: init, draw, update
def initialize():
    global w, ant, time, keepgoing, gridsize, start   # list global variables
    # initialize system states
    w = world(gridsize,'blank') #Create the world
    ant = langton(w,int(round(w.gridsize/2.))-5,int(round(w.gridsize/2.))+5,north) #Create the ant
    
    #run the first start time steps before beginning,
    time = 0 #Set the step counter
    keepgoing = True #Create a check to stop the simulation when the ant hits the borders if the world is fixed
    if start>0: #run the previous start time steps in the background before beginning; this enables one to quickly observe the 10k step mark without having to visualize it
        for i in xrange(start):
            update()                 

def observe():
    global w, ant, time# list global variables
    pl.cla() # to clear the visualization space
    # visualize system states
    #plot the world
    pl.pcolor(w.config,vmin = white, vmax = black, cmap = pl.cm.Greys) #adapted from the other ca examples in the py-cx folder, such as ca-forestfire.py
    pl.hold(True)
    #plot the ant
    pl.plot(ant.x+.5,ant.y+.5,'r'+arrows[ant.h]) #note the weirdness of the heading because of the way matrices are plotted, namely with north down; this is why the arrow list is relied on
    pl.axis('image')
    pl.title("Langton's Ant, t = " + str(time))
    pl.hold(False)
    pl.draw()
    
def update():
    global w, ant, time, keepgoing, wraps# list global variables
    # update system states for one discrete time step
    #This step is implemented different if the world wraps
    if wraps == False: #if boundaries are fixed:
        if ant.x == 0 or ant.x == w.gridsize - 1 or ant.y == 0 or ant.y == w.gridsize - 1: #if at the edges of the world, stop the simulation
            keepgoing = False
        if keepgoing == True: #else:
            ant.update() # follow ant update and movement rules
            time += 1 # increment the time counter
    else: # if the world wraps, then updates will never end
        ant.update() #follow ant update and movement rules
        ant.x = ant.x % w.gridsize #wrap the world
        ant.y = ant.y % w.gridsize
        time += 1 #incremenet the time counter

#Define the parameter selection; these examples are adapted from the abm-schelling.py script in the Py-CX repository and from the course website
def wrapsF(val = wraps):
    """
    Whether the world wraps. Input is 0 = False, 1 = True
    The parameter shouldn't be changed in a running model.
    """
    global wraps
    wraps = bool(val)
    return val    

def startF(val = start):
    """
    What time step to start the model visualization at.
    This can only be changed for a new model."
    """
    global start
    start = int(val)
    return val
    
def gridsizeF(val = gridsize):
    """
    Gridsize of the world. Min 10.
    This can only be changed for a new model.
    """
    global gridsize
    gridsize= int(val)
    return val

import pycxsimulator
pycxsimulator.GUI(parameterSetters=[wrapsF,startF,gridsizeF]).start(func=[initialize, observe, update])