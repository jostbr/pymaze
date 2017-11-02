
import cell
import random
import copy
import time
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
        self.height = num_rows*cell_size
        self.width = num_cols*cell_size
        self.start_row = start_coor[0]
        self.start_col = start_coor[1]
        self.loop_count = 0
        self.grid = self.generate_grid()
        self.init_grid = copy.deepcopy(self.grid)
        self.path = [(start_coor)]  # To track path of solution

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
                self.path.append((k_curr, l_curr))

            elif (len(visited_cells) > 0):  # If there are no unvisited neighbour cells
                k_curr, l_curr = visited_cells.pop()      # Pop previous visited cell (backtracking)
                self.path.append((k_curr, l_curr))

            self.loop_count += 1

        print("Number of moves performed: {}".format(len(self.path)))
        print("Execution time for algorithm: {:.4f}".format(time.clock() - time_start))
        return self.grid

    def pick_random_entry_exit(self):
        """Function that picks random coordinates along the maze boundary
        to represent either the entry or exit point of the maze."""
        rng_side = random.randint(0, 3)

        if (rng_side == 0):
            rng_entry_exit = (0, random.randint(0, self.num_cols-1))
        elif (rng_side == 2):
            rng_entry_exit = (self.num_rows-1, random.randint(0, self.num_cols-1))
        elif (rng_side == 1):
            rng_entry_exit = (random.randint(0, self.num_rows-1), self.num_cols-1)
        elif (rng_side == 3):
            rng_entry_exit = (random.randint(0, self.num_rows-1), 0)

        return rng_entry_exit

    def plot_maze(self):
        """Function that plots the generated mase. Also with added entry and exit point."""
        fig, ax = plt.subplots(figsize = (7, 7*self.num_rows/self.num_cols))
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)
        lines = list()

        entry_coor = self.pick_random_entry_exit()  # Entry cell of maze
        exit_coor = self.pick_random_entry_exit()    # Exit cell of maze

        ax.text(entry_coor[1], entry_coor[0], "ENTRY", weight = "bold", va = "bottom")
        ax.text(exit_coor[1], exit_coor[0], "EXIT", weight = "bold")

        for i in range(self.num_rows):
            for j in range(self.num_cols):
                if (entry_coor == (i, j)):
                    self.grid[i][j].set_as_entry_exit(self.num_rows-1, self.num_cols-1)
                
                if (exit_coor == (i, j)):
                    self.grid[i][j].set_as_entry_exit(self.num_rows-1, self.num_cols-1)

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

    def animate_maze(self):
        fig = plt.figure(figsize = (7, 7*self.num_rows/self.num_cols))
        ax = plt.axes(xlim = (-1, self.width+1), ylim = (-1, self.height+1))
        #ax.set_aspect("equal")
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)

        lines = dict()

        indicator = plt.Rectangle((self.start_row*self.cell_size,
            self.start_col*self.cell_size), self.cell_size,
            self.cell_size, fc = "purple", alpha = 0.5)
        ax.add_patch(indicator)

        # Only need to plot right and bottom wall for each cell since walls overlap
        color_walls = "k"
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                lines["{},{}: right".format(i, j)] = ax.plot([], [],
                    linewidth = 2, color = color_walls)[0]
                lines["{},{}: bottom".format(i, j)] = ax.plot([], [],
                    linewidth = 2, color = color_walls)[0]

        # Plotting boundaries of maze
        color_boundary = "k"
        ax.plot([0, self.width], [self.height,self.height], linewidth = 2, color = color_boundary)
        ax.plot([self.width, self.width], [self.height, 0], linewidth = 2, color = color_boundary)
        ax.plot([self.width, 0], [0, 0], linewidth = 2, color = color_boundary)
        ax.plot([0, 0], [0, self.height], linewidth = 2, color = color_boundary)

        def init():
            """Function that initializes animation process by setting up artists and drawing grid."""
            for i in range(self.num_rows):
                for j in range(self.num_cols):
                    #lines["{},{}: top".format(i,j)].set_data([j*self.cell_size, (j+1)*self.cell_size],
                    #    [i*self.cell_size, i*self.cell_size])
                    lines["{},{}: right".format(i,j)].set_data([(j+1)*self.cell_size, (j+1)*self.cell_size],
                        [i*self.cell_size, (i+1)*self.cell_size])
                    lines["{},{}: bottom".format(i,j)].set_data([(j+1)*self.cell_size, j*self.cell_size],
                        [(i+1)*self.cell_size, (i+1)*self.cell_size])
                    #lines["{},{}: left".format(i,j)].set_data([j*self.cell_size, j*self.cell_size],
                    #    [(i+1)*self.cell_size, i*self.cell_size])

            indicator.set_xy((self.path[0][1]*self.cell_size, self.path[0][0]*self.cell_size))
            
            return []

        def animate(frame):
            """Function to supervise animation of all objects."""
            animate_walls(frame)
            animate_indicator(frame+1)
            ax.set_title("Step: {}".format(frame + 1), fontname = "serif", fontsize = 19)
            return []

        def animate_walls(frame):
            if (frame < len(self.path) - 1):
                self.init_grid[self.path[frame][0]][self.path[frame][1]].remove_walls(
                    self.path[frame+1][0], self.path[frame+1][1])   # Wall between curr and neigh
                self.init_grid[self.path[frame+1][0]][self.path[frame+1][1]].remove_walls(
                    self.path[frame][0], self.path[frame][1])   # Wall between neigh and curr

                current_cell = self.init_grid[self.path[frame][0]][self.path[frame][1]]
                next_cell = self.init_grid[self.path[frame+1][0]][self.path[frame+1][1]]

                """Function to animate walls between cells as the search goes on."""
                for wall_key in ["right", "bottom"]:    # Only need to draw two of the four walls (overlap)
                    if (current_cell.walls[wall_key] == False):
                        lines["{},{}: {}".format(current_cell.row,
                            current_cell.col, wall_key)].set_visible(False)
                    if (next_cell.walls[wall_key] == False):
                        lines["{},{}: {}".format(next_cell.row,
                            next_cell.col, wall_key)].set_visible(False)

                return []

            else:
                return None

        def animate_indicator(frame):
            """Function to animate where the current search is happening."""
            if (frame < len(self.path)):
                indicator.set_xy((self.path[frame][1]*self.cell_size, self.path[frame][0]*self.cell_size))

            return []

        anim = animation.FuncAnimation(fig, animate, init_func = init, frames = len(self.path),
            interval = 100, blit = True, repeat = False)
        #mpeg_writer = animation.FFMpegWriter(fps = 24, bitrate = 1000,
        #    codec = "libx264", extra_args = ["-pix_fmt", "yuv420p"])
        #anim.save("{}x{}.mp4".format(self.num_rows, self.num_cols), writer = mpeg_writer)
        return anim

    def print_grid(self, g):
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                print(g[i][j].visited, "", end = "")

            print()
        print()



if (__name__ == "__main__"):
    maze_generator = Maze(20, 20, 1, (0, 0))
    grid = maze_generator.generate_maze()
    maze_generator.plot_maze()
    #anim = maze_generator.animate_maze()

    plt.show()