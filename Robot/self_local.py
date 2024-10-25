#!/usr/bin/env python3
import numpy as np
import math
from scipy.stats import norm


def move_samples(samples, turn, dist):
    def move_sample(sample, turn, dist):
        x, y, t = sample
        return (x+np.cos(t-turn)*dist, y+np.sin(t-turn)*dist, t-turn)

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
