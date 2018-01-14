from __future__ import absolute_import
import unittest

from src.maze import Maze
from src.cell import Cell


def generate_maze():
    # Used to generate a 5x5 maze for testing, Feel free to modify as needed

    cols = 5
    rows = 5
    return Maze(rows, cols)


class TestMaze(unittest.TestCase):
    def test_ctor(self):
        """Make sure that the constructor values are getting properly set."""
        cols = 5
        rows = 5
        maze = Maze(rows, cols)

        self.assertEqual(maze.num_cols, cols)
        self.assertEqual(maze.num_rows, rows)
        self.assertEqual(maze.id, 0)
        self.assertEqual(maze.grid_size, rows*cols)

        id=33
        maze2 = Maze(rows, cols, id)
        self.assertEqual(maze2.num_cols, cols)
        self.assertEqual(maze2.num_rows, rows)
        self.assertEqual(maze2.id, id)
        self.assertEqual(maze2.grid_size, rows * cols)

    def test_generate_grid(self):
        maze = generate_maze()
        grid = maze.generate_grid()

        self.assertEqual(len(grid), maze.num_cols)
        self.assertGreater(len(grid), 2)
        self.assertEqual(len(grid[0]), maze.num_rows)

    def test_find_neighbors(self):
        maze = Maze(2, 2)
        neighbors = maze.find_neighbours(0, 1)
        self.assertIsNotNone(neighbors)


if __name__ == "__main__":
    unittest.main()