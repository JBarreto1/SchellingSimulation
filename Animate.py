import random
import numpy as np

import matplotlib
import matplotlib.pyplot as plt

import matplotlib.animation as animation

import copy

import schelling

fps = 10
nSeconds = 5
grid = schelling.createGrid(9)
plot=[grid]
for _ in range((nSeconds * fps) - 1):
    newGrid = copy.deepcopy(schelling.nextRound(grid)) 
    plot.append(newGrid)
    grid = newGrid
# plot = [nextRound(grid) for _ in range( nSeconds * fps ) ]
# for i in range(len(plot)):
#     print(i, end=' ')
#     print(plot[i])

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

writergif = animation.PillowWriter(fps=30)
anim.save('filename.gif',writer=writergif)

print('Done!')

# plt.show()  # Not required, it seems!