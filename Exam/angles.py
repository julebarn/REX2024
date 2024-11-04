#!/usr/bin/env python3
import numpy as np


def est_angles(angles, bins=40):
    bin_size  = (2*np.pi)/bins
    estimates = np.array(
        [np.mod(angles + (i*bin_size), 2*np.pi).mean() - (i*bin_size)
         for i in range(bins)]
    )
    return min(
        [(np.delete(estimates, i).mean(), estimates[i]) for i in range(bins)],
        key = lambda x: x[0] - x[1]
    )[0]

if __name__ == "__main__":
    a = np.mod(np.random.normal(0, 2, (1000)), 2*np.pi)
    est_angles(a)
