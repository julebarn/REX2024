#!/usr/bin/env python3

from robot import Robot
from time import sleep
import json

arlo = Robot()

class Agent():
    def __init__(self, robot, config=None):
        self.robot = robot

    def move(speed=100, length=1)

def calibrate_differential(agent=arlo):
    speed = 100
    bias = .0
    res  = .1

    agent.go_diff(100,100, 1, 1)
    sleep(1)
    agent.stop()

    for i in range(5):
        agent.go_diff(100 * (1+bias),100 * (1-bias), 1, 1)
        sleep(1)
        agent.stop()
        if input("Drifting left? [y/n] ") == "y":
            bias += res
        else:
            bias -= res
        res /= 2

    return bias

calibrate_differential()


def calibrate_speed(agent=arlo):
    speed = 100
    time = 2

    for i in range(5):
