#schelling segregation model

import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#create an nxn board
#populate randomly with two different groups

def createGrid(gridSize):
    grid = []
    for i in range(0,gridSize):
        row = []
        for j in range(0,gridSize):
            row.append(random.randint(0,2))
        grid.append(row)
    return grid

#agents in group A prefer a fraction around them to be of the same group

#initialize beginning diversity tolerance
tol = 0.5

#take the position and grid and return the count for the group you're looking for

#create an array of neighbors
def neighbors(rowNumber, columnNumber, grid):
     return [[grid[i][j] if  i >= 0 and i < len(grid) and j >= 0 and j < len(grid[0]) else 0
                for j in range(columnNumber-2, columnNumber+1)]
                    for i in range(rowNumber-2, rowNumber+1)]

#Does the agent want to move because the number of outGroup is larger than tolerance?
def agentWantsMove(posX, posY, grid):
    nieghborhood = neighbors(posX, posY, grid)
    inGroup = nieghborhood[1][1]
    inGroupCount = -1 #the neighbors array returns the agent itself, so always subtract one
    outGroupCount = 0
    for i in range(0,3):
        for j in range(0,3):
            if nieghborhood[i][j] == inGroup:
                inGroupCount += 1
            elif nieghborhood[i][j] != 0:
                outGroupCount += 1
    return outGroupCount / (outGroupCount + inGroupCount) > tol

# if an agent is surrounded by more agents of a different group than the fraction set, 
# then they'll choose to move to a vacant spot

def agentShuffle(movingAgents, openLocations, grid):
    for i in range(len(movingAgents)):
        newHome = random.randint(0,len(openLocations)-1) #pick a random number in the available "addresses" for the agent to move to
        grid[openLocations[newHome][0]][openLocations[newHome][1]] = grid[movingAgents[i][0]][movingAgents[i][1]]
        grid[movingAgents[i][0]][movingAgents[i][1]] = 0
        openLocations.pop(newHome)
        openLocations.append([movingAgents[i][0],movingAgents[i][1]])
    return grid

def nextRound(grid):
    movingAgents = []
    openLocations = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] != 0:
                if agentWantsMove(i,j,grid):
                    movingAgents.append([i, j])
            else:
                openLocations.append([i,j])
    return agentShuffle(movingAgents, openLocations, grid)

def main():
    grid = createGrid(9)
    for i in range(0,3):
        grid = nextRound(grid)
        plt.imshow(grid)
        plt.colorbar()
        plt.show()
    return grid

# print(main())
