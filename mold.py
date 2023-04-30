import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap

# Parameters
grid_size = 100
num_food_sources = 4
growth_rate = 0.1
pruning_rate = 0.01

# Initialize grid
grid = np.zeros((grid_size, grid_size))
center_x, center_y = grid_size // 2, grid_size // 2
grid[center_x, center_y] = 1

# Generate random food sources
np.random.seed(42)
food_sources = [tuple(np.random.randint(0, grid_size, 2)) for _ in range(num_food_sources)]
for x, y in food_sources:
    grid[x, y] = 2

# Define the animation function
def animate(i):
    global grid
    new_grid = np.zeros_like(grid)
    for x in range(1, grid_size - 1):
        for y in range(1, grid_size - 1):
            if grid[x, y] > 0:
                new_grid[x, y] += grid[x, y] * (1 - growth_rate)
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx != 0 or dy != 0:
                            new_grid[x + dx, y + dy] += grid[x, y] * growth_rate / 8
    # Add food sources back to the grid
    for x, y in food_sources:
        new_grid[x, y] = 2
    grid = prune(new_grid, pruning_rate)

    # Display the current grid as an image
    im.set_array(grid)
    return [im]

# Pruning function
def prune(grid, pruning_rate):
    new_grid = np.zeros_like(grid)
    for x in range(1, grid_size - 1):
        for y in range(1, grid_size - 1):
            if grid[x, y] > 0.01:
                new_grid[x, y] = grid[x, y] * (1 - pruning_rate) + pruning_rate
    return new_grid

# Create a custom colormap for visualization
cmap = ListedColormap(['saddlebrown', 'yellow', 'red'])

# Create the animation
fig = plt.figure()
im = plt.imshow(grid, cmap=cmap, vmin=0, vmax=2)
plt.colorbar(ticks=[0, 1, 2], label='Mold Intensity')
plt.title('Physarum polycephalum Network Model')

ani = animation.FuncAnimation(fig, animate, frames=1000, interval=.1, blit=True)

plt.show()
