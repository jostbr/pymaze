from __future__ import absolute_import
import matplotlib.pyplot as plt
from matplotlib import animation
from src.maze import Maze
from src.maze_viz import plot_maze, animate_maze_generate, plot_maze_solution, animate_maze_solve


if __name__ == "__main__":
    maze_generator = Maze(10, 10, 1)
    grid, path_gen = maze_generator.generate_maze((0, 0))

    plot_maze(maze_generator, grid)
    anim_generate = animate_maze_generate(maze_generator, path_gen)

    path_solve = maze_generator.solve_maze(grid, method = "fancy")

    plot_maze_solution(maze_generator, grid, path_solve)
    anim_solve = animate_maze_solve(maze_generator, grid, path_solve)

    plt.show()