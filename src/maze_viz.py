
# Written by: Jostein Brændshøi
# Last Last modified: 06.11.17

import matplotlib.pyplot as plt
from matplotlib import animation

def plot_walls(maze, grid, ax):
    """ Plots the walls of the maze. This is used when generating the maze image"""
    fig = plt.figure(figsize = (7, 7*maze.num_rows/maze.num_cols))
    ax = plt.axes()

    ax.set_aspect("equal")
    #ax.axis("off")
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)

    title_box = ax.text(0, maze.num_rows + maze.cell_size + 0.1,
        r"{}$\times${}".format(maze.num_rows, maze.num_cols),
        bbox={"facecolor": "gray", "alpha": 0.5, "pad": 4}, fontname = "serif", fontsize = 15)

    for i in range(maze.num_rows):
        for j in range(maze.num_cols):
            if (grid[i][j].is_entry_exit == "entry"):
                ax.text(j*maze.cell_size, i*maze.cell_size, "START", fontsize = 7, weight = "bold")
            elif (grid[i][j].is_entry_exit == "exit"):
                ax.text(j*maze.cell_size, i*maze.cell_size, "END", fontsize = 7, weight = "bold")

            if (grid[i][j].walls["top"] == True):
                ax.plot([j*maze.cell_size, (j+1)*maze.cell_size],
                    [i*maze.cell_size, i*maze.cell_size], color = "k")
            if (grid[i][j].walls["right"] == True):
                ax.plot([(j+1)*maze.cell_size, (j+1)*maze.cell_size],
                    [i*maze.cell_size, (i+1)*maze.cell_size], color = "k")
            if (grid[i][j].walls["bottom"] == True):
                ax.plot([(j+1)*maze.cell_size, j*maze.cell_size],
                    [(i+1)*maze.cell_size, (i+1)*maze.cell_size], color = "k")
            if (grid[i][j].walls["left"] == True):
                ax.plot([j*maze.cell_size, j*maze.cell_size],
                    [(i+1)*maze.cell_size, i*maze.cell_size], color = "k")

def  configure_plot(maze):
    """Sets the initial properties of the maze image"""

    fig = plt.figure(figsize = (7, 7*maze.num_rows/maze.num_cols))
    ax = plt.axes()

    ax.set_aspect("equal")
    #ax.axis("off")
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)

    title_box = ax.text(0, maze.num_rows + maze.cell_size + 0.1,
        r"{}$\times${}".format(maze.num_rows, maze.num_cols),
        bbox={"facecolor": "gray", "alpha": 0.5, "pad": 4}, fontname = "serif", fontsize = 15)

    return ax, fig

def plot_maze(maze, grid, save_filename = None):
    """Function that plots the generated maze. Also adds indication of entry and exit points."""

    ax, fig = configure_plot(maze)

    plot_walls(maze, grid, ax)

    if save_filename is not None:
        fig.savefig("{}.png".format(save_filename), frameon = False)

def plot_maze_solution(maze, grid, path, save_filename = None):
    """Function that plots the generated maze. Also adds indication of entry and exit points."""

    ax, fig = configure_plot(maze)
    plot_walls(maze, grid, ax)

    list_of_backtrackers = [path_element[0] for path_element in path if path_element[1]]
    circle_num = 0      # Counter for coloring of circles

    ax.add_patch(plt.Circle(((path[0][0][1] + 0.5)*maze.cell_size,
        (path[0][0][0] + 0.5)*maze.cell_size), 0.2*maze.cell_size,
        fc = (0, circle_num/(len(path) - 2*len(list_of_backtrackers)), 0), alpha = 0.4))

    for i in range(1, len(path)):
        if path[i][0] not in list_of_backtrackers and path[i-1][0] not in list_of_backtrackers:
            circle_num += 1
            ax.add_patch(plt.Circle(((path[i][0][1] + 0.5)*maze.cell_size,
                (path[i][0][0] + 0.5)*maze.cell_size), 0.2*maze.cell_size,
                fc = (0, circle_num/(len(path) - 2*len(list_of_backtrackers)), 0), alpha = 0.4))

    if save_filename is not None:
        fig.savefig("{}.png".format(save_filename), frameon = False)

def animate_maze_generate(maze, path, save_filename = None):
    """Function that animates the process of generating the a maze where path is a list
    of coordinates indicating the path taken to carve out (break down walls) the maze."""
    fig = plt.figure(figsize = (7, 7*maze.num_rows/maze.num_cols))
    ax = plt.axes(xlim = (-1, maze.width+1), ylim = (-1, maze.height+1))

    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)

    lines = dict()
    squares = dict()

    # Adding indicator to see shere current search is happening.
    indicator = plt.Rectangle((path[0][0]*maze.cell_size, path[0][1]*maze.cell_size),
        maze.cell_size, maze.cell_size, fc = "purple", alpha = 0.6)
    ax.add_patch(indicator)

    # Only need to plot right and bottom wall for each cell since walls overlap.
    # Also adding squares to animate the path taken to carve out the maze.
    color_walls = "k"
    for i in range(maze.num_rows):
        for j in range(maze.num_cols):
            lines["{},{}: right".format(i, j)] = ax.plot([(j+1)*maze.cell_size, (j+1)*maze.cell_size],
                    [i*maze.cell_size, (i+1)*maze.cell_size],
                linewidth = 2, color = color_walls)[0]
            lines["{},{}: bottom".format(i, j)] = ax.plot([(j+1)*maze.cell_size, j*maze.cell_size],
                    [(i+1)*maze.cell_size, (i+1)*maze.cell_size],
                linewidth = 2, color = color_walls)[0]

            squares["{},{}".format(i, j)] = plt.Rectangle((j*maze.cell_size,
                i*maze.cell_size), maze.cell_size, maze.cell_size, fc = "red", alpha = 0.4)
            ax.add_patch(squares["{},{}".format(i, j)])

    # Plotting boundaries of maze.
    color_boundary = "k"
    ax.plot([0, maze.width], [maze.height,maze.height], linewidth = 2, color = color_boundary)
    ax.plot([maze.width, maze.width], [maze.height, 0], linewidth = 2, color = color_boundary)
    ax.plot([maze.width, 0], [0, 0], linewidth = 2, color = color_boundary)
    ax.plot([0, 0], [0, maze.height], linewidth = 2, color = color_boundary)

    def animate(frame):
        """Function to supervise animation of all objects."""
        animate_walls(frame)
        animate_squares(frame)
        animate_indicator(frame)
        ax.set_title("Step: {}".format(frame + 1), fontname = "serif", fontsize = 19)
        return []

    def animate_walls(frame):
        """Function that animates the visibility of the walls between cells."""
        if frame > 0:
            maze.init_grid[path[frame-1][0]][path[frame-1][1]].remove_walls(
                path[frame][0], path[frame][1])   # Wall between curr and neigh
            maze.init_grid[path[frame][0]][path[frame][1]].remove_walls(
                path[frame-1][0], path[frame-1][1])   # Wall between neigh and curr

            current_cell = maze.init_grid[path[frame-1][0]][path[frame-1][1]]
            next_cell = maze.init_grid[path[frame][0]][path[frame][1]]

            """Function to animate walls between cells as the search goes on."""
            for wall_key in ["right", "bottom"]:    # Only need to draw two of the four walls (overlap)
                if current_cell.walls[wall_key] == False:
                    lines["{},{}: {}".format(current_cell.row,
                        current_cell.col, wall_key)].set_visible(False)
                if next_cell.walls[wall_key] == False:
                    lines["{},{}: {}".format(next_cell.row,
                        next_cell.col, wall_key)].set_visible(False)

        return []

    def animate_squares(frame):
        """Function to animate the searched path of the algorithm."""
        squares["{},{}".format(path[frame][0], path[frame][1])].set_visible(False)
        return []


    def animate_indicator(frame):
        """Function to animate where the current search is happening."""
        indicator.set_xy((path[frame][1]*maze.cell_size, path[frame][0]*maze.cell_size))
        return []

    anim = animation.FuncAnimation(fig, animate, frames = len(path),
        interval = 50, blit = True, repeat = False)

    if (save_filename is not None):
        mpeg_writer = animation.FFMpegWriter(fps = 24, bitrate = 1000,
            codec = "libx264", extra_args = ["-pix_fmt", "yuv420p"])
        anim.save("{}{}x{}.mp4".format(save_filename, maze.num_rows,
            maze.num_cols), writer = mpeg_writer)

    return anim

def add_path(maze, grid, ax, lines, squares):
    # Adding squares to animate the path taken to solve the maze. Also adding entry/exit text
    color_walls = "k"
    for i in range(maze.num_rows):
        for j in range(maze.num_cols):
            if (grid[i][j].is_entry_exit == "entry"):
                ax.text(j*maze.cell_size, i*maze.cell_size, "START", fontsize = 7, weight = "bold")
            elif (grid[i][j].is_entry_exit == "exit"):
                ax.text(j*maze.cell_size, i*maze.cell_size, "END", fontsize = 7, weight = "bold")

            if grid[i][j].walls["top"]:
                lines["{},{}: top".format(i, j)] = ax.plot([j*maze.cell_size, (j+1)*maze.cell_size],
                        [i*maze.cell_size, i*maze.cell_size], linewidth = 2, color = color_walls)[0]
            if grid[i][j].walls["right"]:
                lines["{},{}: right".format(i, j)] = ax.plot([(j+1)*maze.cell_size, (j+1)*maze.cell_size],
                        [i*maze.cell_size, (i+1)*maze.cell_size], linewidth = 2, color = color_walls)[0]
            if grid[i][j].walls["bottom"]:
                lines["{},{}: bottom".format(i, j)] = ax.plot([(j+1)*maze.cell_size, j*maze.cell_size],
                        [(i+1)*maze.cell_size, (i+1)*maze.cell_size], linewidth = 2, color = color_walls)[0]
            if grid[i][j].walls["left"]:
                lines["{},{}: left".format(i, j)] = ax.plot([j*maze.cell_size, j*maze.cell_size],
                        [(i+1)*maze.cell_size, i*maze.cell_size], linewidth = 2, color = color_walls)[0]

            squares["{},{}".format(i, j)] = plt.Rectangle((j*maze.cell_size,
                i*maze.cell_size), maze.cell_size, maze.cell_size,
                fc = "red", alpha = 0.4, visible = False)
            ax.add_patch(squares["{},{}".format(i, j)])

def animate_maze_solve(maze, grid, path, save_filename = None):
    """Function that animates the process of generating the a maze where path is a list
    of coordinates indicating the path taken to carve out (break down walls) the maze."""
    fig = plt.figure(figsize = (7, 7*maze.num_rows/maze.num_cols))
    ax = plt.axes(xlim = (-1, maze.width+1), ylim = (-1, maze.height+1))
    # ax.set_aspect("equal")
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)

    lines = dict()
    squares = dict()

    # Adding indicator to see shere current search is happening.
    indicator = plt.Rectangle((path[0][0][0]*maze.cell_size, path[0][0][1]*maze.cell_size),
        maze.cell_size, maze.cell_size, fc = "purple", alpha = 0.6)
    ax.add_patch(indicator)

    add_path(maze, grid, ax, lines, squares)

    def animate(frame):
        """Function to supervise animation of all objects."""
        animate_squares(frame)
        animate_indicator(frame)
        ax.set_title("Step: {}".format(frame + 1), fontname = "serif", fontsize = 19)
        return []

    def animate_squares(frame):
        """Function to animate the solved path of the algorithm."""
        if frame > 0:
            if (path[frame-1][1] == True):  # Color backtracking
                squares["{},{}".format(path[frame-1][0][0], path[frame-1][0][1])].set_facecolor("orange")

            squares["{},{}".format(path[frame-1][0][0], path[frame-1][0][1])].set_visible(True)
            squares["{},{}".format(path[frame][0][0], path[frame][0][1])].set_visible(False)
        return []

    def animate_indicator(frame):
        """Function to animate where the current search is happening."""
        indicator.set_xy((path[frame][0][1]*maze.cell_size, path[frame][0][0]*maze.cell_size))
        return []

    anim = animation.FuncAnimation(fig, animate, frames = len(path),
        interval = 50, blit = True, repeat = False)

    if save_filename is not None:
        mpeg_writer = animation.FFMpegWriter(fps = 24, bitrate = 1000,
            codec = "libx264", extra_args = ["-pix_fmt", "yuv420p"])
        anim.save("{}{}x{}.mp4".format(save_filename, maze.num_rows,
            maze.num_cols), writer = mpeg_writer)

    return anim
