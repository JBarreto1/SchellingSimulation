#schelling segregation model
#resourses: http://nifty.stanford.edu/2014/mccown-schelling-model-segregation/
# https://en.wikipedia.org/wiki/Schelling%27s_model_of_segregation

import random
import numpy as np
import matplotlib.pyplot as plt
import copy
from matplotlib.animation import FuncAnimation

#create an nxn board
#populate randomly with two different groups

def createGrid(gridSize,groupRatio,percentEmpty):
    grid = []
    totalSpaces = gridSize * gridSize
    emptySpaces = int(totalSpaces * percentEmpty)
    occupiedSpaces = totalSpaces - emptySpaces
    groupOne = int(occupiedSpaces * groupRatio)
    groupTwo = occupiedSpaces - groupOne
    agentsChoice = [0,1,2]
    for i in range(0,gridSize):
        row = []
        for j in range(0,gridSize):
            choice = random.choices(agentsChoice, weights = [emptySpaces, groupOne, groupTwo], k = 1)
            row.append(choice[0])
            if choice == [0]:
                emptySpaces -= 1
            elif choice == [1]:
                groupOne -= 1
            elif choice == [2]:
                groupTwo -= 1
            # row.append(random.randint(0,2))
        grid.append(row)
    # print(groupOne,groupTwo,emptySpaces)
    return grid

#agents in group A prefer a fraction around them to be of the same group

#take the position and grid and return the count for the group you're looking for

#create an array of neighbors
def neighbors(radius, rowNumber, columnNumber, grid):
     return [[grid[i][j] if  i >= 0 and i < len(grid) and j >= 0 and j < len(grid[0]) else 0
                for j in range(columnNumber-radius, columnNumber+1+radius)]
                    for i in range(rowNumber-radius, rowNumber+1+radius)]

#Does the agent want to move because the number of outGroup is larger than tolerance?
def agentWantsMove(posX, posY, grid, tol):
    neighborhood = neighbors(1, posX, posY, grid)
    # print('hood', end=' ')
    # print(neighborhood)
    inGroup = neighborhood[1][1]
    inGroupCount = 0 
    outGroupCount = 0
    for i in range(0,3):
        for j in range(0,3):
            if not(i == 1 and j == 1): #don't count the middle agent
                if neighborhood[i][j] == inGroup:
                    inGroupCount += 1
                elif neighborhood[i][j] != 0:
                    outGroupCount += 1
    totalNeighbors = outGroupCount + inGroupCount
    if totalNeighbors > 0:
        return inGroupCount / totalNeighbors < tol
    else:
        return False #Agent has NO neighbors, lonely, but choosing not to move

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

def nextRound(grid, tol):
    movingAgents = []
    openLocations = []
    #initialize beginning diversity tolerance
    # tol = 0.3
    # return grid
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] != 0:
                # print(i,j,agentWantsMove(i,j,grid,tol))
                if agentWantsMove(i,j,grid,tol):
                    movingAgents.append([i, j])
            else:
                openLocations.append([i,j])
    if len(movingAgents) == 0:
        # print("Found the end") #all agents are satisfied
        return False
    return agentShuffle(movingAgents, openLocations, grid)


#troubelshooting area

# grid = [[1, 1, 2], [0, 2, 2], [2, 0, 0]]
# print(grid)
# print(nextRound(grid))
# def main():
#     # grid = [[1, 1, 2], [0, 2, 2], [2, 0, 0]]
#     grid = createGrid(10,.5,1/3)
#     # print(grid)
#     for i in range(0,5):
#         plt.imshow(grid)
#         plt.colorbar()
#         plt.show()
#         grid = nextRound(grid)
#     return grid

# print(main())


