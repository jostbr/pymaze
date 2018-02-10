import random
import math
import time
from src.circle_cell import CircleCell
from src.maze import Maze
class Circle(Maze):
    
    def __init__(self, num_layers, id=0):
        self.num_layers = num_layers
        self.id = id
        self.grid_size = self.get_size()
        self.generate_grid()
        self.entry_coor = self._pick_random_entry_exit(None)
        self.exit_coor = self._pick_random_entry_exit(self.entry_coor)
        self.generation_path = []
        self.solution_path = None
        self.initial_grid = self.generate_grid()
        self.grid = self.initial_grid
        self.generate_maze((0, 0))
    
    def get_size(self):
        size = 0
        for i in range(self.num_layers):
            size += int(math.pow(2,int(i/2)+2))
        return(size)
    def generate_grid(self):
        """Function that creates a 2D grid of Cell objects. This can be thought of as a
        maze without any paths carved out

        Return:
            A list with Cell objects at each position

        """

        # Create an empty list
        grid = list()

        # Place a Cell object at each location in the grid
        for i in range(self.num_rows):
            grid.append(list())

            for j in range(int(math.pow(2,2+int(i/2)))):
                grid[i].append(CircleCell(i, j))

        return grid
    
    def _pick_random_entry_exit(self, used_entry_exit=None):
        """Function that picks random coordinates along the maze boundary to represent either
        the entry or exit point of the maze. Makes sure they are not at the same place.

        Args:
            used_entry_exit

        Return:

        """
        rng_entry_exit = used_entry_exit    # Initialize with used value
        boundary_points = int(math.pow(2,(int((self.num_rows-1)/2)+2)))
        # Try until unused location along boundary is found.
        while rng_entry_exit == used_entry_exit:
            rng_entry_exit = (self.num_rows-1,random.randint(0, boundary_points-1))
        return rng_entry_exit
    
    def find_neighbours(self, cell_row, cell_col):
        """Finds all existing and unvisited neighbours of a cell in the
        grid. Return a list of tuples containing indices for the unvisited neighbours.

        Args:
            cell_row (int):
            cell_col (int):

        Return:
            None: If there are no unvisited neighbors
            list: A list of neighbors that have not been visited
        """
        neighbours = list()
        def check_neighbour(row, col):
            # Check that a neighbour exists and that it's not visited before.
            if row >= 0 and row < self.num_rows:
                if col ==-1:
                    neighbours.append((row,int(math.pow(2,int(row/2)+2))-1))
                elif col == int(math.pow(2,int(row/2)+2)):
                    neighbours.append((row, 0))
                else:
                    neighbours.append((row,col))
        check_neighbour(cell_row, cell_col-1)     # Right neighbour
        check_neighbour(cell_row, cell_col+1)
        if cell_row%2 != 0:
            check_neighbour(cell_row-1, cell_col)     # inner neighbour
            check_neighbour(cell_row+1, (cell_col*2))     # outer neighbour-1
            check_neighbour(cell_row+1, (cell_col*2)+1)     # outer neighbour-2
        else:
            check_neighbour(cell_row-1, int(cell_col/2))     # inner neighbour
            check_neighbour(cell_row+1, cell_col)     # outer neighbour-1

        if len(neighbours) > 0:
            return neighbours

        else:
            return None     # None if no unvisited neighbours found
    
         