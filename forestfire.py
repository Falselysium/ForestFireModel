import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import colors

# http://web.archive.org/web/20230212225125/https://triplebyte.com/blog/how-fire-spreads-mathematical-models-and-simulators

# # neighborhood = ((-1,-1), (-1,0), (-1,1), (0,-1), (0, 1), (1,-1), (1,0), (1,1))
# # NY and NX are now neighborhood
# NY=([-1,-1,-1,
#       0,    0,
#       1, 1, 1])
# NX=([-1, 0, 1,
#      -1,    1,
#      -1, 0, 1])
# NZ=(
# [.1,.1,.1,
#  .1,    1,
#  .1, 1, 1])

# Displacements from a cell to its eight nearest neighbours
neighbourhood = ((-1, -1), (-1, 0), (-1, 1), 
                (0, -1),            (0, 1), 
                (1, -1), (1, 0), (1, 1))
# windp = [.1 if x+y<=0 else 1 for x,y in neighbourhood]
windp = [.1, .1, .1, 
        .1,    1, 
        .1, 1, 1]
print("Wind Probability", windp)
EMPTY, TREE, FIRE, WATER = 0, 1, 2, 3
colors_list = [(0.2, 0, 0), (0, 0.5, 0), (1, 0, 0), 'orange', 'blue']
cmap = colors.ListedColormap(colors_list)
bounds = [0, 1, 2, 3, 4]
norm = colors.BoundaryNorm(bounds, cmap.N)


def iterate(X):
    """Iterate the forest according to the forest-fire rules."""
    # The boundary of the forest is always empty, so only consider cells
    # indexed from 1 to nx-2, 1 to ny-2
    X1 = np.zeros((ny, nx))
    for ix in range(1, nx-1):
        for iy in range(1, ny-1):
            if X[iy, ix] == WATER:
                X1[iy, ix] = WATER
            if X[iy, ix] == EMPTY and np.random.random() <= p:
                X1[iy, ix] = TREE
            if X[iy, ix] == TREE:
                X1[iy, ix] = TREE
                for dy, dx in neighbourhood:
                    # The diagonally-adjacent trees are further away, so
                    # only catch fire with a reduced probability:
                    # if abs(dx) == abs(dy) and np.random.random() < .0567:
                    #     continue
                    if X[iy+dy, ix+dx] == FIRE and np.random.random() <= windp[neighbourhood.index((dx, dy))]:
                        X1[iy, ix] = FIRE
                        break
                else:
                    if np.random.random() <= f:
                        X1[iy, ix] = FIRE
    return X1


# The initial fraction of the forest occupied by trees.
forest_fraction = 0.2

# Probability of new tree growth per empty cell, and of lightning strike.
p, f = 0.06, 0.0005

# Forest size (number of cells in x and y directions).
nx, ny = 150, 150

# Initialize the forest grid.
X = np.zeros((ny, nx))
X[1:ny-1, 1:nx-1] = np.random.randint(0, 2, size=(ny-2, nx-2))
X[1:ny-1, 1:nx-1] = np.random.random(size=(ny-2, nx-2)) < forest_fraction

# # Water
# X[40:50, 90:100] = WATER
# X[50:60, 80:90] = WATER
# X[60:70, 70:80] = WATER
# X[70:80, 60:70] = WATER
# X[80:90, 50:60] = WATER
# X[90:100,40:50] = WATER
# X[10:90, 10:15] = WATER
# X[10:90, 40:45] = WATER
# X[10:90, 60:65] = WATER
# X[10:90, 80:85] = WATER

fig = plt.figure(figsize=(25/3, 6.25))
ax = fig.add_subplot(111)
ax.set_axis_off()
im = ax.imshow(X, cmap=cmap, norm=norm)  # , interpolation='nearest')

# The animation function: called to produce a frame for each generation.


def animate(i):
    im.set_data(animate.X)
    animate.X = iterate(animate.X)


# Bind our grid to the identifier X in the animate function's namespace.
animate.X = X

# Interval between frames (ms).
interval = 50
anim = animation.FuncAnimation(fig, animate, interval=interval, frames=100)
plt.show()
