import time
from itertools import accumulate
from calibration import calibration
import math



def goDist(arlo,dist, speed=60):
    # this needs to include the sonar sensor 
    # TODO REWRITE
    print("Going", dist, "meters")
    arlo.go_diff(speed * (1+calibration["bias"]),speed * (1-calibration["bias"]), 1, 1)
    time.sleep(calibration["speed"]*dist)
    arlo.stop()
    time.sleep(0.5)

def rotateDeg(arlo,deg, speed=60, clockwise=False):
    print("Rotating", deg, "degrees", ("clockwise" if clockwise else "countercloskwise"))
    if deg < 5:
        return
    
    arlo.go_diff(speed * (1+calibration["bias"]),speed * (1-calibration["bias"]), 
                0 if clockwise else 1,
                1 if clockwise else 0)
    time.sleep(deg/calibration["rotation_speed"])
    arlo.stop()
    time.sleep(0.5)


def movement(prev_state, p):
    prev, angle, d = prev_state
    if (prev[1]-p[1]) == 0:
        return (p,
            0,
            math.dist(prev, p))
    return (p,
            math.degrees(math.atan((prev[0]-p[0])/(prev[1]-p[1]))) - angle,
            math.dist(prev, p))


def MovePath(arlo,path):
    for _, turn, dist in accumulate(path, movement, initial=((0,0),0,0)):
        clockwise = False
        if turn<0:
            clockwise = True
            turn = -turn 

    rotateDeg(arlo,turn,60,clockwise)
    goDist(arlo,dist)
