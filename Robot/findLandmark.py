import cv2
import numpy
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

def rotateUntil(pred, max_i=1000, agent=None, clockwise=False):
    v = .34

    go = False
    while not go:
        agent.go_diff(v*speed * (1+bias), v*speed * (1-bias), 
                0 if clockwise else 1,
                1 if clockwise else 0)
        time.sleep(0.2)
        agent.stop()
        time.sleep(0.15)
        go = pred()

    agent.stop()

def foundLandmark(cam=None):
    img = cam.capture_array()
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    _, ids, _ = cv2.aruco.detectMarkers(img, aruco_dict, parameters=parameters)
    print(ids)
    return ids != None

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

#while partial(foundLandmark, cam):
#    arlo.go_diff(speed * (1+bias),speed * (1-bias), 1, 1)
#    time.sleep(0.2)
#    arlo.stop()
