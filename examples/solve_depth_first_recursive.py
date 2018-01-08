from __future__ import absolute_import
from matplotlib import pyplot as plt
from src.maze import Maze
from src.maze_viz import plot_maze, animate_maze_generate, plot_maze_solution, animate_maze_solve


if __name__ == "__main__":
    maze_generator = Maze(10, 10, 1)
    grid, entry, exit, path_gen = maze_generator.generate_maze((0, 0))
    path_solve = maze_generator.solve_bfs(grid, entry, exit)

    plot_maze(maze_generator, grid)
    plot_maze_solution(maze_generator, grid, path_solve)
    anim_generate = animate_maze_generate(maze_generator, path_gen)
    anim_solve = animate_maze_solve(maze_generator, grid, path_solve)

plt.show()