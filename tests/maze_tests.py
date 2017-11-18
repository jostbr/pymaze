from __future__ import absolute_import
import unittest
from src.maze import Maze


def generate_maze():
    # Used to generate a 5x5 maze for testing, Feel free to modify as needed

    cols = 5
    rows = 5
    cell_size = 1
    return Maze(rows, cols, cell_size)


class TestMaze(unittest.TestCase):
    def test_ctor(self):
        """Make sure that the constructor values are getting properly set."""
        cols = 5
        rows = 5
        cell_size = 1
        maze = Maze(rows, cols, cell_size)

        self.assertEqual(maze.num_cols, cols)
        self.assertEqual(maze.num_rows, rows)
        self.assertEqual(maze.cell_size, cell_size)
        self.assertEqual(maze.grid_size, rows*cols)
        self.assertEqual(maze.height, rows*cell_size)
        self.assertEqual(maze.width, cols*cell_size)

    def test_generate_grid(self):
        maze = generate_maze()
        grid = maze.generate_grid()

        self.assertEqual(len(grid), maze.num_cols)
        self.assertGreater(len(grid), 2)
        self.assertEqual(len(grid[0]), maze.num_rows)

if (__name__ == "__main__"):
    unittest.main()