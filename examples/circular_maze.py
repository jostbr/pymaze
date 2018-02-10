from src.maze import Circle
from src.circle_viz import Visualizer
if __name__ == "__main__":
    #Generates and displays a random circular maze
    
    maze = Circle(12) #Generates a circular maze of 10 layers
    Visualizer(maze) #Visualizes the generated circular maze

    