import numpy as np

def rand_between(n=50, low=0, high=100):
    """
    The 'high' and 'low' are just a readability
    thing, I will create this array even if you
    fuck it up
    """
    dif = abs(high - low)
    return ((np.random.rand(n) * 100) % dif) + (low if low < high else high)

def distance_2d(x1, x2, y1, y2):
    """
    Compute the distance between 2 points.
    """
    return np.sqrt((x2-x1)**2+(y2-y1)**2)

def distance(v1, v2):
    """
    Finds the distance between two vectors
    of any size.
    """

    # Get the x's, y's, z's, etc. together
    pairs = np.transpose(np.array([v1, v2]))
    # Distance formula
    return np.sqrt( sum([ (p[1] - p[0]) ** 2 for p in pairs]) )