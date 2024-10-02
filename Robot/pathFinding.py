import cv2
import math
import numpy as np
from robot import Robot 
from functools import partial
import time
from calibration import calibration
from picamera2 import Picamera2, Preview
from itertools import accumulate
from RRT import *
from calibration import calibration



aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
parameters = cv2.aruco.DetectorParameters_create()

bias  = calibration["bias"]
speed = 100

def movement(prev_state, p):
    prev, angle, d = prev_state
    if (prev[1]-p[1]) == 0:
        return (p,
            math.degrees(math.atan((prev[0]-p[0])/0.0001)) - angle,
            math.dist(prev, p))
    return (p,
            math.degrees(math.atan((prev[0]-p[0])/(prev[1]-p[1]))) - angle,
            math.dist(prev, p))


def cameraMatrix(focal_length, center=(320,240)):
    f = focal_length
    cx, cy = center
    return np.array([
        [f, 0, cx],
        [0, f, cy],
        [0, 0, 1 ]
    ])

try:
    arlo
except NameError:
    arlo = Robot()

try:
    cam
except NameError:
    cam = Picamera2()
    cam.start()

img = cam.capture_array()
img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
corners, ids, _ = cv2.aruco.detectMarkers(img, aruco_dict, parameters=parameters)

cmat = cameraMatrix(1273) # TODO calibrate
dcof = np.array([0,0,0,0])

rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners, .145, cmat, dcof)

def getCenter(rvec, tvec):
    rotation_matrix, _ = cv2.Rodrigues(rvec)
    point_marker_coords = np.array([0, 0, -0.14])  # 14 cm behind, along the negative z-axis
    point_camera_coords = np.dot(rotation_matrix, point_marker_coords) + tvec
    return point_camera_coords

centers = [getCenter(r,t)[0][[0,2]] for r,t in zip(rvecs, tvecs)]

# [array([0.24546187, 1.6224191 ]), array([-0.16363691,  1.42022181])]
# [ (x,z,r) ,...]
rad = 0.14
obstacles = []
for centre in centers:
    tuple = (centre[0],centre[1],rad)
    obstacles.append(tuple)


start = (0, 0)
goal = (1, 4)
map_size = (10, 10)
rrt = RRT(start, goal, map_size, obstacles, step_size=1, max_iter=1000)


path = rrt.find_path()

def goLine(dist):
    arlo.go_diff(speed * (1+bias),speed * (1-bias), 1, 1)
    time.sleep(calibration["speed"]*dist)
    arlo.stop()

def rotateDeg(deg, speed=60, clockwise=False):
    if deg < 5:
        return
    
    arlo.go_diff(speed * (1+bias),speed * (1-bias), 
                0 if clockwise else 1,
                1 if clockwise else 0)
    time.sleep(calibration["rotation_speed"]*deg)
    arlo.stop()

for _, turn, dist in accumulate(path, movement, initial=((0,0),0,0)):
    rotateDeg(turn)
    goLine(dist)




