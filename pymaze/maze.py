import random
import math
from .cell import Cell
from .algorithm import depth_first_recursive_backtracker, binary_tree


class Maze(object):
    """Class representing a maze; a 2D grid of Cell objects. Contains functions
    for generating randomly generating the maze as well as for solving the maze.

    Attributes:
        num_cols (int): The height of the maze, in Cells
        num_rows (int): The width of the maze, in Cells
        id (int): A unique identifier for the maze
        grid_size (int): The area of the maze, also the total number of Cells in the maze
        entry_coor Entry location cell of maze
        exit_coor Exit location cell of maze
        generation_path : The path that was taken when generating the maze
        solution_path : The path that was taken by a solver when solving the maze
        initial_grid (list):
        grid (list): A copy of initial_grid (possible this is un-needed)
    """

    def __init__(self, num_rows, num_cols, id=0, algorithm="dfs_backtrack"):
        """Creates a gird of Cell objects that are neighbors to each other.

        Args:
                num_rows (int): The width of the maze, in cells
                num_cols (int): The height of the maze in cells
                id (id): An unique identifier

        """
        self.num_cols = num_cols
        self.num_rows = num_rows
        self.id = id
        self.grid_size = num_rows * num_cols
        self.entry_coor = self._pick_random_entry_exit(None)
        self.exit_coor = self._pick_random_entry_exit(self.entry_coor)
        self.generation_path = []
        self.solution_path = None
        self.initial_grid = self.generate_grid()
        self.grid = self.initial_grid
        self.generate_maze(algorithm, (0, 0))

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

            for j in range(self.num_cols):
                grid[i].append(Cell(i, j))

        return grid

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
            if (
                row >= 0
                and row < self.num_rows
                and col >= 0
                and col < self.num_cols
            ):
                neighbours.append((row, col))

        check_neighbour(cell_row - 1, cell_col)  # Top neighbour
        check_neighbour(cell_row, cell_col + 1)  # Right neighbour
        check_neighbour(cell_row + 1, cell_col)  # Bottom neighbour
        check_neighbour(cell_row, cell_col - 1)  # Left neighbour

        if len(neighbours) > 0:
            return neighbours

        else:
            return None  # None if no unvisited neighbours found

    def _validate_neighbours_generate(self, neighbour_indices):
        """Function that validates whether a neighbour is unvisited or not. When generating
        the maze, we only want to move to move to unvisited cells (unless we are backtracking).

        Args:
            neighbour_indices:

        Return:
            True: If the neighbor has been visited
            False: If the neighbor has not been visited

        """

        neigh_list = [
            n for n in neighbour_indices if not self.grid[n[0]][n[1]].visited
        ]

        if len(neigh_list) > 0:
            return neigh_list
        else:
            return None

    def validate_neighbours_solve(
        self, neighbour_indices, k, l, k_end, l_end, method="fancy"
    ):
        """Function that validates whether a neighbour is unvisited or not and discards the
        neighbours that are inaccessible due to walls between them and the current cell. The
        function implements two methods for choosing next cell; one is 'brute-force' where one
        of the neighbours are chosen randomly. The other is 'fancy' where the next cell is chosen
        based on which neighbour that gives the shortest distance to the final destination.

        Args:
            neighbour_indices
            k
            l
            k_end
            l_end
            method

        Return:


        """
        if method == "fancy":
            neigh_list = list()
            min_dist_to_target = 100000

            for k_n, l_n in neighbour_indices:
                if not self.grid[k_n][l_n].visited and not self.grid[k][
                    l
                ].is_walls_between(self.grid[k_n][l_n]):
                    dist_to_target = math.sqrt(
                        (k_n - k_end) ** 2 + (l_n - l_end) ** 2
                    )

                    if dist_to_target < min_dist_to_target:
                        min_dist_to_target = dist_to_target
                        min_neigh = (k_n, l_n)

            if "min_neigh" in locals():
                neigh_list.append(min_neigh)

        elif method == "brute-force":
            neigh_list = [
                n
                for n in neighbour_indices
                if not self.grid[n[0]][n[1]].visited
                and not self.grid[k][l].is_walls_between(
                    self.grid[n[0]][n[1]]
                )
            ]

        if len(neigh_list) > 0:
            return neigh_list
        else:
            return None

    def _pick_random_entry_exit(self, used_entry_exit=None):
        """Function that picks random coordinates along the maze boundary to represent either
        the entry or exit point of the maze. Makes sure they are not at the same place.

        Args:
            used_entry_exit

        Return:

        """
        rng_entry_exit = used_entry_exit  # Initialize with used value

        # Try until unused location along boundary is found.
        while rng_entry_exit == used_entry_exit:
            rng_side = random.randint(0, 3)

            if rng_side == 0:  # Top side
                rng_entry_exit = (0, random.randint(0, self.num_cols - 1))

            elif rng_side == 2:  # Right side
                rng_entry_exit = (
                    self.num_rows - 1,
                    random.randint(0, self.num_cols - 1),
                )

            elif rng_side == 1:  # Bottom side
                rng_entry_exit = (
                    random.randint(0, self.num_rows - 1),
                    self.num_cols - 1,
                )

            elif rng_side == 3:  # Left side
                rng_entry_exit = (random.randint(0, self.num_rows - 1), 0)

        return rng_entry_exit  # Return entry/exit that is different from exit/entry

    def generate_maze(self, algorithm, start_coor=(0, 0)):
        """This takes the internal grid object and removes walls between cells using the
        depth-first recursive backtracker algorithm.

        Args:
            start_coor: The starting point for the algorithm

        """

        if algorithm == "dfs_backtrack":
            depth_first_recursive_backtracker(self, start_coor)
        elif algorithm == "bin_tree":
            binary_tree(self, start_coor)
