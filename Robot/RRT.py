import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import KDTree
import time

class Node:
    """
    This class is for nodes to be used in the RRT algorithm
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None


class RRT:

    """
    This class implements the standard Rapid-exploring Random Trees Algorithm (RRT)  
    """

    def __init__(self, start, goal, map_size, obstacles, step_size=0.5, max_iter=500):
        """
        Initializer:-
            start: tuple of (x,y) coords of current position of Arlo
            goal:  tuple of (x,y) coords for goal destination
            map_size: tuple of (x,y) values determing the size of the map
            obstacles: List of obstacles as (x, y, radius)
            step_size: The maximum radius for a new node to be from it's nearest node
            max_iter: max number of new nodes that can be created before the algorithm gives up
        """
        self.start = Node(start[0], start[1]) #Initial node takes the current position of arlo
        self.goal = Node(goal[0], goal[1]) #Node containing the final location
        self.map_size = map_size 
        self.obstacles = obstacles 
        self.step_size = step_size
        self.max_iter = max_iter
        self.nodes = [self.start] #List of all nodes in the map, initialised with the start node

    def get_random_node(self):
        """
        select a new random position
        """
        x = np.random.uniform(0, self.map_size[0])
        y = np.random.uniform(0, self.map_size[1])
        random_node = Node(x, y)
        return random_node
    
    def distance(self, node1, node2):
        """
        Find the distance between any 2 nodes
        """
        return np.sqrt((node1.x - node2.x)**2 + (node1.y - node2.y)**2)
    
    def is_in_obstacle(self, node):
        """
        check for being inside obstacle
        """
        for (ox, oy, radius) in self.obstacles:
            if np.sqrt((node.x - ox)**2 + (node.y - oy)**2) <= radius: 
                #If distances between node and obstacle's centre is less than the obstacels radius, then the node is inside the obstacle
                return True
        return False
    
    def get_nearest_node(self, random_node):
        """
        To get the nearest node, I am transforming the nodes into a KDTree,
        as the KDTree library has easy querying for nearest node
        """
        nodes = np.array([(node.x, node.y) for node in self.nodes])
        tree = KDTree(nodes) 
        _, idx = tree.query([random_node.x, random_node.y]) #Built in function for finding nearest node
        return self.nodes[idx]
    
    def step_towards(self, nearest_node, random_node):
        """
        Creates a new node that is at the same angle from the nearest node as the randomly generated node,
        but is at a distance equal to the step size.
        """
        theta = np.arctan2(random_node.y - nearest_node.y, random_node.x - nearest_node.x)
        new_node = Node(nearest_node.x + self.step_size * np.cos(theta), nearest_node.y + self.step_size * np.sin(theta))
        new_node.parent = nearest_node
        return new_node
    
    def is_collision_free(self, node1, node2):
        """
        Detects if there are any obstacels between node1 and node2
        This is done by splitting the distance between the nodes into step_size steps, and checking that 
        at each step, we do not intersect with an obstacle.
        ie. The edge between nodes does not cross through an obstacle
        """
        steps = int(self.distance(node1, node2) / 1000*self.step_size) # number of steps between the nodes
        for i in range(steps):
            x = node1.x + i * (node2.x - node1.x) / steps
            y = node1.y + i * (node2.y - node1.y) / steps
            if self.is_in_obstacle(Node(x, y)):
                return False
        return True
    
    def find_path(self): 
        """
        This functions implements the pathfinding algorithm, utilising the above methods
        """
        for i in range(self.max_iter):
            random_node = self.get_random_node() #step 1: select any random position
            nearest_node = self.get_nearest_node(random_node) #step 2: find that positions nearest node
            new_node = self.step_towards(nearest_node, random_node)#step 3: check if rand.pos. and nearest node are within max.rad
            
            if not self.is_in_obstacle(new_node) and self.is_collision_free(nearest_node, new_node):
                # check if new_node is within an obstacle, and if 
                # the path between it and its nearest node is obstacle free
                self.nodes.append(new_node) # if all conditions satisfied, add the new node, with its parent being nearest node
                self.plot_step(new_node)  # Update plot in real time (only for visual effect hehe)
                
                if self.distance(new_node, self.goal) < self.step_size: #check if the new node is at the goal
                    final_node = Node(self.goal.x, self.goal.y)
                    final_node.parent = new_node
                    self.nodes.append(final_node)
                    print(f"Goal reached in {i} iterations.")
                    path = self.get_final_path(final_node)
                    return path
            time.sleep(0.01)  # Slow down to see the steps better
        print("Goal not reached.")
        return None
    
    def get_final_path(self, node): 
        """
        iterate backwards from goal nodes parents to determine the desired path
        """
        path = []
        while node is not None:
            path.append([node.x, node.y])
            node = node.parent
        return path[::-1]
    def plot_initial(self):
        fig, ax = plt.subplots()
        ax.set_xlim(0, self.map_size[0])
        ax.set_ylim(0, self.map_size[1])
        
        # Plot obstacles
        for (ox, oy, radius) in self.obstacles:
            obstacle = plt.Circle((ox, oy), radius, color='r')
            ax.add_patch(obstacle)
        
        # Plot start and goal
        ax.plot(self.start.x, self.start.y, "go")  # Start in green
        ax.plot(self.goal.x, self.goal.y, "bo")  # Goal in blue
        
        self.fig = fig
        self.ax = ax

    def plot_step(self, node):
        if node.parent:
            self.ax.plot([node.x, node.parent.x], [node.y, node.parent.y], "k-", alpha=0.5)
        plt.pause(0.01)

    def plot_final(self, path=None):
        # Plot final path
        if path:
            self.ax.plot([x for (x, y) in path], [y for (x, y) in path], "g-", linewidth=2)

        plt.show()



