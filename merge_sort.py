# Visualization of the merge sort algorithm.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani

from util.style import PlotStyle

# Create a list of random integers between 0 and 100.
# In this case it will be easier to work with lists
# than numpy arrays
ogdata = list(np.random.randint(1, 100, size=25))

fig, ax = plt.subplots()
    
def merge(a, b):
    merged = []
    while len(a) and len(b):
        if a[0] < b[0]:
            merged.append(a.pop(0))
        else:
            merged.append(b.pop(0))
    while len(a):
        merged.append(a.pop(0))
    while len(b):
        merged.append(b.pop(0))
    return merged


def merge_sort_gen():
    data = [[x] for x in ogdata]
    while len(data) > 1:
        nd = []
        for i in range(len(data)):
            if i % 2 == 1:
                continue
            try:
                nd.append(merge(data[i], data[i+1]))
            except IndexError:
                nd.append(data.pop(-1))
            yield (i, nd, data)
        data = nd


def update(frame):
    i, nd, datums = frame

    flat = []
    colors = []
    for k, dat in enumerate(nd):
        flat.extend(dat)
        if k == len(nd) - 1:
            # Differentiate the section currently
            # being merged
            colors.extend([PlotStyle.RED]*len(dat))
        else:
            colors.extend([PlotStyle.BLUE]*len(dat))

    for dat in datums:
        flat.extend(dat)
        colors.extend([PlotStyle.BLUE]*len(dat))

    ax.clear()
    PlotStyle.apply(ax)
    bars = ax.bar(range(len(flat)), flat, color=colors)

_ = ani.FuncAnimation(fig, update, frames=merge_sort_gen, interval=500, blit=False)
plt.show()

