import cv2
import numpy
from robot import Robot 
try:
    from picamera2 import Picamera2, Preview
    print("Camera.py: Using picamera2 module")
except ImportError:
    print("Camera.py: picamera2 module not available")
    exit(-1)

bias = -0.043750000000000004
speed = 100

def make_detector():
        aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
        parameters = cv2.aruco.DetectorParameters()
        return cv2.aruco.ArucoDetector(aruco_dict, parameters)


def goLine():
    arlo.go_diff(speed * (1+bias),speed * (1-bias), 1, 1)



def main():
    arlo = Robot()
    
    cam = Picamera2()
    camera_config = cam.create_preview_configuration()
    cam.configure(camera_config)
    cam.start()
    
    Detector = make_detector()

    while True:
        img = cam.capture_array()
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        
        corners, ids, rejected = Detector.detectMarkers(img)

        if ids is not None:
            cv2.aruco.drawDetectedMarkers(image, corners, ids)
            cv2.imshow('Detected Markers', image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

       
 

        






if __name__ == "__main__":
    main()