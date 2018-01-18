from __future__ import absolute_import
import unittest

from src.maze_manager import MazeManager
from src.maze_viz import Visualizer
from src.maze import Maze


class TestMgr(unittest.TestCase):

    def test_ctor(self):
        """Make sure that the constructor values are getting properly set."""
        manager = MazeManager()

        self.assertEqual(manager.get_maze_count(), 0)
        self.assertEqual(manager.get_mazes(), [])
        self.assertEqual(manager.quiet_mode, False)

    def test_add_new(self):
        """Test adding mazes by passing maze specs into add_maze"""
        manager = MazeManager()

        maze1 = manager.add_maze(6, 6)
        self.assertEqual(maze1.id, 0)
        self.assertEqual(manager.get_mazes().__len__(), 1)
        self.assertEqual(manager.get_maze_count(), 1)

        maze2 = manager.add_maze(3, 3, 1)
        self.assertEqual(maze2.id, 1)
        self.assertEqual(manager.get_mazes().__len__(), 2)
        self.assertEqual(manager.get_maze_count(), 2)

    def test_add_existing(self):
        """Test adding mazes by passing already existing Maze objects in"""
        manager = MazeManager()

        maze1 = Maze(2, 2)
        self.assertEqual(maze1.id, 0)
        manager.add_existing_maze(maze1)

        self.assertEqual(manager.get_mazes().__len__(), 1)
        self.assertEqual(manager.get_maze_count(), 1)
        self.assertIsNotNone(manager.get_maze(maze1.id))
        self.assertEqual(manager.get_maze(maze1.id).id, maze1.id)

        maze2 = Maze(3, 3, 1)
        self.assertEqual(maze2.id, 1)
        manager.add_existing_maze(maze2)

        self.assertEqual(manager.get_mazes().__len__(), 2)
        self.assertEqual(manager.get_maze_count(), 2)
        self.assertIsNotNone(manager.get_maze(maze2.id))
        self.assertEqual(manager.get_maze(maze2.id).id, maze2.id)

    def test_get_maze(self):
        """Test the get_maze function"""
        manager = MazeManager()

        self.assertEqual(manager.get_maze(0), None)
        self.assertEqual(manager.get_mazes(), [])
        maze1 = manager.add_maze(6, 6)
        self.assertEqual(maze1.id, 0)

    def test_get_mazes(self):
        """Tests that get_mazes is returning all mazes"""
        manager = MazeManager()

        self.assertEqual(manager.get_maze(0), None)
        self.assertEqual(manager.get_mazes(), [])
        manager.add_maze(6, 6)
        manager.add_maze(6, 6)
        mazes = manager.get_mazes()
        self.assertAlmostEqual(mazes.__len__(), 2)

    def test_get_maze_count(self):
        """Tests the get_maze_number function"""
        manager = MazeManager()

        self.assertEqual(manager.get_maze_count(), 0)
        maze1 = Maze(2, 2)
        manager.add_existing_maze(maze1)
        self.assertEqual(manager.get_maze_count(), 1)

    def test_check_matching_id(self):
        """Check that check_matching_id is functioning properly"""

        manager = MazeManager()
        manager.add_maze(8, 8, 1)
        manager.add_maze(8, 8, 1)
        result = [manager.check_matching_id(1)]
        self.assertEqual(len(result), 1)

    def test_set_filename(self):
        """Tests that the filename is getting set"""
        manager = MazeManager()
        filename = "myFile"
        manager.set_filename(filename)
        self.assertEqual(filename, manager.media_name)

    def test_set_quiet_mode(self):
        manager = MazeManager()
        self.assertEqual(manager.quiet_mode, False)
        manager.set_quiet_mode(True)
        self.assertEqual(manager.quiet_mode, True)


if __name__ == "__main__":
    unittest.main()
