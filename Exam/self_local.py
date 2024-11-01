#!/usr/bin/env python3
import numpy as np
import numpy.random as rand
import math
from scipy.stats import norm, multivariate_normal
import matplotlib.pyplot as plt

def sampler(X, p=None, n=1000):
    if p.sum() != 1:
        p = p/p.sum()

    #print(f"{np.sum(p)=}")
    samples = []
    r = np.random.uniform(0, 1/n)
    c = p[0]
    i = 0
    for m in range(n-1):
        u = r + (m/n)
        while u > c:
            i += 1
            c += p[i]
        samples.append(X[i-1])
    return np.array(samples)


def move_sample(sample, turn, dist):
    """ DO NOT IMPORT THIS FUNCTION 
    """
    #print(f"{sample=}")
    x, y, t = sample
    return (x+np.cos(t-turn)*dist, y+np.sin(t-turn)*dist, t-turn)

def move_samples(samples, turn, dist):
    #print("move")
    return [move_sample(sample, turn, dist) for sample in samples]



def sensor_weights(samples, landmark):
    #print("sensor")
    def sense_weight(sample, landmark):
        # The robot senses a landmark;
        # with absolute position (lx,ly),
        # with relative position (rx, ry)
        lx, ly, rx, ry = landmark
        angle  = math.atan2(rx,ry)
        dist = math.dist((rx,ry),(0,0))
        sx, sy, _ = move_sample(sample, angle, dist)
        re = norm.pdf(math.dist((lx,ly),(sx,sy)), scale=0.08)
        #print(f"{re=}")
        return re

    return np.array([sense_weight(sample, landmark) for sample in samples])


def resample_map(samples, w=None, jitter=0, n=1000):

    #print("resample")
    p = w/w.sum() 
    return sampler(samples, p=p)
    #p = w/w.sum() if w else None
    #return samples[np.random.choice(len(samples), n, p=p)]

def init_map(x_range, y_range, n=1000):
    X = rand.uniform(*x_range,  n)
    Y = rand.uniform(*y_range,  n)
    T = rand.uniform(0, math.tau, n)
    return np.vstack((X,Y,T)).T

def plt_samples(r_samples):
    plt.quiver(*r_samples.T[:2], np.cos(r_samples.T[2]), np.sin(r_samples.T[2]))

    # plot the landmarks at (1,1), (1,5), (4,1), (4,5)
    plt.scatter([1,1,4,4], [1,5,1,5], c='r') 

    plt.show()

n = 1000
samples = init_map((0,5), (0,4), n)
w = np.ones(n)/n
samples = resample_map(samples, w=w)

def sense_landmark(landmark):
    global samples
    w = sensor_weights(samples, landmark)
    samples = resample_map(samples, w=w)
    print(f"{EstimatePosition()=}")
    plt_samples(samples)
def move(turn, dist):
    global samples
    samples = move_samples(samples, turn, dist)
def EstimatePosition():
    return np.array(samples).mean(axis=0)
