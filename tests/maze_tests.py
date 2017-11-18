import unittest
import maze as mazegen


def generate_maze():
    cols = 5
    rows = 5
    cell_size = 1
    return mazegen.Maze(rows, cols, cell_size)


class TestMaze(unittest.TestCase):
    def test_ctor(self):
        """Make sure that the constructor values are getting properly set."""
        cols = 5
        rows = 5
        cell_size = 1
        maze = mazegen.Maze(rows, cols, cell_size)

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
        self.assertGreater(len(grid), 0)
        self.assertEqual(len(grid[0]), maze.num_rows)

if (__name__ == "__main__"):
    unittest.main()