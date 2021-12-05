import unittest
from pymaze.cell import Cell


class TestCell(unittest.TestCase):
    def test_ctor(self):
        """Make sure that the constructor values are getting properly set."""

        cell = Cell(2, 2)
        self.assertEqual(cell.row, 2)
        self.assertEqual(cell.col, 2)
        self.assertEqual(cell.visited, False)
        self.assertEqual(cell.active, False)
        self.assertEqual(cell.is_entry_exit, None)
        self.assertEqual(
            cell.walls, {"top": True, "right": True, "bottom": True, "left": True}
        )
        self.assertEqual(cell.neighbours, list())

    def test_entry_exit(self):
        """Test the Cell::entry_exit method"""

        # Check if the entrance/exit is on the top row.
        cell = Cell(0, 1)
        cell.set_as_entry_exit(True, 3, 3)
        self.assertEqual(cell.is_entry_exit, True)
        self.assertEqual(cell.walls["top"], False)

        cell.set_as_entry_exit(False, 1, 0)
        self.assertEqual(cell.is_entry_exit, False)
        self.assertEqual(cell.walls["top"], False)

        # Check if the entrance/exit is on the bottom row.
        cell = Cell(1, 0)
        cell.set_as_entry_exit(True, 1, 0)
        self.assertEqual(cell.walls["bottom"], False)
        self.assertEqual(cell.is_entry_exit, True)

        # Check if the entrance/exit is on the left wall.
        cell = Cell(2, 0)
        cell.set_as_entry_exit(True, 3, 1)
        self.assertEqual(cell.walls["left"], False)
        cell.set_as_entry_exit(True, 1, 1)

        # Check if the entrance/exit is on the right side wall.
        cell = Cell(3, 2)
        cell.set_as_entry_exit(True, 2, 2)
        self.assertEqual(cell.walls["right"], False)

        # Check if we can make the exit on the right wall in a corner
        cell = Cell(2, 2)
        cell.set_as_entry_exit(True, 2, 2)
        self.assertEqual(cell.walls["right"], True)

    def test_remove_walls(self):
        """Test the Cell::remove_walls method"""
        # Remove the cell to the right
        cell = Cell(0, 0)
        cell.remove_walls(0, 1)
        self.assertEqual(cell.walls["right"], False)

        # Remove the cell to the left
        cell = Cell(0, 1)
        cell.remove_walls(0, 0)
        self.assertEqual(cell.walls["left"], False)

        # Remove the cell above
        cell = Cell(1, 1)
        cell.remove_walls(0, 1)
        self.assertEqual(cell.walls["top"], False)

        # Remove the cell below
        cell = Cell(1, 1)
        cell.remove_walls(2, 1)
        self.assertEqual(cell.walls["bottom"], False)

    def test_is_walls_between(self):
        """Test the Cell::is_walls_between method

        Note that cells are constructed with neighbors on each side.
        We'll need to remove some walls to get full coverage.
        """
        # Create a base cell for which we will be testing whether walls exist
        cell = Cell(1, 1)

        # Create a cell appearing to the top of this cell
        cell_top = Cell(0, 1)
        # Create a cell appearing to the right of this cell
        cell_right = Cell(1, 2)
        # Create a cell appearing to the bottom of this cell
        cell_bottom = Cell(2, 1)
        # Create a cell appearing to the left of this cell
        cell_left = Cell(1, 0)

        # check for walls between all these cells
        self.assertEqual(cell.is_walls_between(cell_top), True)
        self.assertEqual(cell.is_walls_between(cell_right), True)
        self.assertEqual(cell.is_walls_between(cell_bottom), True)
        self.assertEqual(cell.is_walls_between(cell_left), True)

        # remove top wall of 'cell' and bottom wall of 'cell_top'
        cell.remove_walls(0, 1)
        cell_top.remove_walls(1, 1)

        # check that there are no walls between these cells
        self.assertEqual(cell.is_walls_between(cell_top), False)


if __name__ == "__main__":
    unittest.main()
