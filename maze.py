
import cell
import random
import copy
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

class Maze(object):
    """Class representing a maze; a 2D grid of Cell objects. Contains functions
    for generating randomly generating the maze as well as for solving the maze."""
    def __init__(self, num_rows, num_cols, cell_size, start_coor = (0, 0)):
        """Constructor function that iniates maze with key attributes and creates grid."""
        self.num_cols = num_cols
        self.num_rows = num_rows
        self.grid_size = num_rows*num_cols
        self.cell_size = cell_size
        self.start_row = start_coor[0]
        self.start_col = start_coor[1]
        self.grid = self.generate_grid()
        self.grid_list = [copy.deepcopy(self.grid)]

    def generate_grid(self):
        """Function that creates a 2D grid of Cell objects to be the maze."""
        grid = list()

        for i in range(self.num_rows):
            grid.append(list())

            for j in range(self.num_cols):
                grid[i].append(cell.Cell(i, j))

        return grid

    def find_neighbours(self, cell_row, cell_col):
        """Function that finds all existing and unvisited neighbours of a cell in the
        grid. Return a list of tuples containing indices for the unvisited neighbours."""
        neighbours = list()

        def check_neighbour(row, col):
            # Check that a neighbour exists and that it's not visisted before.
            if (row >= 0 and row < self.num_rows and col >= 0
                and col < self.num_cols and not self.grid[row][col].visited):
                neighbours.append((row, col))

        check_neighbour(cell_row-1, cell_col)     # Top neighbour
        check_neighbour(cell_row, cell_col+1)     # Right neighbour
        check_neighbour(cell_row+1, cell_col)     # Bottom neighbour
        check_neighbour(cell_row, cell_col-1)     # Left neighbour

        if (len(neighbours) > 0):
            return neighbours
        
        else:
            return None     # None if no unvisited neighbours found

    def generate_maze(self):
        """Function that implements the depth-first recursive bactracker maze genrator
        algorithm. Hopfully will return a 2D grid of Cell objects that is the resulting maze."""
        k_curr, l_curr = self.start_row, self.start_col     # Where to start generating
        self.grid[k_curr][l_curr].visited = True
        visit_counter = 1
        visited_cells = list()
        time_start = time.clock()
        
        while (visit_counter < self.grid_size):     # While there are unvisited cells
            neighbour_coors = self.find_neighbours(k_curr, l_curr)    # Find neighbour indicies

            if (neighbour_coors is not None):   # If there are unvisited neighbour cells
                visited_cells.append((k_curr, l_curr))              # Add current cell to stack
                k_next, l_next = random.choice(neighbour_coors)     # Choose random neighbour
                self.grid[k_curr][l_curr].remove_walls(k_next, l_next)   # Remove walls between neighbours
                self.grid[k_next][l_next].remove_walls(k_curr, l_curr)   # Remove walls between neighbours
                self.grid[k_next][l_next].visited = True            # Move to that neighbour
                visit_counter += 1
                k_curr = k_next
                l_curr = l_next

            elif (len(visited_cells) > 0):  # If there are no unvisited neighbour cells
                k_curr, l_curr = visited_cells.pop()      # Pop prevoius visited cell (backtracking)

            self.grid[k_curr][l_curr].active = True
            self.grid_list.append(copy.deepcopy(self.grid))
            self.grid[k_curr][l_curr].active = False
        
        print("Execution time for algorithm: {:.4f}".format(time.clock() - time_start))
        
        return self.grid

    def plot_grid(self):
        fig, ax = plt.subplots(figsize = (7, 7*self.num_rows/self.num_cols))
        
        lines = list()

        for i in range(self.num_rows):
            for j in range(self.num_cols):
                if (self.grid[i][j].walls["top"] == True):
                    lines.append(ax.plot([j*self.cell_size, (j+1)*self.cell_size],
                        [i*self.cell_size, i*self.cell_size], color = "k"))
                if (self.grid[i][j].walls["right"] == True):
                    lines.append(ax.plot([(j+1)*self.cell_size, (j+1)*self.cell_size],
                        [i*self.cell_size, (i+1)*self.cell_size], color = "k"))
                if (self.grid[i][j].walls["bottom"] == True):
                    lines.append(ax.plot([(j+1)*self.cell_size, j*self.cell_size],
                        [(i+1)*self.cell_size, (i+1)*self.cell_size], color = "k"))
                if (self.grid[i][j].walls["left"] == True):
                    lines.append(ax.plot([j*self.cell_size, j*self.cell_size],
                        [(i+1)*self.cell_size, i*self.cell_size], color = "k"))

    def animate_maze_generation(self):
        #for i in range(len(self.grid_list)):
        #    self.print_grid(self.grid_list[i])

        fig = plt.figure(figsize = (8, 8))
        ax = plt.axes(xlim = (-1, self.num_cols*self.cell_size+1),
            ylim = (-1, self.num_cols*self.cell_size+1))
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)

        lines = dict()

        indicator = plt.Rectangle((self.start_row*self.cell_size,
            self.start_col*self.cell_size), self.cell_size,
            self.cell_size, fc = "purple", alpha = 0.5)
        ax.add_patch(indicator)

        for i in range(self.num_rows):
            for j in range(self.num_cols):
                for wall_key in self.grid_list[0][i][j].walls.keys():
                    lines["{},{}: {}".format(i, j, wall_key)] = ax.plot([], [],
                        linewidth = 2, color = "k")[0]

        def init():
            """Function that initializes the animation process by setting up artists."""
            for i in range(self.num_rows):
                for j in range(self.num_cols):
                    if (self.grid_list[0][i][j].active == True):
                        indicator.set_xy((j*self.cell_size, i*self.cell_size))

                    lines["{},{}: top".format(i,j)].set_data([j*self.cell_size, (j+1)*self.cell_size],
                        [i*self.cell_size, i*self.cell_size])
                    lines["{},{}: right".format(i,j)].set_data([(j+1)*self.cell_size, (j+1)*self.cell_size],
                        [i*self.cell_size, (i+1)*self.cell_size])
                    lines["{},{}: bottom".format(i,j)].set_data([(j+1)*self.cell_size, j*self.cell_size],
                        [(i+1)*self.cell_size, (i+1)*self.cell_size])
                    lines["{},{}: left".format(i,j)].set_data([j*self.cell_size, j*self.cell_size],
                        [(i+1)*self.cell_size, i*self.cell_size])

            return []

        def animate(frame):
            """Function to supervise animation of all objects."""
            for i in range(self.num_rows):
                for j in range(self.num_cols):
                    current_cell = self.grid_list[frame][i][j]
                    animate_walls(frame, current_cell)
                    animate_indicator(frame, current_cell)

            ax.set_title("Step: {}".format(frame + 1))
            return []

        def animate_walls(frame, current_cell):
            """Function to animate walls between cells as the search goes on."""
            for wall_key in current_cell.walls.keys():
                if (current_cell.walls[wall_key] == False):
                    lines["{},{}: {}".format(current_cell.row,
                        current_cell.col, wall_key)].set_visible(False)

            return lines["{},{}: {}".format(current_cell.row, current_cell.col, wall_key)]

        def animate_indicator(frame, current_cell):
            """Function to animate where the current search is happening."""
            if (current_cell.active == True):
                indicator.set_xy((current_cell.col*self.cell_size,
                    current_cell.row*self.cell_size))

            return indicator

        anim = animation.FuncAnimation(fig, animate, init_func = init, frames = len(self.grid_list),
            interval = 50, blit = True, repeat = False)
        return anim

    def plot_maze(self):
        flat_grid = [item.visited for sublist in self.grid for item in sublist]
        CS = plt.imshow(np.array(flat_grid).reshape((self.num_rows, self.num_cols)))
        plt.show()

    def print_grid(self, g):
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                print(g[i][j].visited, "", end = "")

            print()
        print()



if (__name__ == "__main__"):
    maze_generator = Maze(20, 20, 1, (4, 4))
    grid = maze_generator.generate_maze()
    #maze_generator.plot_grid()
    anim = maze_generator.animate_maze_generation()

    plt.show()