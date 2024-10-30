import time
from itertools import accumulate
from calibration import calibration
import math
from self_local import move_samples, getSamples, setSamples


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

    #adjust for motor issue
    arlo.go_diff(lspeed,rspeed,0,1)
    time.sleep(0.2)
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
    

    setSamples(move_samples(getSamples(), 0, dist))
     
    return True


def checkSonar(arlo, stopdist):
    """ Check if any of the sonar sensors detect an object within stopdist meters

    Args:
        arlo (Robot): The robot object
        stopdist (int): The distance to check for
    """
    # print("Checking sonar")

    return (
        arlo.read_front_ping_sensor() < stopdist or
        # arlo.read_back_ping_sensor() < stopdist or 
        arlo.read_left_ping_sensor() < stopdist or 
        arlo.read_right_ping_sensor() < stopdist )
    

def rotateDeg(arlo,deg, speed=60):
    
    lspeed = speed * (1+calibration["bias"])
    rspeed = speed * (1-calibration["bias"])
    clockwise = False
    if deg>0:
        clockwise = False
        deg = abs(deg)
    else:
        clockwise = True
        deg = abs(deg)
    
    dirLeft  = 1 if clockwise else 0
    dirRight = 0 if clockwise else 1

    print("Rotating", deg, "degrees", ("clockwise" if clockwise else "countercloskwise"))
    arlo.go_diff(lspeed, rspeed, dirLeft, dirRight)

    # here we make the assumption that the robot rotates in place
    # ie the robot can not hit anything new while rotating 
    # so we can use a simple time.sleep to wait for the rotation to finish
    # this is a acceptable assumption since the robot is a circle
    # and should not be close to any objects

    time.sleep(deg/calibration["rotation_speed"])
    
    arlo.stop()
    time.sleep(0.5)

        
    setSamples(move_samples(getSamples, deg, 0))



def getPath(path):
    """
    This function takes a list of [x,y] coordinates,
    and returns a list of angles and a list of distances
    that create a path of how arlo should move
    """
    # Start at 90 degrees (facing the positive y-axis)
    current_angle = 90
    angles_to_turn = []
    distances_to_move = []

    # Iterate through the list of path
    for i in range(1, len(path)):
        # Current and next point
        x1, y1 = path[i - 1]
        x2, y2 = path[i]
        
        # Calculate target angle relative to positive y-axis
        delta_x = x2 - x1
        delta_y = y2 - y1
        target_angle = math.degrees(math.atan2(delta_y, delta_x))  # angle relative to x-axis

        # Calculate the angle difference relative to the current angle
        angle_difference = target_angle - current_angle

        # Adjust angle difference for shortest rotation (between -180 and 180)
        if angle_difference > 180:
            angle_difference -= 360
        elif angle_difference < -180:
            angle_difference += 360

        # Calculate the distance to move
        distance = math.sqrt(delta_x ** 2 + delta_y ** 2)

        # Store the angle to turn and distance to move
        angles_to_turn.append(angle_difference)
        distances_to_move.append(distance)

        # Update the current angle to face the target direction
        current_angle += angle_difference

    return angles_to_turn, distances_to_move




def MovePath(arlo,path):
    angles,dists = getPath(path)
    print(angles)
    for i in range(len(angles)):
        rotateDeg(arlo,angles[i])
        time.sleep(0.2)
        finished =  goDist(arlo,dists[i])
         if not finished:
         # TODO a better way to handle this
            return False

