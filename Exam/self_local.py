#!/usr/bin/env python3
import numpy as np
import numpy.random as rand
import math
from scipy.stats import norm, multivariate_normal

def sampler(X, p=None, n=1000):
    print(f"{np.sum(p)=}")
    samples = []
    r = np.random.uniform(0, 1/n)
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
    print(f"{sample=}")
    x, y, t = sample
    return (x+np.cos(t-turn)*dist, y+np.sin(t-turn)*dist, t-turn)

def move_samples(samples, turn, dist):
    print("move")
    return [move_sample(sample, turn, dist) for sample in samples]



def sensor_weights(samples, landmark):
    print("sensor")
    def sense_weight(sample, landmark):
        # The robot senses a landmark;
        # with absolute position (lx,ly),
        # with relative position (rx, ry)
        lx, ly, rx, ry = landmark
        angle  = math.atan2(rx,ry)
        dist = math.dist((rx,ry),(0,0))
        sx, sy, _ = move_sample(sample, angle, dist)
        re = norm.pdf(math.dist((lx,ly),(sx,sy)), scale=.2)
        print(f"{re=}")
        return re

    return np.array([sense_weight(sample, landmark) for sample in samples])


def resample_map(samples, w=None, jitter=0, n=1000):
<<<<<<< HEAD
    print("resample")
    p = w/w.sum() if w.all() else np.ones(len(samples)) / len(samples)
    return sampler(samples, p=p)
    #p = w/w.sum() if w else None
    #return samples[np.random.choice(len(samples), n, p=p)]
def init_map(loc, var, n=1000):
    X = np.random.normal(loc, var, (n, len(var)))
    W = multivariate_normal(loc, var).pdf(X)
    X = np.hstack((X,np.random.uniform(0, math.tau, n)[np.newaxis].T))
    return sampler(X, p=W/W.sum())
=======
    p = w/w.sum() if w else None
    return samples[np.random.choice(len(samples), n, p=p)]

def init_map(x_range, y_range, n=1000):
    X = rand.uniform(0, x_range,  n)
    Y = rand.uniform(0, y_range,  n)
    T = rand.uniform(0, math.tau, n)
    return np.vstack((X,Y,T)).T
>>>>>>> b3f7c6f9ada1e19848047c4f0a889fa91b4f882b


n = 1000
samples = init_map((0,0), (2,2), n)

def sense_landmark(landmark):
    global samples
    w = sensor_weights(samples, landmark)
    samples = resample_map(samples, w=w)
def move(turn, dist):
    global samples
    samples = move_samples(samples, turn, dist)
def EstimatePosition():
    return np.array(samples).mean(axis=0)
