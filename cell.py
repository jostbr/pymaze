
class Cell(object):
    """Class for representing a cell in a 2D grid."""
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.visited = False
        self.active = False
        self.is_start = False
        self.is_end = False
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}
        self.neighbours = list()

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

    def set_as_entry_exit(self, row_limit, col_limit):
        """Function that sets the cell as an entry/exit cell by
        disabling the outer boundayr wall."""
        if (self.row == 0):
            self.walls["top"] = False
        elif (self.row == row_limit):
            self.walls["bottom"] = False
        elif (self.col == 0):
            self.walls["left"] = False
        elif (self.col == col_limit):
            self.walls["right"] = False
