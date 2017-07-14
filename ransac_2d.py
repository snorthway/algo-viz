# Visualization of the RanSaC algorithm in one dimension.
# (RanSaC stands for Random Sample Consensus).
# 
# RanSaC is meant for dealing with situations where 
# taking the average (or doing the linear regression in 2d)
# would be misleading due to outliers.

from random import choice
from functools import partial

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani
from scipy.stats import linregress

from util.style import PlotStyle

# Create inlier and outlier data, put them together
slope = 2
wiggle = 15
inlier_x_data = np.random.rand(50) * 100
inlier_y_data = inlier_x_data * slope + np.random.uniform(
                                        low=-wiggle, 
                                        high=wiggle, 
                                        size=len(inlier_x_data))
outlier_x_data = ((np.random.rand(20) * 100) % 30) + 60
outlier_y_data = (np.random.rand(len(outlier_x_data)) * 100) % 30

x_data = np.concatenate((inlier_x_data, outlier_x_data))
y_data = np.concatenate((inlier_y_data, outlier_y_data))
data = zip(x_data, y_data) # tuple of coordinate pairs

# Constants
TOL = 5  # Tolerance for what counts as an inlier
SAMPLES = 20  # How many samples to take

# Initialize the figure
fig, ax = plt.subplots()

def distance_from_line(c1, c2, c3):
    x1, y1 = c1
    x2, y2 = c2
    x3, y3 = c3
    
    num = np.abs((y2-y1)*x3 - (x2-x1)*y3 + x2*y1 - y2*x1)
    den = np.sqrt((y2-y1)**2 + (x2-x1)**2)

    return num/den

def get_inliers(cp1, cp2, data):
    dist = partial(distance_from_line, cp1, cp2)
    return [d for d in data if dist(d) <= TOL]


def ransac_2d_gen():
    sample_count = 0
    samples_inliers = []  # List of tuples to be sorted later

    # Take random samples
    while sample_count < SAMPLES:
        sample_count += 1
        pt1 = choice(data)
        pt2 = choice(data)
        inliers = get_inliers(pt1, pt2, data)
        samples_inliers.append((len(inliers), pt1, pt2))
        yield (
            'Sample {} | Inliers {}'.format(sample_count, len(inliers)), 
            pt1,
            pt2, 
            inliers,
            False
        )

    # Now that we're done sampling, find the line 
    # with the most inliers (e.g. the 'consensus')
    sorted_inliers = sorted(samples_inliers)
    best = sorted_inliers[-1]
    num_inliers, cp1, cp2 = best
    best_inliers = get_inliers(cp1, cp2, data)
    # Do linear regression on the best inliers
    in_x, in_y = zip(*best_inliers)
    slope, intercept, _, _, _ = linregress(in_x, in_y)
    d_slope, d_intercept, _, _, _ = linregress(x_data, y_data)
    # The graph should now show the best fit of the entire data set
    yield(
        'Line: y = {:0.2f}x + {:0.2f}'
            .format(slope, intercept), 
        (slope, intercept),
        (d_slope, d_intercept),
        best_inliers,
        True
    )


def update(frame):
    title = frame[0]
    pt1 = frame[1]
    pt2 = frame[2]
    inliers = frame[3]
    is_end = frame[4]

    if not is_end:
        x1, y1 = pt1
        x2, y2 = pt2
        
        # Redraw the plot
        ax.clear()
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 200)
        PlotStyle.apply(ax)
        colors = [PlotStyle.BLUE if x not in inliers else PlotStyle.RED for x in data]
        ax.scatter(x_data, y_data, c=colors)
        ax.set_title(title)
        # plot the line between the 2 points
        ax.plot([x1, x2], [y1, y2], color=PlotStyle.BLUE, linestyle='-')
    
    else:
        slope, intercept = pt1
        d_slope, d_intercept = pt2
        # Redraw the plot
        ax.clear()
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 200)
        PlotStyle.apply(ax)
        colors = [PlotStyle.BLUE if x not in inliers else PlotStyle.RED for x in data]
        ax.scatter(x_data, y_data, c=colors)
        ax.set_title(title)
        # plot the line between the 2 points
        ax.plot(x_data, x_data * slope + intercept, color=PlotStyle.BLUE, linestyle='-')
        ax.plot(x_data, x_data * d_slope + d_intercept, color=PlotStyle.ORANGE, linestyle='--')

_ = ani.FuncAnimation(fig, update, frames=ransac_2d_gen, interval=300, blit=False, repeat=False)
plt.show()
