
class Cell(object):
    """Class for representing a cell in a 2D grid."""
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.visited = False
        self.active = False
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}
        self.neighbours = list()

    #def compute_neighbours(self, row_limit, col_limit):
    #    def verify_neighbour(indices):
    #        if (indices[0] >= 0 and indices[0] <= row_limit and
    #            indices[1] >= 0 and indices[1] <= col_limit):
    #            self.neighbours.append(indices)
    #
    #    verify_neighbour((self.row-1, self.col))
    #    verify_neighbour((self.row, self.col+1))
    #    verify_neighbour((self.row+1, self.col))
    #    verify_neighbour((self.row, self.col-1))



    #def find_neighbours(self, cell_row, cell_col):
    #    """Function that finds all existing and unvisited neighbours of a cell in the
    #    grid. Return a list of tuples containing indices for the unvisited neighbours."""
    #    neighbours = list()
    #
    #    def check_neighbour(row, col):
    #        # Check that a neighbour exists and that it's not visisted before.
    #        if (row >= 0 and row < self.num_rows and col >= 0
    #            and col < self.num_cols and not self.grid[row][col].visited):
    #            neighbours.append((row, col))
    #
    #    check_neighbour(cell_row-1, cell_col)     # Top neighbour
    #    check_neighbour(cell_row, cell_col+1)     # Right neighbour
    #    check_neighbour(cell_row+1, cell_col)     # Bottom neighbour
    #    check_neighbour(cell_row, cell_col-1)     # Left neighbour
    #
    #    if (len(neighbours) > 0):
    #        return neighbours
    #    else:
    #        return None     # None if no unvisited neighbours found

    def remove_walls(self, neighbour_row, neighbour_col):
        """Function that removes walls between neighbour cell given by indices in grid."""
        if (self.row - neighbour_row == 1):
            self.walls["top"] = False
        elif (self.row - neighbour_row == -1):
            self.walls["bottom"] = False
        elif (self.col - neighbour_col == 1):
            self.walls["left"] = False
        elif (self.col - neighbour_col == -1):
            self.walls["right"] = False
