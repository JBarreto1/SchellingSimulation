import random
import numpy as np

import matplotlib
import matplotlib.pyplot as plt

import matplotlib.animation as animation

import copy

import schelling

#initialize model parameters
gridSize = 50
tol = .3
groupRatio = .5
percentEmpty = .1

fps = 7
# nSeconds = 4
grid = schelling.createGrid(gridSize,groupRatio,percentEmpty)
plot=[grid]
# for _ in range((nSeconds * fps) - 1):
#     newGrid = copy.deepcopy(schelling.nextRound(grid)) 
#     plot.append(newGrid)
#     grid = newGrid

endNotFound = True
maxIter = 40 #don't let it run away if something is wrong and it takes a long time
for i in range(maxIter):
    #build the series of plots and either get to a point where all agents are satisfied or max iterations is hit
    newGrid = copy.deepcopy(schelling.nextRound(grid, tol)) 
    if newGrid:
        plot.append(newGrid)
        grid = newGrid
    else:
        break

#keep the GIF to a whole number of seconds, and use the remainder time to show the steady state grid (all satisfied agents)
for i in range(fps - (len(plot) % fps)):
    plot.append(grid)

nSeconds = int(len(plot) / fps)

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure( figsize=(9,9) )

a = plot[0]
im = plt.imshow(a, vmin=0, vmax=2)

def animate_func(i):
    if i % fps == 0:
        print( '.', end ='' )
    im.set_array(plot[i])
    return [im]



anim = animation.FuncAnimation(
                               fig, 
                               animate_func,
                               frames = nSeconds * fps,
                               interval = 1000 / fps, # in ms
                               )

writergif = animation.PillowWriter(fps=fps)
anim.save('filename.gif',writer=writergif)

print('Done!')

# plt.show()  # Not required, it seems!