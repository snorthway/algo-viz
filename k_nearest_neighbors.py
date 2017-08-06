# Visualization of the k-nearest neighbors algorithm in 2d,
# commonly used for classifying new data based on sample data.
from collections import Counter

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani

from util.helpers import rand_between, distance_2d
from util.style import PlotStyle

# Create some clusters
c1_x = rand_between(n=30, low=10, high=25)
c1_y = rand_between(n=30, low=20, high=45)
ct_pts = zip(c1_x, c1_y)

c2_x = rand_between(n=45, low=25, high=50)
c2_y = rand_between(n=45, low=45, high=80)
c2_pts = zip(c2_x, c2_y)

c3_x = rand_between(n=20, low=70, high=95)
c3_y = rand_between(n=20, low=40, high=60)
c3_pts = zip(c3_x, c3_y)

# Cat that shit
x_data = np.concatenate((c1_x, c2_x, c3_x))
y_data = np.concatenate((c1_y, c2_y, c3_y))
data = zip(x_data, y_data)

print(len(data))

# Constants
K = 5  # number of neighbors to consider
SAMPLES = 10  # number of samples to show in animation

fig, ax = plt.subplots()

def cluster_color(pt):
    if pt[0] in c1_x and pt[1] in c1_y:
        return PlotStyle.RED
    if pt[0] in c2_x and pt[1] in c2_y:
        return PlotStyle.GREEN
    if pt[0] in c3_x and pt[1] in c3_y:
        return PlotStyle.ORANGE
    raise RuntimeError('this point should not exist: {}'.format(pt))

def best_cluster_color(best_k):
    points = [bk[1] for bk in best_k]
    colors = [cluster_color(pt) for pt in points]
    # https://stackoverflow.com/a/20872750/1763621
    data = Counter(colors)
    return data.most_common(1)[0][0]

def knn_gen():
    sample_count = 0
    while sample_count < SAMPLES:
        s_x = np.random.random() * 100
        s_y = np.random.random() * 100
        all_pts = []
        for datum in data:
            dist = distance_2d(s_x, datum[0], s_y, datum[1])
            all_pts.append((dist, datum))
        best_k = sorted(all_pts)[:K]

        sample_count += 1

        yield (s_x, s_y, best_k)

def update(frame):
    s_x, s_y, best_k = frame
    neighbor_datums = zip(*best_k)[1]
    neighbors = zip(*neighbor_datums)
    nx = list(neighbors[0])
    ny = list(neighbors[1])

    # Plot that shit
    ax.clear()
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    PlotStyle.apply(ax)
    ax.scatter(nx, ny, c='white', s=30)
    ax.scatter(c1_x, c1_y, c=PlotStyle.RED, s=10)
    ax.scatter(c2_x, c2_y, c=PlotStyle.GREEN, s=10)
    ax.scatter(c3_x, c3_y, c=PlotStyle.ORANGE, s=10)
    ax.scatter([s_x], [s_y], c=best_cluster_color(best_k), s=30)
    ax.scatter([s_x], [s_y], c='white', s=10)

_ = ani.FuncAnimation(fig, update, frames=knn_gen, interval=1000, blit=False)
plt.show()


    


