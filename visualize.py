import pygame
 
# Define some colors
EMPTY_COLOR = (255, 255, 255) # white
WALL_COLOR = (0, 0, 0) # black
GOAL_COLOR = (0, 255, 0) # green
AGENT_COLOR = (0, 0, 255) # blue
 
# This sets the WIDTH and HEIGHT (in pixels) of each grid location
WIDTH = 20
HEIGHT = 20

# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [222, 222]

# This sets the margin between each cell
MARGIN = 2
 

class VisualGame:
    def __init__(self, state):
        pygame.init()
        self.initialize_game(state)

    def initialize_game(self, state):
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Array Backed Grid")
        self.done = False
        self.clock = pygame.time.Clock()
        self.grid = self.state_to_grid(state)

    def state_to_grid(self, state):
        # state is a 100 dim list composed of 0,1,2,3
        # grid should be 10x10 list composed of COLORS
        color_map = {0: EMPTY_COLOR,
                     1: WALL_COLOR,
                     2: GOAL_COLOR,
                     3: AGENT_COLOR}
        # initialize a 10x10 grid
        grid = [[0 for i in range(10)] for j in range(10)]
        for row in range(10):
            for col in range(10):
                grid[row][col] = color_map[state[row*10+col]]
        return grid

    def update_grid(self, new_state):
        self.grid = self.state_to_grid(new_state)

    def end_game(self):
        self.done = True

    def run(self):
        while not self.done:
            # if user clicks close, then exit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  
                    self.done = True
            grid = self.grid
            self.screen.fill(EMPTY_COLOR)
            for row in range(len(grid)):
                for col in range(len(grid[0])):
                    color = grid[row][col]
                    pygame.draw.rect(self.screen, color,
                                    [(MARGIN + WIDTH) * col + MARGIN,
                                     (MARGIN + HEIGHT) * row + MARGIN,
                                     WIDTH, HEIGHT])
            # Limit to 60 frames per second
            self.clock.tick(30)
            pygame.display.flip()
        pygame.quit()
