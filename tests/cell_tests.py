import unittest
import cell as Cell


class test_cell(unittest.TestCase):
    def test_ctor(self):
        """Make sure that the constructor values are getting properly set."""

        cell = Cell.Cell(2, 2)
        self.assertEqual(cell.row, 2)
        self.assertEqual(cell.col, 2)
        self.assertEqual(cell.visited, False)
        self.assertEqual(cell.active, False)
        self.assertEqual(cell.is_entry_exit, None)
        self.assertEqual(cell.walls, {"top": True, "right": True, "bottom": True, "left": True})
        self.assertEqual(cell.neighbours, list())

    def test_entry_exit(self):
        """Test the Cell::entry_exit method"""

        # Check if the entrance/exit is on the top row.
        cell = Cell.Cell(0, 1)
        cell.set_as_entry_exit(True, 3, 3)
        self.assertEqual(cell.is_entry_exit, True)
        self.assertEqual(cell.walls["top"], False)

        cell.set_as_entry_exit(False, 1, 0)
        self.assertEqual(cell.is_entry_exit, False)
        self.assertEqual(cell.walls["top"], False)

        # Check if the entrance/exit is on the bottom row.
        cell = Cell.Cell(1, 0)
        cell.set_as_entry_exit(True, 1, 0)
        self.assertEqual(cell.walls["bottom"], False)
        self.assertEqual(cell.is_entry_exit, True)

        # Check if the entrance/exit is on the left wall.
        cell = Cell.Cell(2, 0)
        cell.set_as_entry_exit(True, 3, 1)
        self.assertEqual(cell.walls["left"], False)
        cell.set_as_entry_exit(True, 1, 1)

        # Check if the entrance/exit is on the right side wall.
        cell = Cell.Cell(2, 2)
        cell.set_as_entry_exit(True, 2, 2)
        self.assertEqual(cell.walls["right"], False)

    def test_remove_walls(self):
        """Test the Cell::remove_walls method"""
        # Remove the cell to the right
        cell = Cell.Cell(0, 0);
        cell.remove_walls(0,1)
        self.assertEqual(cell.walls["right"], False)

        # Remove the cell to the left
        cell = Cell.Cell(0, 1)
        cell.remove_walls(1, 0)
        self.assertEqual(cell.walls["left"], False)

        # Remove the cell above
        cell = Cell.Cell(1, 1)
        cell.remove_walls(0, 1)
        self.assertEqual(cell.walls["top"], False)

        # Remove the cell below
        cell = Cell.Cell(1, 1)
        cell.remove_walls(2, 1)
        self.assertEqual(cell.walls["bottom"], False)

    def test_is_walls_between(self):
        """Test the Cell::is_walls_between method

            Note that cells are constructed with neighbors on each side.
            We'll need to remove some walls to get full coverage.
        """

        # We should have walls on all sides of a new cell
        cell = Cell.Cell (0, 0);
        self.assertEqual(cell.walls, {"top": True, "right": True, "bottom": True, "left": True})

        # Remove the wall to the right
        cell2 = Cell.Cell(1, 0);
        cell2.remove_walls(1, 2)
        self.assertEqual(cell.walls, {"top": True, "right": False, "bottom": True, "left": True})

        # Remove the wall to the left
        cell3 = Cell.Cell(0, 2);
        cell3.remove_walls(0, 1)
        self.assertEqual(cell.walls, {"top": True, "right": True, "bottom": True, "left": False})

        # Remove the wall on the top
        cell4 = Cell.Cell(1, 2);
        cell4.remove_walls(0, 2)
        self.assertEqual(cell.walls, {"top": False, "right": True, "bottom": True, "left": True})

        # Remove the wall on the bottom
        cell5 = Cell.Cell(2, 2);
        cell5.remove_walls(3, 2)
        self.assertEqual(cell.walls, {"top": True, "right": True, "bottom": False, "left": True})


if (__name__ == "__main__"):
    unittest.main()