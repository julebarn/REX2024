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

def goLine():
    arlo.go_diff(speed * (1+bias),speed * (1-bias), 1, 1)



def main():
    arlo = Robot()
    
    cam = Picamera2()
    camera_config = cam.create_preview_configuration()
    cam.configure(camera_config)
    cam.start_preview(Preview.QTGL)
    cam.start()


    img = cam.capture_array()
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        
    cv2.imshow("Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

        #cv2.aruco.detectMarkers(image, aruco_dict, parameters=parameters)






if __name__ == "__main__":
    main()