#!/usr/bin/env python3
import numpy as np
import numpy.random as rand
import math
from scipy.stats import norm, multivariate_normal
import matplotlib.pyplot as plt

def move_sample(sample, turn, dist):
    angle_u1, dist_u, angle_u2 = .08, .05, .08
    x, y, t = sample
    t2 = t - turn + np.random.normal(0, angle_u1)
    d2 = np.random.normal(1, dist_u) * dist
    x2 = x + np.sin(t2)*d2
    y2 = y + np.cos(t2)*d2
    t3 = t2 + np.random.normal(0, angle_u2)
    return (x2,y2,t3)

def move_samples(samples, turn, dist):
    return [move_sample(sample, turn, dist) for sample in samples]

def sensor_weights(samples, landmark):
    def sense_weight(sample, landmark):
        # The robot senses a landmark;
        # with absolute position (lx,ly),
        # with relative position (rx, ry)
        lx, ly, rx, ry = landmark
        angle  = math.atan2(rx,ry)
        dist = math.dist((rx,ry),(0,0))
        sx, sy, _ = move_sample(sample, angle, dist)
        re = norm.pdf(math.dist((lx,ly),(sx,sy)), scale=0.1)
        return re
    return np.array([sense_weight(sample, landmark) for sample in samples])

def resample_map(samples, w=None, jitter=0, n=1000):
    p = w/w.sum()
    smp = np.array(samples)[np.random.choice(len(samples), n, p=p)] 
    smp = smp + np.random.normal(0, 0.1, smp.shape)
    return smp

def init_map(x_range, y_range, n=1000):
    X = rand.uniform(*x_range,  n)
    Y = rand.uniform(*y_range,  n)
    T = rand.uniform(0, math.tau, n)
    return np.vstack((X,Y,T)).T

def plt_samples(r_samples):
    #r_samples = r_samples + np.random.normal(0, 0.1, r_samples.shape)
    plt.quiver(*r_samples.T[:2], np.cos(r_samples.T[2]), np.sin(r_samples.T[2]))

    pos = EstimatePosition()
    x,y,_ = pos
    plt.scatter(x,y,c="b")
    # plot the landmarks at (1,1), (1,5), (4,1), (4,5)
    plt.scatter([1,1,4,4], [1,5,1,5], c='r') 
    plt.show()

n = 20_000
samples = init_map((0,6), (0,5), n)

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
