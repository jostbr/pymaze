
class Cell(object):
    """Class for representing a cell in a 2D grid.

        Attributes:
            row (int): The row that this cell belongs to
            col (int): The column that this cell belongs to
            visited (bool): True if this cell has been visited by an algorithm
            active (bool):
            is_entry_exit (bool): True when the cell is the beginning or end of the maze
            walls (list):
            neighbours (list):
    """
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.visited = False
        self.active = False
        self.is_entry_exit = None
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}
        self.neighbours = list()

    def is_walls_between(self, neighbour):
        """Function that checks if there are walls between self and a neighbour cell.
        Returns true if there are walls between. Otherwise returns False.

        Args:
            neighbour The cell to check between

        Return:
            True: If there are walls in between self and neighbor
            False: If there are no walls in between the neighbors and self

        """
        if self.row - neighbour.row == 1 and self.walls["top"] and neighbour.walls["bottom"]:
            return True
        elif self.row - neighbour.row == -1 and self.walls["bottom"] and neighbour.walls["top"]:
            return True
        elif self.col - neighbour.col == 1 and self.walls["left"] and neighbour.walls["right"]:
            return True
        elif self.col - neighbour.col == -1 and self.walls["right"] and neighbour.walls["left"]:
            return True

        return False

    def remove_walls(self, neighbour_row, neighbour_col):
        """Function that removes walls between neighbour cell given by indices in grid.

            Args:
                neighbour_row (int):
                neighbour_col (int):

            Return:
                True: If the operation was a success
                False: If the operation failed

        """
        if self.row - neighbour_row == 1:
            self.walls["top"] = False
            return True, ""
        elif self.row - neighbour_row == -1:
            self.walls["bottom"] = False
            return True, ""
        elif self.col - neighbour_col == 1:
            self.walls["left"] = False
            return True, ""
        elif self.col - neighbour_col == -1:
            self.walls["right"] = False
            return True, ""
        return False

    def set_as_entry_exit(self, entry_exit, row_limit, col_limit):
        """Function that sets the cell as an entry/exit cell by
        disabling the outer boundary wall.
        First, we check if the entrance/exit is on the top row. Next, we check if it should
        be on the bottom row. Finally, we check if it is on the left wall or the bottom row.

        Args:
            entry_exit: True to set this cell as an exit/entry. False to remove it as one
            row_limit:
            col_limit:
        """

        if self.row == 0:
            self.walls["top"] = False
        elif self.row == row_limit:
            self.walls["bottom"] = False
        elif self.col == 0:
            self.walls["left"] = False
        elif self.col == col_limit:
            self.walls["right"] = False

        self.is_entry_exit = entry_exit

class CircleCell(Cell):
    """Child class of Cell to represent cells in a circular 2D grid.

        Attributes:
            row (int): The circular layer that this cell belongs to
            col (int): The column within a layer that the cell belongs to
            visited (bool): True if this cell has been visited by an algorithm
            active (bool):
            is_entry_exit (bool): True when the cell is the beginning or end of the maze
            walls (list):
            neighbours (list):
    """
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.visited = False
        self.active = False
        self.is_entry_exit = None
        self.walls = {"inner": True, "right": True, "outer_1": True,"outer_2":True,"left": True}
        self.neighbours = list()
        
    def get_walls(self,cell_1_row,cell_1_col,cell_2_row,cell_2_col):
        """Function that returns the walls of each of the two cells that are in contact.

            Args:
                cell_1_row (int) , cell_1_col (int): Co-ordinates of cell-1
                cell_2_row (int) , cell_2_col (int): Co-ordinates of cell-2

            Return:
                Tuple: (wall_1,wall_2): wall_1 and wall_2 are corresponding 
                                        walls of cell-1 and cell-2 that are in contact

        """
        wall_1 = None
        wall_2 = None
        if cell_1_row - cell_2_row ==1:
            wall_1 = (("inner",))
            if cell_1_row%2 == 0:
                if cell_1_col%2 == 0:
                    wall_2 = (("outer_1",))
                else:
                    wall_2 = (("outer_2",))
            else:
                wall_2 = (("outer_1","outer_2"))
        elif cell_1_row - cell_2_row == -1:
            wall_2 = (("inner"))
            if cell_2_row%2 == 0:
                if cell_2_col%2 == 0:
                    wall_1 = (("outer_1",))
                else:
                    wall_1 = (("outer_2",)) 
            else:
                wall_1 = (("outer_1","outer_2"))
        elif (cell_1_col - cell_2_col == 1) or ((cell_1_col - cell_2_col) < -1):
            wall_1 = (("right",))
            wall_2 = (("left",))
        elif (cell_1_col - cell_2_col == -1) or ((cell_1_col - cell_2_col) > 1):
            wall_1 = (("left",))
            wall_2 = (("right",))
        return((wall_1,wall_2))
                
    def is_walls_between(self, neighbour):
        """Function that checks if there are walls between self and a neighbour cell.
        Returns true if there are walls between. Otherwise returns False.

        Args:
            neighbour The cell to check between

        Return:
            True: If there are walls in between self and neighbor
            False: If there are no walls in between the neighbors and self

        """
        walls = self.get_walls(self.row,self.col,neighbour.row,neighbour.col)
        wall_status = True
        for wall_1 in walls[0]:
            if not self.walls[wall_1]:
                wall_status = False
        for wall_2 in walls[1]:
            if not neighbour.walls[wall_2]:
                wall_status = False
        return wall_status

    def remove_walls(self, neighbour_row, neighbour_col):
        """Function that removes walls between neighbour cell given by indices in grid.

            Args:
                neighbour_row (int):
                neighbour_col (int):

            Return:
                True: If the operation was a success
                False: If the operation failed

        """
        walls = self.get_walls(self.row,self.col,neighbour_row,neighbour_col)
        for wall in walls[0]:
            self.walls[wall] = False
        return True, ""

    def set_as_entry_exit(self, entry_exit, row_limit, col_limit):
        """Function that sets the cell as an entry/exit cell by
        disabling the outer boundary wall.
        Args:
            entry_exit: True to set this cell as an exit/entry. False to remove it as one
            row_limit:
            col_limit:
        """

        self.walls['outer_1'] = False
        self.walls['outer_2'] = False
        self.is_entry_exit = entry_exit