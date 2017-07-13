# Visualization of the bubble sort algorithm.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani

from util.style import PlotStyle

# Create a list of random integers between 0 and 100
data = np.random.randint(1, 100, size=20)
sorted_data = sorted(data)

# Create the figure
fig, ax = plt.subplots()

def bubble_sort_gen():
    """
    This will be a generator function,
    yielding the updated array in the bubble sort.
    """
    is_sorted = False    
    iter_count = 0
    while not is_sorted:
        iter_count += 1
        for i in range(len(data) - 1):
            if data[i] > data[i+1]:
                tmp = data[i+1]
                data[i+1] = data[i]
                data[i] = tmp
            yield (data, i, iter_count)
        is_sorted = reduce(lambda x, y: x and y, data == sorted_data, True)


def update(frame):
    """
    frame is the (data, i, iter_count) tuple
    """
    datums, i, iter_count = frame
    ax.clear()
    PlotStyle.apply(ax)
    bars = ax.bar(range(len(data)), datums)
    for k in range(len(data)):
        if k == i+1:
            bars[k].set_color(PlotStyle.RED)
        else:
            bars[k].set_color(PlotStyle.BLUE)
    
    ax.set_title('Iteration number {}'.format(iter_count))

_ = ani.FuncAnimation(fig, update, frames=bubble_sort_gen, interval=5, blit=False, repeat=False)
plt.show()