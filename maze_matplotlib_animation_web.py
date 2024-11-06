import streamlit as st
import streamlit.components.v1 as components

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import math

from simpleai.search import CspProblem, backtrack
from simpleai.search import SearchProblem, astar

# Define cost of moving around the map
W = 21
cost_regular = 1.0
cost_diagonal = 1.7

# Create the cost dictionary
COSTS = {
    "up": cost_regular,
    "down": cost_regular,
    "left": cost_regular,
    "right": cost_regular,
    "up left": cost_diagonal,
    "up right": cost_diagonal,
    "down left": cost_diagonal,
    "down right": cost_diagonal,
}

# Define the map
MAP = """
##############################
#         #              #   #
# ####    ########       #   #
# o  #    #              #   #
#    ###     #####  ######   #
#      #   ###   #           #
#      #     #   #  #  #   ###
#     #####    #    #  # x   #
#              #       #     #
##############################
"""

# Class containing the methods to solve the maze
class MazeSolver(SearchProblem):
    # Initialize the class 
    def __init__(self, board):
        self.board = board
        self.goal = (0, 0)

        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x].lower() == "o":
                    self.initial = (x, y)
                elif self.board[y][x].lower() == "x":
                    self.goal = (x, y)

        super(MazeSolver, self).__init__(initial_state=self.initial)

    # Define the method that takes actions
    # to arrive at the solution
    def actions(self, state):
        actions = []
        for action in COSTS.keys():
            newx, newy = self.result(state, action)
            if self.board[newy][newx] != "#":
                actions.append(action)

        return actions

    # Update the state based on the action
    def result(self, state, action):
        x, y = state

        if action.count("up"):
            y -= 1
        if action.count("down"):
            y += 1
        if action.count("left"):
            x -= 1
        if action.count("right"):
            x += 1

        new_state = (x, y)

        return new_state

    # Check if we have reached the goal
    def is_goal(self, state):
        return state == self.goal

    # Compute the cost of taking an action
    def cost(self, state, action, state2):
        return COSTS[action]

    # Heuristic that we use to arrive at the solution
    def heuristic(self, state):
        x, y = state
        gx, gy = self.goal

        return math.sqrt((x - gx) ** 2 + (y - gy) ** 2)

MAP = [list(x) for x in MAP.split("\n") if x]

# Create maze solver object
problem = MazeSolver(MAP)

# Run the solver
result = astar(problem, graph_search=True)

# Extract the path
path = [x[1] for x in result.path()]
n = len(path)
px = []
py = []
for p in path:
    px.append(p[0]*W + W // 2)
    py.append(p[1]*W + W // 2)

# Print the result
print(path)

im = plt.imread("maze.bmp")
fig, ax = plt.subplots()

image = ax.imshow(im)
dest, = ax.plot(px[-1:], py[-1:],"ro", markersize = 11)

red_square, = ax.plot([],[],"rs", markersize = 11)

def init():
    return image, dest, red_square 

def animate(i):
    red_square.set_data(px[:i+1], py[:i+1])
    return image, dest, red_square 

anim = FuncAnimation(fig, animate, frames = n, interval = 500, 
                     init_func=init, repeat = False, blit = True)

components.html(anim.to_jshtml(), height = 550)
