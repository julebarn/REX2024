import cv2
import numpy
from robot import Robot 
from functools import partial
import time
try:
    from picamera2 import Picamera2, Preview
    print("Camera.py: Using picamera2 module")
except ImportError:
    print("Camera.py: picamera2 module not available")
    exit(-1)


aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
parameters = cv2.aruco.DetectorParameters_create()

bias = -0.043750000000000004
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
        time.sleep(0.05)
        go = pred()

    agent.stop()

def foundLandmark(cam=None):
    img = cam.capture_array()
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    _, ids, _ = cv2.aruco.detectMarkers(img, aruco_dict, parameters=parameters)
    print(ids)
    return ids != None

def main():
    print("main")
    arlo = Robot()
    
    cam = Picamera2()
    cam.video_configuration.controls.FrameRate = 5.0
    # camera_config = cam.create_preview_configuration()
    # cam.configure(camera_config)
    # cam.start_preview(Preview.QTGL)
    cam.start()
    
    print("Out")
    img = cam.capture_array()
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imshow('Detected Markers', img)

    rotateUntil(partial(foundLandmark, cam), agent=arlo, clockwise=False)
    while partial(foundLandmark, cam):
        arlo.go_diff(speed * (1+bias),speed * (1-bias), 1, 1)
        time.sleep(0.2)
        arlo.stop()
    
if __name__ == "__main__":
    main()
