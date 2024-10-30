#!/usr/bin/env python3
import numpy as np
import math
from scipy.stats import norm


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



# 👇 below comment refers to code below this line 👇
# no this is not bad code it use the singleton pattern 
# here seen being implemented with out a class 
# and the singletonnes being enforced by the module system and runtime 😛
# so this code is actually genius level code 😎
# let your mortel eyes gaze upon the glory of the code below 
# and be humbled by its elegance 🤯

n = 1000
samples = resample_map(np.array([(1+x*13,1+y*13,t*2*math.pi)for x,y,t in np.random.rand(n,3)]))

def getSamples():
    return samples

def setSamples(s):
    samples = s
    print(f"EstimatePosition: {EstimatePosition()}")

def EstimatePosition():
    return samples.mean(axis=0)