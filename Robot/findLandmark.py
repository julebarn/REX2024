import cv2
import numpy as np
from robot import Robot 
from functools import partial
import time
from calibration import calibration
try:
    from picamera2 import Picamera2, Preview
    print("Camera.py: Using picamera2 module")
except ImportError:
    print("Camera.py: picamera2 module not available")
    exit(-1)


aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
parameters = cv2.aruco.DetectorParameters_create()

bias  = calibration["bias"]
speed = 100

def goLine():
    arlo.go_diff(speed * (1+bias),speed * (1-bias), 1, 1)

def rotateUntil(pred, agent=None, clockwise=False):
    v = .34

    go = False
    while not go:
        agent.go_diff(v*speed * (1+bias), v*speed * (1-bias), 
                0 if clockwise else 1,
                1 if clockwise else 0)
        time.sleep(0.1)
        agent.stop()
        time.sleep(0.2)
        go = pred()

    agent.stop()

def foundLandmark(cam=None):
    img = cam.capture_array()
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    _, ids, _ = cv2.aruco.detectMarkers(img, aruco_dict, parameters=parameters)

    return ids != None

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

rotateUntil(partial(foundLandmark, cam), agent=arlo, clockwise=False)

img = cam.capture_array()
img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
corners, ids, _ = cv2.aruco.detectMarkers(img, aruco_dict, parameters=parameters)

cmat = cameraMatrix(1273) # TODO calibrate
dcof = np.array([0,0,0,0])

rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners, .145, cmat, dcof)
print(rvecs, tvecs)

goLine()
time.sleep(tvecs[0][0][2]*0.5625-0.113) # go to target -20 cm
arlo.stop()
