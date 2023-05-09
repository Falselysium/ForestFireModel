import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import colors
# Generate a random river path using Perlin noise
from noise import pnoise2

# Displacements from a cell to its eight nearest neighbours (y, x)
neighbourhood = (
    (-1, -1), (-1, 0), (-1, 1),
    ( 0, -1),          ( 0, 1),
    ( 1, -1), ( 1, 0), ( 1, 1)
    )

# windp = [.1 if x+y<=0 else 1 for x,y in neighbourhood]
windp = [
    .1, .1, .1,
    .1,    .1,
    .9, .7, .7
    ]

print("Wind Probability", windp)
EMPTY, TREE, FIRE, WATER = 0, 1, 2, 3
colors_list = [(0.2, 0, 0), (0, 0.5, 0), (1, 0, 0), 'orange', 'blue']
cmap = colors.ListedColormap(colors_list)
bounds = [0, 1, 2, 3, 4]
norm = colors.BoundaryNorm(bounds, cmap.N)


def iterate(X):
    """Iterate the forest according to the forest-fire rules."""
    X1 = np.zeros((ny, nx))
    for ix in range(1, nx-1):
        for iy in range(1, ny-1):
            if X[iy, ix] == WATER:
                X1[iy, ix] = WATER
            elif X[iy, ix] == EMPTY and np.random.random() <= p:
                X1[iy, ix] = TREE
            elif X[iy, ix] == TREE:
                X1[iy, ix] = TREE
                if np.random.random() <= f:
                    X1[iy, ix] = FIRE
                    continue

                for dy, dx in neighbourhood:
                    if X[iy+dy, ix+dx] == FIRE and np.random.random() <= windp[neighbourhood.index((dy, dx))]:
                        X1[iy, ix] = FIRE
                        break
    return X1

# The initial fraction of the forest occupied by trees.
forest_fraction = 0.2

# Probability of new tree growth per empty cell, and of lightning strike.
p, f = 0.03, 0.00005

# Forest size (number of cells in x and y directions).
nx, ny = 150, 150

# Initialize the forest grid.
X = np.zeros((ny, nx))
X[1:ny-1, 1:nx-1] = np.random.randint(0, 2, size=(ny-2, nx-2))
X[1:ny-1, 1:nx-1] = np.random.random(size=(ny-2, nx-2)) < forest_fraction


# ##########################################################################
# ##########################################################################
# # Water
# # X[10:90, 10:15] = WATER
# # X[10:90, 40:45] = WATER
# # X[10:90, 60:65] = WATER
# # X[10:90, 80:85] = WATER
scale = 40    # Controls the frequency of the noise
octaves = 2   # Controls the detail of the noise
persistence = 0.3  # Controls the roughness of the noise
lacunarity = 8.0    # Controls the frequency multiplier between octaves
for i in range(150):
    for j in range(150):
        x = i / scale
        y = j / scale
        noise_val = pnoise2(x, y, 
                            octaves=octaves, 
                            persistence=persistence, 
                            lacunarity=lacunarity, 
                            repeatx=150, 
                            repeaty=150)
        if noise_val < -0.2:    # Set cells below a certain noise threshold to water
            X[i, j] = 3
##########################################################################
##########################################################################
            
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
interval = 30
anim = animation.FuncAnimation(fig, animate, interval=interval, frames=100)
plt.show()
