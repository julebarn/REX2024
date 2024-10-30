#!/usr/bin/env python3
import numpy as np
import math
from scipy.stats import norm, multivariate_normal

def sampler(X, p=0, n=1000):
    samples = []
    r = rand.uniform(0, 1/n)
    c = p[0]
    i = 0
    for m in range(n-1):
        u = r + (m/n)
        while u > c:
            i += 1
            c += p[i-1]
        samples.append(X[i-1])
    return np.array(samples)


def move_sample(sample, turn, dist):
        """ DO NOT IMPORT THIS FUNCTION 
        """
        x, y, t = sample
        return (x+np.cos(t-turn)*dist, y+np.sin(t-turn)*dist, t-turn)

def move_samples(samples, turn, dist):
    return [move_sample(sample, turn, dist) for sample in samples]



def sensor_weights(samples, landmark):
    def sense_weight(sample, landmark):
        # The robot senses a landmark;
        # with absolute position (lx,ly),
        # with relative position (rx, ry)
        lx, ly, rx, ry = landmark
        angle, dist = math.atan(rx/ry), math.dist(rx,ry)
        sx, sy, _ = move_sample(sample, angle, dist)
        return norm.pdf(math.dist((lx,ly),(sx,sy)), scale=.2)

    return [sense_weight(sample, landmark) for sample in samples]


def resample_map(samples, w=None, jitter=0, n=1000):
    p = w/w.sum() if w else None
    return samples[np.random.choice(len(samples), n, p=p)]

def init_map(loc, var, n=1000):
    X = rand.normal(loc, var, (n, len(var)))
    W = multivariate_normal(loc, var).pdf(X)
    X = np.hstack((X,rand.uniform(0, math.tau, n)[np.newaxis].T))
    return sampler(X, p=W/W.sum())


# 👇 below comment refers to code below this line 👇
# no this is not bad code it use the singleton pattern 
# here seen being implemented with out a class 
# and the singletonnes being enforced by the module system and runtime 😛
# so this code is actually genius level code 😎
# let your mortel eyes gaze upon the glory of the code below 
# and be humbled by its elegance 🤯

n = 1000
samples = init_map((0,0), (2,2), n)

def getSamples():
    return samples

def setSamples(s):
    samples = s
    print(f"EstimatePosition: {EstimatePosition()}")

def EstimatePosition():
    return samples.mean(axis=0)
