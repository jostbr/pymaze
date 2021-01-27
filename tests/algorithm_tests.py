
# test no cell has a wall on all four walls
import unittest

# import all algorithms present in algorithm.py
from src.algorithm import *
from src.maze import Maze

def create_maze(algorithm):
    rows, cols = (5,5)
    return Maze(rows, cols, algorithm = algorithm)

class TestAlgorithm(unittest.TestCase):
    def test_NonEmptyPath(self):
        """Test to check that generation path for a maze is not an empty list"""
        # repeat the following for all algorithms developed in algorithm.py
        for algorithm in algorithm_list:
            # generate a maze using this algorithm
            maze = create_maze( algorithm )
            # create message to display when test fails
            err_msg = f'Algorithm {algorithm} generated empty path'
            # assert path is non empty list
            self.assertNotEqual( maze.generation_path, list(), msg = err_msg)

    def test_MazeHasEntryExit(self):
        """Test to check that entry and exit cells have been properly marked"""
        # repeat the following for all algorithms
        for algorithm in algorithm_list:
            # generate a maze using the algorithm
            maze = create_maze( algorithm )
            # create message to display when test fails
            err_msg = f'Algorithm {algorithm} did not generate entry_exit cells'

            # get the cell that has been set as entry point
            entry_cell = maze.grid[maze.entry_coor[0]][maze.entry_coor[1]]
            # check that the cell has been marked as an entry cell
            self.assertIsNotNone( entry_cell.is_entry_exit, msg = err_msg )

            # get the cell that has been set as exit point
            exit_cell = maze.grid[maze.exit_coor[0]][maze.exit_coor[1]]
            # check that the cell has been marked as an exit cell
            self.assertIsNotNone( entry_cell.is_entry_exit ,msg = err_msg )

    def test_AllCellsUnvisited(self):
        """Test to check that after maze generation all cells have been
        marked as unvisited."""
        # repeat the following for all algorithms
        for algorithm in algorithm_list:
            # generate a maze using the algorithm
            maze = create_maze( algorithm )
            # create message to display when test fails
            err_msg = f'Algorithm {algorithm} did not unvisit all cells'

            # repeat the following for all rows in maze
            for row in maze.grid:
                # repeat the following for all cells in the row
                for cell in row:
                    # assert that no cell is marked as visited
                    self.assertFalse( cell.visited, msg = err_msg )

    def test_NoCellUnvisited(self):
        """Test to check that all cells have been processed, thus no cell has
        walls on all four sides"""
        # repeat the following for all algorithms
        for algorithm in algorithm_list:
            # generate a maze using the algorithm
            maze = create_maze( algorithm )
            # create message to display when test fails
            err_msg = f'Algorithm {algorithm} did not generate entry_exit cells'
            # variable to store how a cell with walls on all sides is denoted
            walls_4 = {"top": True, "right": True, "bottom": True, "left": True}

            # repeat the following for all rows in maze
            for row in maze.grid:
                # repeat the following for all cells in the row
                for cell in row:
                    # check that the cell does not have walls on all four sides
                    self.assertNotEqual( cell.walls, walls_4, msg = err_msg )
