# Visualization of the RanSaC algorithm in one dimension.
# (RanSaC stands for Random Sample Consensus).
# 
# RanSaC is meant for dealing with situations where 
# taking the average (or doing the linear regression in 2d)
# would be misleading due to outliers.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani

from util.style import PlotStyle

# Create inlier and outlier data, put them together
inlier_data = ((np.random.rand(40) * 100) % 30) + 10  # 40 numbers between 10 and 40
outlier_data = ((np.random.rand(10) * 100) % 20) + 80  # 10 numbers between 80 and 95

data = np.concatenate((inlier_data, outlier_data))

# Constants
TOL = 15  # Tolerance for what counts as an inliner
SAMPLES = 20  # How many samples to take
Y = np.zeros(len(data))  # This is 1d, so all y values are 0

# Initialize the figure
fig, ax = plt.subplots()

def ransac_1d_gen():
    sample_count = 0
    samples_inliers = []  # List of tuples to be sorted later

    # Take random samples
    while sample_count < SAMPLES:
        sample_count += 1
        sample_val = np.random.choice(data)
        inliers = [x for x in data if abs(x - sample_val) <= TOL]
        samples_inliers.append((len(inliers), sample_val))
        yield (
            'Sample {} | Value {:0.2f} | Inliers {}'.format(sample_count, sample_val, len(inliers)), 
            sample_val, 
            inliers,
            False
        )

    # Now that we're done sampling, find the one 
    # with the most inliers (e.g. the 'consensus')
    sorted_inliers = sorted(samples_inliers)
    best = sorted_inliers[-1]
    best_inliers = [x for x in data if abs(x - best[1]) <= TOL]
    # Take the average of the inliers for this best value
    avg = np.average(best_inliers)
    # The graph should now show the average
    yield(
        'Best value {:0.2f} | Average of inliers {:0.2f} | Average of dataset {:0.2f}'
            .format(best[1], avg, np.average(data)), 
        avg,
        best_inliers,
        True
    )


def update(frame):
    title = frame[0]
    sample_val = frame[1]
    inliers = frame[2]
    is_end = frame[3]
    
    # Redraw the plot
    ax.clear()
    ax.set_xlim(0, 100)
    ax.set_ylim(1, -1)
    PlotStyle.apply(ax)
    colors = [PlotStyle.BLUE if x not in inliers else PlotStyle.RED for x in data]
    ax.scatter(data, Y, marker='|', c=colors)
    ax.set_title(title)
    ax.axvline(x=sample_val, color=PlotStyle.RED) # current sample
    

    # If done, show the average of the whole dataset 
    # to demonstrate the value of this algo
    if is_end:
        ax.axvline(x=np.average(data), color=PlotStyle.ORANGE, linestyle='--')
    

_ = ani.FuncAnimation(fig, update, frames=ransac_1d_gen, interval=300, blit=False, repeat=False)
plt.show()
