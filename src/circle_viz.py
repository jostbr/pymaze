import matplotlib.pyplot as plt
from matplotlib.patches import Arc
import math
import numpy as np

class Visualizer(object):
    """Class that temperorily handles aspects of visualization for a circular maze.


    Attributes:
        maze: The maze that will be visualized"""

    def __init__(self,maze):
        self.maze = maze
        self.size = maze.num_rows   #Total number of circular layers in maze
        fig_width, fig_height = 10,10  
        self.fig, self.ax = plt.subplots(1, 1)
        self.ax.axis([-self.size, self.size, -self.size, self.size])
        self.ax.set_axis_off()
        self.visualize()
        plt.show()
        
    def visualize(self):
        r_factor = 0.0174533    #Factor to convert degrees into radians
        for i in range(self.maze.num_rows):
            angle = 360/math.pow(2,2+int(i/2))*r_factor     #Generates an angle in degrees for each with respect to the centre of the maze
            for j in range(int(math.pow(2,2+int(i/2)))):
                t1 = j*angle
                t2 = t1+angle
                
                #Plots an arc for the inner wall
                if self.maze.initial_grid[i][j].walls["inner"] and i != 0:
                    self.ax.add_patch(Arc((0, 0), (i)*2, (i)*2, angle=0.0,
                                          theta1=t1/r_factor, theta2=t2/r_factor, edgecolor='k', lw=1.5))
                    
                #Plots an arc for the first outer wall
                if self.maze.initial_grid[i][j].walls["outer_1"]:
                    self.ax.add_patch(Arc((0, 0), (i+1)*2, (i+1)*2, angle=0.0,
                                          theta1=t1/r_factor, theta2=((t2/r_factor)+(t1/r_factor))/2, edgecolor='k', lw=1.5))
                #Plots an arc for the second outer wall
                if self.maze.initial_grid[i][j].walls["outer_2"]:
                    self.ax.add_patch(Arc((0, 0), (i+1)*2, (i+1)*2, angle=0.0,
                                          theta1=((t2/r_factor)+(t1/r_factor))/2, theta2=t2/r_factor, edgecolor='k', lw=1.5))
                    
                #Handles the plotting for the first layer of the maze
                if i ==0:
                    if self.maze.initial_grid[i][j].walls["right"]:
                        plt.plot([0, math.cos(t2)], [0, math.sin(t2)],'k')
                    if self.maze.initial_grid[i][j].walls["left"]:
                        plt.plot([0, math.cos(t1)], [0, math.sin(t1)],'k')
                    continue 
                    
                #Plots a line connecting the ends of both the arcs to the left
                if self.maze.initial_grid[i][j].walls["left"]:
                    plt.plot([(i+1)*math.cos(t2), i*math.cos(t2)], [(i+1)*math.sin(t2), i*math.sin(t2)],'k')
                    
                #Plots a line connecting the ends of both the arcs to the left
                if self.maze.initial_grid[i][j].walls["right"]:
                    
                    plt.plot([(i+1)*math.cos(t1), i*math.cos(t1)], [(i+1)*math.sin(t1), i*math.sin(t1)],'k')
                        