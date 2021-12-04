from pymaze.maze_manager import MazeManager
from pymaze.maze import Maze


if __name__ == "__main__":

    # create a maze manager to handle all operations
    manager = MazeManager()

    # now create a maze using the binary tree method
    maze_using_btree = Maze(10, 10, algorithm="bin_tree")

    # add this maze to the maze manager
    maze_using_btree = manager.add_existing_maze(maze_using_btree)

    # show the maze
    manager.show_maze(maze_using_btree.id)

    # show how the maze was generated
    manager.show_generation_animation(maze_using_btree.id)
