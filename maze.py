
import cell
import maze_viz
import random
import math
import copy
import time
import matplotlib.pyplot as plt
from matplotlib import animation

class Maze(object):
    """Class representing a maze; a 2D grid of Cell objects. Contains functions
    for generating randomly generating the maze as well as for solving the maze."""
    def __init__(self, num_rows, num_cols, cell_size):
        """Constructor function that iniates maze with key attributes and creates grid."""
        self.num_cols = num_cols
        self.num_rows = num_rows
        self.cell_size = cell_size
        self.grid_size = num_rows*num_cols
        self.height = num_rows*cell_size
        self.width = num_cols*cell_size
        self.init_grid = self.generate_grid()

    def generate_grid(self):
        """Function that creates a 2D grid of Cell objects to be the maze."""
        grid = list()

        for i in range(self.num_rows):
            grid.append(list())

            for j in range(self.num_cols):
                grid[i].append(cell.Cell(i, j))

        return grid

    def _find_neighbours(self, cell_row, cell_col):
        """Function that finds all existing and unvisited neighbours of a cell in the
        grid. Return a list of tuples containing indices for the unvisited neighbours."""
        neighbours = list()

        def check_neighbour(row, col):
            # Check that a neighbour exists and that it's not visisted before.
            if (row >= 0 and row < self.num_rows and col >= 0 and col < self.num_cols):
                neighbours.append((row, col))

        check_neighbour(cell_row-1, cell_col)     # Top neighbour
        check_neighbour(cell_row, cell_col+1)     # Right neighbour
        check_neighbour(cell_row+1, cell_col)     # Bottom neighbour
        check_neighbour(cell_row, cell_col-1)     # Left neighbour

        if (len(neighbours) > 0):
            return neighbours
        
        else:
            return None     # None if no unvisited neighbours found

    def _validate_neighbours_generate(self, neighbour_indices, grid):
        """Function that validates whether a neighbour is unvisited or not. When generating
        the maze, we only want to move to move to unvisited cells (unless we are backtracking)."""
        neigh_list = [n for n in neighbour_indices if not grid[n[0]][n[1]].visited]

        if (len(neigh_list) > 0):
            return neigh_list
        else:
            return None

    def _validate_neighbours_solve(self, neighbour_indices, grid, k, l, k_end, l_end, method = "fancy"):
        """Function that validates wheter a neighbour is unvisited or not and discards the
        neighbours that are inaccessible due to walls between them and the current cell. The
        function implements two methods for choosing next cell; one is 'brute-force' where one
        of the neighbours are chosen randomly. The other is 'fancy' where the next cell is chosen
        based on which neighbour that gives the shortest distance to the final destination."""

        if (method == "fancy"):
            neigh_list = list()
            min_dist_to_target = 100000

            for k_n, l_n in neighbour_indices:
                if (not grid[k_n][l_n].visited
                    and not grid[k][l].is_walls_between(grid[k_n][l_n])):
                    dist_to_target = math.sqrt((k_n - k_end)**2 + (l_n - l_end)**2)
                    
                    if (dist_to_target < min_dist_to_target):
                        min_dist_to_target = dist_to_target
                        min_neigh = (k_n, l_n)

            if ("min_neigh" in locals()):
                neigh_list.append(min_neigh)

        elif (method == "brute-force"):
            neigh_list = [n for n in neighbour_indices if not grid[n[0]][n[1]].visited
                and not grid[k][l].is_walls_between(grid[n[0]][n[1]])]

        if (len(neigh_list) > 0):
            return neigh_list
        else:
            return None

    def _pick_random_entry_exit(self, used_entry_exit = None):
        """Function that picks random coordinates along the maze boundary to represent either
        the entry or exit point of the maze. Makes sure they are not at the same place."""
        rng_entry_exit = used_entry_exit    # Initialize with used value

        # Try until unused location along bounday is found.
        while((rng_entry_exit == used_entry_exit)):
            rng_side = random.randint(0, 3)

            if (rng_side == 0):     # Top side
                rng_entry_exit = (0, random.randint(0, self.num_cols-1))

            elif (rng_side == 2):   # Right side
                rng_entry_exit = (self.num_rows-1, random.randint(0, self.num_cols-1))

            elif (rng_side == 1):   # Bottom side
                rng_entry_exit = (random.randint(0, self.num_rows-1), self.num_cols-1)

            elif (rng_side == 3):   # Left side
                rng_entry_exit = (random.randint(0, self.num_rows-1), 0)

        return rng_entry_exit       # Return entry/exit that is different from exit/entry

    def generate_maze(self, start_coor = (0, 0)):
        """Function that implements the depth-first recursive bactracker maze genrator
        algorithm. Hopfully will return a 2D grid of Cell objects that is the resulting maze."""
        grid = copy.deepcopy(self.init_grid)
        k_curr, l_curr = start_coor             # Where to start generating
        path = [(k_curr, l_curr)]               # To track path of solution
        grid[k_curr][l_curr].visited = True     # Set initial cell to visited
        visit_counter = 1                       # To count number of visited cells
        visited_cells = list()                  # Stack of visited cells for backtracking
        
        print("\nGenerating the maze...")
        time_start = time.clock()
        
        while (visit_counter < self.grid_size):     # While there are unvisited cells
            neighbour_indices = self._find_neighbours(k_curr, l_curr)    # Find neighbour indicies
            neighbour_indices = self._validate_neighbours_generate(neighbour_indices, grid)

            if (neighbour_indices is not None):   # If there are unvisited neighbour cells
                visited_cells.append((k_curr, l_curr))              # Add current cell to stack
                k_next, l_next = random.choice(neighbour_indices)     # Choose random neighbour
                grid[k_curr][l_curr].remove_walls(k_next, l_next)   # Remove walls between neighbours
                grid[k_next][l_next].remove_walls(k_curr, l_curr)   # Remove walls between neighbours                                
                grid[k_next][l_next].visited = True                 # Move to that neighbour
                k_curr = k_next
                l_curr = l_next
                path.append((k_curr, l_curr))   # Add coordinates to part of generation path
                visit_counter += 1

            elif (len(visited_cells) > 0):  # If there are no unvisited neighbour cells
                k_curr, l_curr = visited_cells.pop()      # Pop previous visited cell (backtracking)
                path.append((k_curr, l_curr))   # Add coordinates to part of generation path

        entry_indices = self._pick_random_entry_exit(None)     # Entry location cell of maze
        exit_indices = self._pick_random_entry_exit(entry_indices)      # Exit location cell of maze
        grid[entry_indices[0]][entry_indices[1]].set_as_entry_exit("entry",
            self.num_rows-1, self.num_cols-1)
        grid[exit_indices[0]][exit_indices[1]].set_as_entry_exit("exit",
            self.num_rows-1, self.num_cols-1)

        print("Number of moves performed: {}".format(len(path)))
        print("Execution time for algorithm: {:.4f}".format(time.clock() - time_start))

        return grid, path

    def solve_maze(self, grid, method = "fancy"):
        """Function that implements the depth-first recursive bactracker algorithm for
        solving the maze, i.e. starting at the entry point and searching for the exit.
        The main difference from the generator algorithm is that we can't go through
        walls and thus need to implement a proper path-finding algorithm."""

        # Locate start and end coordinate of maze and make sure all cells are unvisited
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                grid[i][j].visited = False      # Set all cells to unvisited

                if (grid[i][j].is_entry_exit == "entry"):
                    entry_indices = (i, j)

                elif (grid[i][j].is_entry_exit == "exit"):
                    exit_indices = (i, j)

        k_curr, l_curr = entry_indices          # Where to start generating
        path = list()                           # To track path of solution and backtracking cells
        grid[k_curr][l_curr].visited = True     # Set initial cell to visited
        visited_cells = list()                  # Stack of visited cells for backtracking

        print("\nSolving the maze...")
        time_start = time.clock()
        
        while ((k_curr, l_curr) != exit_indices):     # While there are unvisited cells
            neighbour_indices = self._find_neighbours(k_curr, l_curr)    # Find neighbour indicies
            neighbour_indices = self._validate_neighbours_solve(neighbour_indices, grid, k_curr,
                l_curr, exit_indices[0], exit_indices[1], method = "fancy")

            if (neighbour_indices is not None):   # If there are unvisited neighbour cells
                visited_cells.append((k_curr, l_curr))              # Add current cell to stack
                path.append(((k_curr, l_curr), False))  # Add coordinates to part of generation path
                k_next, l_next = random.choice(neighbour_indices)   # Choose random neighbour
                grid[k_next][l_next].visited = True                 # Move to that neighbour
                k_curr = k_next
                l_curr = l_next

            elif (len(visited_cells) > 0):  # If there are no unvisited neighbour cells
                path.append(((k_curr, l_curr), True))   # Add coordinates to part of generation path
                k_curr, l_curr = visited_cells.pop()    # Pop previous visited cell (backtracking)

        path.append(((k_curr, l_curr), False))  # Append final location to path
        print("Number of moves performed: {}".format(len(path)))
        print("Execution time for algorithm: {:.4f}".format(time.clock() - time_start))

        return path


if (__name__ == "__main__"):
    maze_generator = Maze(60, 60, 1)
    grid, path_gen = maze_generator.generate_maze((0, 0))
    #maze_viz.plot_maze(maze_generator, grid)
    #anim_generate = maze_viz.animate_maze_generate(maze_generator, path_gen)

    path_solve = maze_generator.solve_maze(grid, method = "fancy")
    anim_solve = maze_viz.animate_maze_solve(maze_generator, grid, path_solve, "anim_solve")

    #plt.show()