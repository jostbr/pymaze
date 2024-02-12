from __future__ import absolute_import
from src.maze_manager import MazeManager
from src.maze import Maze


if __name__ == "__main__":

    # create a maze manager to handle all operations
    manager = MazeManager()

    # now create a maze using the binary tree method
    maze_using_aldous_broder = Maze(9, 7, algorithm="aldous_broder",start_coor=(1,1))

    # add this maze to the maze manager
    maze_using_aldous_broder = manager.add_existing_maze(maze_using_aldous_broder)

    # show the maze
    manager.show_maze(maze_using_aldous_broder.id)
    # show how the maze was generated
    # TO DO: Fix the animation for this algorithm
