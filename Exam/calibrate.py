#!/usr/bin/env python3

from robot import Robot
from time import sleep
import json
import numpy as np
from calibration import calibration

arlo = Robot()

class Agent():
    # Non blocking
    def __init__(self, robot, config=None):
        self.robot = robot
        self.topspeed = config["topspeed"]

    def move(length_m):
        pass

    def turn(degrees):
        pass

    def stop():
        # Clear queue
        pass

    def curve(to_point, to_angle):
        pass

def calibrate_differential(agent=arlo):
    speed = 60
    bias = .0
    res  = .1


    for i in range(5):
        #adjust for motor issue
        #agent.go_diff(speed,speed,0,1)
        #sleep(0.175)
        
        #start calib
        agent.go_diff(speed * (1+bias),speed * (1-bias), 1, 1)
        sleep(4)
        agent.stop()
        if input("Drifting left? [y/n] ") == "y":
            bias += res
        else:
            bias -= res
        res /= 2

    return bias

def calibrate_speed(agent=arlo):
    # returns time to move 1 meter
    speed = 60
    lspeed = speed * (1+calibration["bias"])
    rspeed = speed * (1-calibration["bias"])
    time = 2.5
    bias = 1.5


    for i in range(4):
        
        print(f"{time=}")
        #adjust for motor issue
        agent.go_diff(lspeed,rspeed,0,1)
        sleep(0.4)
        agent.stop()
        agent.go_diff(lspeed, rspeed, 1, 1)
        sleep(time)
        agent.stop()
        if input("Above 1 meter [y/n] ") == "y":
            time -= bias
        else:
            time += bias
        bias /= 2

    return time


def calibrate_rotation(agent=arlo):
    # returns time over degrees regression
    full_rotation = .85
    offset = 0.2

    # agent.go_diff(100,100, 1, 0)
    # sleep(full_rotation)
    # agent.stop()

    res = []

    for n in range(2):
        for i in range(2,5):
            agent.go_diff(60, 60, 0, 1)
            sleep(full_rotation / i)
            agent.stop()
            res.append((i, int(input("Degrees turned?: "))))

    return np.polyfit(*np.array(res).T, 1)

if __name__ == "__main__":
    #print(calibrate_differential(arlo))
    #print(calibrate_speed())
    calibrate_rotation()
