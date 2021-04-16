import time
import random
import math

# global variable to store list of all available algorithms
algorithm_list = ["dfs_backtrack", "bin_tree"]

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

def binary_tree( maze, start_coor ):
    # store the current time
    time_start = time.time()

    # repeat the following for all rows
    for i in range(0, maze.num_rows):

        # check if we are in top row
        if( i == maze.num_rows - 1 ):
            # remove the right wall for this, because we cant remove top wall
            for j in range(0, maze.num_cols-1):
                maze.grid[i][j].remove_walls(i, j+1)
                maze.grid[i][j+1].remove_walls(i, j)

            # go to the next row
            break

        # repeat the following for all cells in rows
        for j in range(0, maze.num_cols):

            # check if we are in the last column
            if( j == maze.num_cols-1 ):
                # remove only the top wall for this cell
                maze.grid[i][j].remove_walls(i+1, j)
                maze.grid[i+1][j].remove_walls(i, j)
                continue

            # for all other cells
            # randomly choose between 0 and 1.
            # if we get 0, remove top wall; otherwise remove right wall
            remove_top = random.choice([True,False])

            # if we chose to remove top wall
            if remove_top:
                maze.grid[i][j].remove_walls(i+1, j)
                maze.grid[i+1][j].remove_walls(i, j)
            # if we chose top remove right wall
            else:
                maze.grid[i][j].remove_walls(i, j+1)
                maze.grid[i][j+1].remove_walls(i, j)

    print("Number of moves performed: {}".format(maze.num_cols * maze.num_rows))
    print("Execution time for algorithm: {:.4f}".format(time.time() - time_start))

    # choose the entry and exit coordinates
    maze.grid[maze.entry_coor[0]][maze.entry_coor[1]].set_as_entry_exit("entry",
        maze.num_rows-1, maze.num_cols-1)
    maze.grid[maze.exit_coor[0]][maze.exit_coor[1]].set_as_entry_exit("exit",
        maze.num_rows-1, maze.num_cols-1)

    # create a path for animating the maze creation using a binary tree
    path = list()
    # variable for holding number of cells visited until now
    visit_counter = 0
    # created list of cell visited uptil now to for backtracking
    visited = list()

    # create variables to hold the coords of current cell
    # no matter what the user gives as start coords, we choose the
    k_curr, l_curr = (maze.num_rows-1, maze.num_cols-1)
    # add first cell to the path
    path.append( (k_curr,l_curr) )

    # mark first cell as visited
    begin_time = time.time()

    # repeat until all the cells have been visited
    while visit_counter < maze.grid_size:     # While there are unvisited cells

        # for each cell, we only visit top and right cells.
        possible_neighbours = list()

        try:
            # take only those cells that are unvisited and accessible
            if not maze.grid[k_curr-1][l_curr].visited and k_curr != 0:
                if not maze.grid[k_curr][l_curr].is_walls_between(maze.grid[k_curr-1][l_curr]):
                    possible_neighbours.append( (k_curr-1,l_curr))
        except:
            print()

        try:
            # take only those cells that are unvisited and accessible
            if not maze.grid[k_curr][l_curr-1].visited and l_curr != 0:
                if not maze.grid[k_curr][l_curr].is_walls_between(maze.grid[k_curr][l_curr-1]):
                    possible_neighbours.append( (k_curr,l_curr-1))
        except:
            print()

        # if there are still traversible cell from current cell
        if len( possible_neighbours ) != 0:
            # select to first element to traverse
            k_next, l_next = possible_neighbours[0]
            # add this cell to the path
            path.append( possible_neighbours[0] )
            # add this cell to the visited
            visited.append( (k_curr,l_curr) )
            # mark this cell as visited
            maze.grid[k_next][l_next].visited = True

            visit_counter+= 1

            # update the current cell coords
            k_curr, l_curr = k_next, l_next

        else:
            # check if no more cells can be visited
            if len( visited ) != 0:
                k_curr, l_curr = visited.pop()
                path.append( (k_curr,l_curr) )
            else:
                break
    for row in maze.grid:
        for cell in row:
            cell.visited = False

    print(f"Generating path for maze took {time.time() - begin_time}s.")
    maze.generation_path = path
