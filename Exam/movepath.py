import time
from itertools import accumulate
from calibration import calibration
import math


def goDist(arlo,dist, speed=60, stopdist = 500):
    """Move the robot a distance in meters 
    If a object is detected within stopdist meters the robot stops and returns False
    Otherwise it returns True

    Args:
        arlo (Robot): The robot object
        dist (float): The distance to move in meters
        speed (int, optional): The speed of the robot. Defaults to 60.
        stopdist (int, optional): The distance to stop if an object is detected. Defaults to 500mm
    """

    print("Going", dist, "meters")

    if checkSonar(arlo, stopdist):
        arlo.stop()
        return False

    lspeed = speed * (1+calibration["bias"])
    rspeed = speed * (1-calibration["bias"])

    arlo.go_diff(lspeed,rspeed,0,1)
    time.sleep(0.05)
    stopTime = time.time() + calibration["speed"]*dist
    
    arlo.go_diff(lspeed,rspeed, 1, 1)

    while time.time() < stopTime:
        if checkSonar(arlo, stopdist):
            print("Object detected")
            arlo.stop()
            return False

        time.sleep(0.1)
    
    arlo.stop()
    time.sleep(0.5)
    return True


def checkSonar(arlo, stopdist):
    """ Check if any of the sonar sensors detect an object within stopdist meters

    Args:
        arlo (Robot): The robot object
        stopdist (int): The distance to check for
    """
    print("Checking sonar")

    return (
        arlo.read_front_ping_sensor() < stopdist or
        # arlo.read_back_ping_sensor() < stopdist or 
        arlo.read_left_ping_sensor() < stopdist or 
        arlo.read_right_ping_sensor() < stopdist )
    

def rotateDeg(arlo,deg, speed=60, clockwise=False):
    print("Rotating", deg, "degrees", ("clockwise" if clockwise else "countercloskwise"))
    
    lspeed = speed * (1+calibration["bias"])
    rspeed = speed * (1-calibration["bias"])

    dirLeft  = 1 if clockwise else 0
    dirRight = 0 if clockwise else 1

    arlo.go_diff(lspeed, rspeed, dirLeft, dirRight)

    # here we make the assumption that the robot rotates in place
    # ie the robot can not hit anything new while rotating 
    # so we can use a simple time.sleep to wait for the rotation to finish
    # this is a acceptable assumption since the robot is a circle
    # and should not be close to any objects

    if clockwise:
        time.sleep(deg/calibration["rotation_speed_clock"])
    else:
        time.sleep(deg/calibration["rotation_speed_anticlock"])
    
    arlo.stop()
    time.sleep(0.5)


def movement(prev_state, p):
    prev, angle, d = prev_state

    if (prev[1]-p[1]) == 0:
        return (p, 0, math.dist(prev, p))
    
    return (p,
            math.degrees(math.atan2((prev[0]-p[0]),(prev[1]-p[1]))) - angle,
            math.dist(prev, p))


def MovePath(arlo,path):
    for _, turn, dist in accumulate(path, movement, initial=((0,0),0,0)):
        clockwise = False if turn < 0 else True
        turn = abs(turn)        
    
        rotateDeg(arlo,turn,60,clockwise)
        finished = goDist(arlo,dist)
        if not finished:
            # TODO a better way to handle this
            break
