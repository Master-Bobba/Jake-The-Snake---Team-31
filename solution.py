#
# Please run this code my calling the constructor of Maze class using 
# m = Maze(<your maze array>) and sending in the maze to be solved. 
#
# See at the bottom for an example.
#
# The solution will be printed in the terminal window
#
# Author Bayvazov

class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)
    
    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("Empty Stack frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

class Maze():
    def __init__(self, contents):
     
        # Determine the height and width of maze
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        #keep track of walls
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "$":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "F":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)
        
        self.solution = None
        print(self.solve())
    
    def neighbors(self, state):
        row, col = state

        # All possible actions
        candidate = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        # Ensure action is valid
        result = []
        for action, (r, c) in candidate:
            try:
                if not self.walls[r][c]:
                    result.append((action, (r, c)))
            except IndexError:
                continue
        return result 

    def solve(self):
        """Finds a solution to maze, if one exists."""

        # Keep track of number of states explored
        self.num_explored = 0

        # Initialize frontier to just the starting position
        start = Node(state = self.start, parent = None, action = None)
        frontier = StackFrontier()
        frontier.add(start)

        # Initialise an empty explored set
        self.explored = set()

        # keep looping until solution found
        while True:

            # If nothing left in frontier, then no solution
            if frontier.empty():
                raise Exception("No Solution")

            # Choose a node from the Frontier
            node = frontier.remove()
            self.num_explored += 1

            # if node is the goal, then we have a solution 
            if node.state == self.goal:
                actions = []
                cells = []
                moves = []

                # Follow parent nodes to find solution
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                output = ""
                for i in range(len(actions)-1):
                    output += actions[i] + ", "

                return output + actions[-1]
            
            # Mark node as explored
            self.explored.add(node.state)

            # Add neighbors to frontier
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state = state, parent = node, action = action)
                    frontier.add(child)

contents = [['+', '-', '+', '-', '+', '-', '+'],
            ['|', ' ', ' ', ' ', ' ', ' ', '|'],
            ['+', ' ', '+', '-', '+', ' ', '+'],
            ['|', ' ', ' ', 'F', '|', ' ', '|'],
            ['+', '-', '+', '-', '+', ' ', '+'],
            ['|', '$', ' ', ' ', ' ', ' ', '|'],
            ['+', '-', '+', '-', '+', '-', '+']]

if __name__ == '__main__':
    m = Maze(contents)

#
# Please run this code my calling the constructor of Maze class using 
# m = Maze(<your maze array>) and sending in the maze to be solved
#
# The solution will be printed in the terminal windon
#