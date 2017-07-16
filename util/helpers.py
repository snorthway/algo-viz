import numpy as np

def rand_between(n=50, low=0, high=100):
    """
    The 'high' and 'low' are just a readability
    thing, I will create this array even if you
    fuck it up
    """
    dif = abs(high - low)
    return ((np.random.rand(n) * 100) % dif) + (low if low < high else high)