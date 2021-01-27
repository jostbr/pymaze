import time
import random
import math


def depth_first_recursive_backtracker( maze, start_coor ):
        k_curr, l_curr = start_coor             # Where to start generating
        path = [(k_curr, l_curr)]               # To track path of solution
        maze.grid[k_curr][l_curr].visited = True     # Set initial cell to visited
        visit_counter = 1                       # To count number of visited cells
        visited_cells = list()                  # Stack of visited cells for backtracking

        print("\nGenerating the maze with depth-first search...")
        time_start = time.time()

        while visit_counter < maze.grid_size:     # While there are unvisited cells
            neighbour_indices = maze.find_neighbours(k_curr, l_curr)    # Find neighbour indicies
            neighbour_indices = maze._validate_neighbours_generate(neighbour_indices)

            if neighbour_indices is not None:   # If there are unvisited neighbour cells
                visited_cells.append((k_curr, l_curr))              # Add current cell to stack
                k_next, l_next = random.choice(neighbour_indices)     # Choose random neighbour
                maze.grid[k_curr][l_curr].remove_walls(k_next, l_next)   # Remove walls between neighbours
                maze.grid[k_next][l_next].remove_walls(k_curr, l_curr)   # Remove walls between neighbours
                maze.grid[k_next][l_next].visited = True                 # Move to that neighbour
                k_curr = k_next
                l_curr = l_next
                path.append((k_curr, l_curr))   # Add coordinates to part of generation path
                visit_counter += 1

            elif len(visited_cells) > 0:  # If there are no unvisited neighbour cells
                k_curr, l_curr = visited_cells.pop()      # Pop previous visited cell (backtracking)
                path.append((k_curr, l_curr))   # Add coordinates to part of generation path

        print("Number of moves performed: {}".format(len(path)))
        print("Execution time for algorithm: {:.4f}".format(time.time() - time_start))

        maze.grid[maze.entry_coor[0]][maze.entry_coor[1]].set_as_entry_exit("entry",
            maze.num_rows-1, maze.num_cols-1)
        maze.grid[maze.exit_coor[0]][maze.exit_coor[1]].set_as_entry_exit("exit",
            maze.num_rows-1, maze.num_cols-1)

        for i in range(maze.num_rows):
            for j in range(maze.num_cols):
                maze.grid[i][j].visited = False      # Set all cells to unvisited before returning grid

        maze.generation_path = path
