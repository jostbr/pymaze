import matplotlib.pyplot as plt
from matplotlib import animation
import logging

logging.basicConfig(level=logging.DEBUG)


class Visualizer(object):
    """Class that handles all aspects of visualization.


    Attributes:
        maze: The maze that will be visualized
        cell_size (int): How large the cells will be in the plots
        height (int): The height of the maze
        width (int): The width of the maze
        ax: The axes for the plot
        lines:
        squares:
        media_filename (string): The name of the animations and images

    """

    def __init__(self, maze, cell_size, media_filename):
        self.maze = maze
        self.cell_size = cell_size
        self.height = maze.num_rows * cell_size
        self.width = maze.num_cols * cell_size
        self.ax = None
        self.lines = dict()
        self.squares = dict()
        self.media_filename = media_filename

    def set_media_filename(self, filename):
        """Sets the filename of the media
        Args:
            filename (string): The name of the media
        """
        self.media_filename = filename

    def show_maze(self):
        """Displays a plot of the maze without the solution path"""

        # Create the plot figure and style the axes
        fig = self.configure_plot()

        # Plot the walls on the figure
        self.plot_walls()

        # Display the plot to the user
        plt.show()

        # Handle any potential saving
        if self.media_filename:
            fig.savefig(
                "{}{}.png".format(self.media_filename, "_generation"),
                frameon=None,
            )

    def plot_walls(self):
        """Plots the walls of a maze. This is used when generating the maze image"""
        for i in range(self.maze.num_rows):
            for j in range(self.maze.num_cols):
                if self.maze.initial_grid[i][j].is_entry_exit == "entry":
                    self.ax.text(
                        j * self.cell_size,
                        i * self.cell_size,
                        "START",
                        fontsize=7,
                        weight="bold",
                    )
                elif self.maze.initial_grid[i][j].is_entry_exit == "exit":
                    self.ax.text(
                        j * self.cell_size,
                        i * self.cell_size,
                        "END",
                        fontsize=7,
                        weight="bold",
                    )
                if self.maze.initial_grid[i][j].walls["top"]:
                    self.ax.plot(
                        [j * self.cell_size, (j + 1) * self.cell_size],
                        [i * self.cell_size, i * self.cell_size],
                        color="k",
                    )
                if self.maze.initial_grid[i][j].walls["right"]:
                    self.ax.plot(
                        [(j + 1) * self.cell_size, (j + 1) * self.cell_size],
                        [i * self.cell_size, (i + 1) * self.cell_size],
                        color="k",
                    )
                if self.maze.initial_grid[i][j].walls["bottom"]:
                    self.ax.plot(
                        [(j + 1) * self.cell_size, j * self.cell_size],
                        [(i + 1) * self.cell_size, (i + 1) * self.cell_size],
                        color="k",
                    )
                if self.maze.initial_grid[i][j].walls["left"]:
                    self.ax.plot(
                        [j * self.cell_size, j * self.cell_size],
                        [(i + 1) * self.cell_size, i * self.cell_size],
                        color="k",
                    )

    def configure_plot(self):
        """Sets the initial properties of the maze plot. Also creates the plot and axes"""

        # Create the plot figure
        fig = plt.figure(
            figsize=(7, 7 * self.maze.num_rows / self.maze.num_cols)
        )

        # Create the axes
        self.ax = plt.axes()

        # Set an equal aspect ratio
        self.ax.set_aspect("equal")

        # Remove the axes from the figure
        self.ax.axes.get_xaxis().set_visible(False)
        self.ax.axes.get_yaxis().set_visible(False)

        title_box = self.ax.text(
            0,
            self.maze.num_rows + self.cell_size + 0.1,
            r"{}$\times${}".format(self.maze.num_rows, self.maze.num_cols),
            bbox={"facecolor": "gray", "alpha": 0.5, "pad": 4},
            fontname="serif",
            fontsize=15,
        )

        return fig

    def show_maze_solution(self):
        """Function that plots the solution to the maze. Also adds indication of entry and exit points."""

        # Create the figure and style the axes
        fig = self.configure_plot()

        # Plot the walls onto the figure
        self.plot_walls()

        list_of_backtrackers = [
            path_element[0]
            for path_element in self.maze.solution_path
            if path_element[1]
        ]

        # Keeps track of how many circles have been drawn
        circle_num = 0

        self.ax.add_patch(
            plt.Circle(
                (
                    (self.maze.solution_path[0][0][1] + 0.5) * self.cell_size,
                    (self.maze.solution_path[0][0][0] + 0.5) * self.cell_size,
                ),
                0.2 * self.cell_size,
                fc=(
                    0,
                    circle_num
                    / (
                        len(self.maze.solution_path)
                        - 2 * len(list_of_backtrackers)
                    ),
                    0,
                ),
                alpha=0.4,
            )
        )

        for i in range(1, self.maze.solution_path.__len__()):
            if (
                self.maze.solution_path[i][0] not in list_of_backtrackers
                and self.maze.solution_path[i - 1][0]
                not in list_of_backtrackers
            ):
                circle_num += 1
                self.ax.add_patch(
                    plt.Circle(
                        (
                            (self.maze.solution_path[i][0][1] + 0.5)
                            * self.cell_size,
                            (self.maze.solution_path[i][0][0] + 0.5)
                            * self.cell_size,
                        ),
                        0.2 * self.cell_size,
                        fc=(
                            0,
                            circle_num
                            / (
                                len(self.maze.solution_path)
                                - 2 * len(list_of_backtrackers)
                            ),
                            0,
                        ),
                        alpha=0.4,
                    )
                )

        # Display the plot to the user
        plt.show()

        # Handle any saving
        if self.media_filename:
            fig.savefig(
                "{}{}.png".format(self.media_filename, "_solution"),
                frameon=None,
            )

    def show_generation_animation(self):
        """Function that animates the process of generating the a maze where path is a list
        of coordinates indicating the path taken to carve out (break down walls) the maze."""

        # Create the figure and style the axes
        fig = self.configure_plot()

        # The square that represents the head of the algorithm
        indicator = plt.Rectangle(
            (
                self.maze.generation_path[0][0] * self.cell_size,
                self.maze.generation_path[0][1] * self.cell_size,
            ),
            self.cell_size,
            self.cell_size,
            fc="purple",
            alpha=0.6,
        )

        self.ax.add_patch(indicator)

        # Only need to plot right and bottom wall for each cell since walls overlap.
        # Also adding squares to animate the path taken to carve out the maze.
        color_walls = "k"
        for i in range(self.maze.num_rows):
            for j in range(self.maze.num_cols):
                self.lines["{},{}: right".format(i, j)] = self.ax.plot(
                    [(j + 1) * self.cell_size, (j + 1) * self.cell_size],
                    [i * self.cell_size, (i + 1) * self.cell_size],
                    linewidth=2,
                    color=color_walls,
                )[0]
                self.lines["{},{}: bottom".format(i, j)] = self.ax.plot(
                    [(j + 1) * self.cell_size, j * self.cell_size],
                    [(i + 1) * self.cell_size, (i + 1) * self.cell_size],
                    linewidth=2,
                    color=color_walls,
                )[0]

                self.squares["{},{}".format(i, j)] = plt.Rectangle(
                    (j * self.cell_size, i * self.cell_size),
                    self.cell_size,
                    self.cell_size,
                    fc="red",
                    alpha=0.4,
                )
                self.ax.add_patch(self.squares["{},{}".format(i, j)])

        # Plotting boundaries of maze.
        color_boundary = "k"
        self.ax.plot(
            [0, self.width],
            [self.height, self.height],
            linewidth=2,
            color=color_boundary,
        )
        self.ax.plot(
            [self.width, self.width],
            [self.height, 0],
            linewidth=2,
            color=color_boundary,
        )
        self.ax.plot(
            [self.width, 0], [0, 0], linewidth=2, color=color_boundary
        )
        self.ax.plot(
            [0, 0], [0, self.height], linewidth=2, color=color_boundary
        )

        def animate(frame):
            """Function to supervise animation of all objects."""
            animate_walls(frame)
            animate_squares(frame)
            animate_indicator(frame)
            self.ax.set_title(
                "Step: {}".format(frame + 1), fontname="serif", fontsize=19
            )
            return []

        def animate_walls(frame):
            """Function that animates the visibility of the walls between cells."""
            if frame > 0:
                self.maze.grid[self.maze.generation_path[frame - 1][0]][
                    self.maze.generation_path[frame - 1][1]
                ].remove_walls(
                    self.maze.generation_path[frame][0],
                    self.maze.generation_path[frame][1],
                )  # Wall between curr and neigh

                self.maze.grid[self.maze.generation_path[frame][0]][
                    self.maze.generation_path[frame][1]
                ].remove_walls(
                    self.maze.generation_path[frame - 1][0],
                    self.maze.generation_path[frame - 1][1],
                )  # Wall between neigh and curr

                current_cell = self.maze.grid[
                    self.maze.generation_path[frame - 1][0]
                ][self.maze.generation_path[frame - 1][1]]
                next_cell = self.maze.grid[
                    self.maze.generation_path[frame][0]
                ][self.maze.generation_path[frame][1]]

                """Function to animate walls between cells as the search goes on."""
                for wall_key in [
                    "right",
                    "bottom",
                ]:  # Only need to draw two of the four walls (overlap)
                    if current_cell.walls[wall_key] is False:
                        self.lines[
                            "{},{}: {}".format(
                                current_cell.row, current_cell.col, wall_key
                            )
                        ].set_visible(False)
                    if next_cell.walls[wall_key] is False:
                        self.lines[
                            "{},{}: {}".format(
                                next_cell.row, next_cell.col, wall_key
                            )
                        ].set_visible(False)

        def animate_squares(frame):
            """Function to animate the searched path of the algorithm."""
            self.squares[
                "{},{}".format(
                    self.maze.generation_path[frame][0],
                    self.maze.generation_path[frame][1],
                )
            ].set_visible(False)
            return []

        def animate_indicator(frame):
            """Function to animate where the current search is happening."""
            indicator.set_xy(
                (
                    self.maze.generation_path[frame][1] * self.cell_size,
                    self.maze.generation_path[frame][0] * self.cell_size,
                )
            )
            return []

        logging.debug("Creating generation animation")
        anim = animation.FuncAnimation(
            fig,
            animate,
            frames=self.maze.generation_path.__len__(),
            interval=100,
            blit=True,
            repeat=False,
        )

        logging.debug("Finished creating the generation animation")

        # Display the plot to the user
        plt.show()

        # Handle any saving
        if self.media_filename:
            print("Saving generation animation. This may take a minute....")
            mpeg_writer = animation.FFMpegWriter(
                fps=24,
                bitrate=1000,
                codec="libx264",
                extra_args=["-pix_fmt", "yuv420p"],
            )
            anim.save(
                "{}{}{}x{}.mp4".format(
                    self.media_filename,
                    "_generation_",
                    self.maze.num_rows,
                    self.maze.num_cols,
                ),
                writer=mpeg_writer,
            )

    def add_path(self):
        # Adding squares to animate the path taken to solve the maze. Also adding entry/exit text
        color_walls = "k"
        for i in range(self.maze.num_rows):
            for j in range(self.maze.num_cols):
                if self.maze.initial_grid[i][j].is_entry_exit == "entry":
                    self.ax.text(
                        j * self.cell_size,
                        i * self.cell_size,
                        "START",
                        fontsize=7,
                        weight="bold",
                    )
                elif self.maze.initial_grid[i][j].is_entry_exit == "exit":
                    self.ax.text(
                        j * self.cell_size,
                        i * self.cell_size,
                        "END",
                        fontsize=7,
                        weight="bold",
                    )

                if self.maze.initial_grid[i][j].walls["top"]:
                    self.lines["{},{}: top".format(i, j)] = self.ax.plot(
                        [j * self.cell_size, (j + 1) * self.cell_size],
                        [i * self.cell_size, i * self.cell_size],
                        linewidth=2,
                        color=color_walls,
                    )[0]
                if self.maze.initial_grid[i][j].walls["right"]:
                    self.lines["{},{}: right".format(i, j)] = self.ax.plot(
                        [(j + 1) * self.cell_size, (j + 1) * self.cell_size],
                        [i * self.cell_size, (i + 1) * self.cell_size],
                        linewidth=2,
                        color=color_walls,
                    )[0]
                if self.maze.initial_grid[i][j].walls["bottom"]:
                    self.lines["{},{}: bottom".format(i, j)] = self.ax.plot(
                        [(j + 1) * self.cell_size, j * self.cell_size],
                        [(i + 1) * self.cell_size, (i + 1) * self.cell_size],
                        linewidth=2,
                        color=color_walls,
                    )[0]
                if self.maze.initial_grid[i][j].walls["left"]:
                    self.lines["{},{}: left".format(i, j)] = self.ax.plot(
                        [j * self.cell_size, j * self.cell_size],
                        [(i + 1) * self.cell_size, i * self.cell_size],
                        linewidth=2,
                        color=color_walls,
                    )[0]
                self.squares["{},{}".format(i, j)] = plt.Rectangle(
                    (j * self.cell_size, i * self.cell_size),
                    self.cell_size,
                    self.cell_size,
                    fc="red",
                    alpha=0.4,
                    visible=False,
                )
                self.ax.add_patch(self.squares["{},{}".format(i, j)])

    def animate_maze_solution(self):
        """Function that animates the process of generating the a maze where path is a list
        of coordinates indicating the path taken to carve out (break down walls) the maze."""

        # Create the figure and style the axes
        fig = self.configure_plot()

        # Adding indicator to see shere current search is happening.
        indicator = plt.Rectangle(
            (
                self.maze.solution_path[0][0][0] * self.cell_size,
                self.maze.solution_path[0][0][1] * self.cell_size,
            ),
            self.cell_size,
            self.cell_size,
            fc="purple",
            alpha=0.6,
        )
        self.ax.add_patch(indicator)

        self.add_path()

        def animate_squares(frame):
            """Function to animate the solved path of the algorithm."""
            if frame > 0:
                if self.maze.solution_path[frame - 1][
                    1
                ]:  # Color backtracking
                    self.squares[
                        "{},{}".format(
                            self.maze.solution_path[frame - 1][0][0],
                            self.maze.solution_path[frame - 1][0][1],
                        )
                    ].set_facecolor("orange")

                self.squares[
                    "{},{}".format(
                        self.maze.solution_path[frame - 1][0][0],
                        self.maze.solution_path[frame - 1][0][1],
                    )
                ].set_visible(True)
                self.squares[
                    "{},{}".format(
                        self.maze.solution_path[frame][0][0],
                        self.maze.solution_path[frame][0][1],
                    )
                ].set_visible(False)
            return []

        def animate_indicator(frame):
            """Function to animate where the current search is happening."""
            indicator.set_xy(
                (
                    self.maze.solution_path[frame][0][1] * self.cell_size,
                    self.maze.solution_path[frame][0][0] * self.cell_size,
                )
            )
            return []

        def animate(frame):
            """Function to supervise animation of all objects."""
            animate_squares(frame)
            animate_indicator(frame)
            self.ax.set_title(
                "Step: {}".format(frame + 1), fontname="serif", fontsize=19
            )
            return []

        logging.debug("Creating solution animation")
        anim = animation.FuncAnimation(
            fig,
            animate,
            frames=self.maze.solution_path.__len__(),
            interval=100,
            blit=True,
            repeat=False,
        )
        logging.debug("Finished creating solution animation")

        # Display the animation to the user
        plt.show()

        # Handle any saving
        if self.media_filename:
            print("Saving solution animation. This may take a minute....")
            mpeg_writer = animation.FFMpegWriter(
                fps=24,
                bitrate=1000,
                codec="libx264",
                extra_args=["-pix_fmt", "yuv420p"],
            )
            anim.save(
                "{}{}{}x{}.mp4".format(
                    self.media_filename,
                    "_solution_",
                    self.maze.num_rows,
                    self.maze.num_cols,
                ),
                writer=mpeg_writer,
            )
