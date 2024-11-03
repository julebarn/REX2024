
import cv2
import numpy as np
from picamera2 import Picamera2, Preview
import movepath
from world import isLandmark, getLandmark, addObstacle
from self_local import sense_landmark


def getCenter(rvec, tvec):
    rotation_matrix, _ = cv2.Rodrigues(rvec)
    point_marker_coords = np.array([0, 0, -0.14])  # 14 cm behind, along the negative z-axis
    point_camera_coords = np.dot(rotation_matrix, point_marker_coords) + tvec
    return point_camera_coords

def cameraMatrix(focal_length, center=(320,240)):
    f = focal_length
    cx, cy = center
    return np.array([
        [f, 0, cx],
        [0, f, cy],
        [0, 0, 1 ]
    ])

cam = Picamera2()
cam.start()
cmat = cameraMatrix(1273) # TODO calibrate
dcof = np.array([0,0,0,0])
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
parameters = cv2.aruco.DetectorParameters_create()


def Spot360(arlo):
    markers = []

    for i in range(8):
        m = spotMarkers()
        markers = markers + m
        movepath.rotateDeg(arlo, 45)
	
    for i in markers:
        print(i)
    print(markers)
    return markers


def spotMarkers():
    img = cam.capture_array()
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    corners, ids, _ = cv2.aruco.detectMarkers(img, aruco_dict, parameters=parameters)
    
    print(ids)
    print(corners)
    
    rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners, .145, cmat, dcof)
    
    ids   = ids   if ids   is not None else []
    rvecs = rvecs if rvecs is not None else []
    tvecs = tvecs if tvecs is not None else []

    for i in range(len(ids)):
        if isLandmark(ids[i][0]):
            print("Landmark", ids[i][0])

            center = getCenter(rvecs[i], tvecs[i])
            print("Center", center)

            # this is relative to the camera not the robot
            rx, rz = center[0][0], center[0][2]
            lx, ly = getLandmark(ids[i][0])
            lm = (lx, ly, rx, rz)

    
            sense_landmark(lm)
            continue
        print("obstacle", ids[i][0])
    
        
        center = getCenter(rvecs[i], tvecs[i])
        print("Center", center)

        addObstacle(ids[i][0], center[0][0], center[0][1])




    return ids

