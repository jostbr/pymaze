from src.maze import Maze
from src.maze_viz import Visualizer
from src.solver import DepthFirstBacktracker
from src.solver import BiDirectional
from src.solver import BreadthFirst


class MazeManager(object):
    """A manager that abstracts the interaction with the library's components. The graphs, animations, maze creation,
    and solutions are all handled through the manager.

    Attributes:
        mazes (list): It is possible to have more than one maze. They are stored inside this variable.
        media_name (string): The filename for animations and images
        quiet_mode (bool): When true, information is not shown on the console
    """

    def __init__(self):
        self.mazes = []
        self.media_name = ""
        self.quiet_mode = False

    def add_maze(self, row, col, id=0):
        """Add a maze to the manager. We give the maze an index of
        the total number of mazes in the manager. As long as we don't
        add functionality to delete mazes from the manager, the ids will
        always be unique. Note that the id will always be greater than 0 because
        we add 1 to the length of self.mazes, which is set after the id assignment

        Args:
            row (int): The height of the maze
            col (int): The width of the maze
            id (int):  The optional unique id of the maze.

        Returns
            Maze: The newly created maze
        """

        if id is not 0:
            self.mazes.append(Maze(row, col, id))
        else:
            if len(self.mazes) < 1:
                self.mazes.append(Maze(row, col, 0))
            else:
                self.mazes.append(Maze(row, col, len(self.mazes) + 1))

        return self.mazes[-1]

    def add_existing_maze(self, maze, override=True):
        """Add an already existing maze to the manager.
        Note that it is assumed that the maze already has an id. If the id
        already exists, the function will fail. To assign a new, unique id to
        the maze, set the overwrite flag to true.

        Args:
            maze: The maze that will be added to the manager
            override (bool): A flag that you can set to bypass checking the id

        Returns:
            True: If the maze was added to the manager
            False: If the maze could not be added to the manager
        """

        # Check if there is a maze with the same id. If there is a conflict, return False
        if self.check_matching_id(maze.id) is None:
            if override:
                if len(self.mazes) < 1:
                    maze.id = 0
                else:
                    maze.id = self.mazes.__len__()+1
        else:
            return False
        self.mazes.append(maze)
        return maze

    def get_maze(self, id):
        """Get a maze by its id.

            Args:
                id (int): The id of the desired maze

            Return:
                    Maze: Returns the maze if it was found.
                    None: If no maze was found
        """

        for maze in self.mazes:
            if maze.id == id:
                return maze
        print("Unable to locate maze")
        return None

    def get_mazes(self):
        """Get all of the mazes that the manager is holding"""
        return self.mazes

    def get_maze_count(self):
        """Gets the number of mazes that the manager is holding"""
        return self.mazes.__len__()

    def solve_maze(self, maze_id, method, neighbor_method="fancy"):
        """ Called to solve a maze by a particular method. The method
        is specified by a string. The options are
            1. DepthFirstBacktracker
            2.
            3.
        Args:
            maze_id (int): The id of the maze that will be solved
            method (string): The name of the method (see above)
            neighbor_method:

        """
        maze = self.get_maze(maze_id)
        if maze is None:
            print("Unable to locate maze. Exiting solver.")
            return None

        """DEVNOTE: When adding a new solution method, call it from here.
            Also update the list of names in the documentation above"""
        if method == "DepthFirstBacktracker":
            solver = DepthFirstBacktracker(maze, neighbor_method, self.quiet_mode)
            maze.solution_path = solver.solve()
        elif method == "BiDirectional":
            solver = BiDirectional(maze, neighbor_method, self.quiet_mode)
            maze.solution_path = solver.solve()
        elif method == "BreadthFirst":
            solver = BreadthFirst(maze, neighbor_method, self.quiet_mode)
            maze.solution_path = solver.solve()

    def show_maze(self, id, cell_size=1):
        """Just show the generation animation and maze"""
        vis = Visualizer(self.get_maze(id), cell_size, self.media_name)
        vis.show_maze()

    def show_generation_animation(self, id, cell_size=1):
        vis = Visualizer(self.get_maze(id), cell_size, self.media_name)
        vis.show_generation_animation()

    def show_solution(self, id, cell_size=1):
        vis = Visualizer(self.get_maze(id), cell_size, self.media_name)
        vis.show_maze_solution()

    def show_solution_animation(self, id, cell_size =1):
        """
        Shows the animation of the path that the solver took.

        Args:
            id (int): The id of the maze whose solution will be shown
            cell_size (int):
        """
        vis = Visualizer(self.get_maze(id), cell_size, self.media_name)
        vis.animate_maze_solution()

    def check_matching_id(self, id):
        """Check if the id already belongs to an existing maze

        Args:
            id (int): The id to be checked

        Returns:

        """
        return next((maze for maze in self.mazes if maze .id == id), None)

    def set_filename(self, filename):
        """
        Sets the filename for saving animations and images
        Args:
            filename (string): The name of the file without an extension
        """

        self.media_name = filename

    def set_quiet_mode(self, enabled):
        """
        Enables/Disables the quiet mode
        Args:
            enabled (bool): True when quiet mode is on, False when it is off
        """
        self.quiet_mode=enabled
