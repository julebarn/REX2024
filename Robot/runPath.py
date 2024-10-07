# import cv2
# import math
# import numpy as np
# from robot import Robot 
# from functools import partial
# import time
# from calibration import calibration
# from picamera2 import Picamera2, Preview
# from itertools import accumulate
# from RRT import *
# from calibration import calibration

with open("Robot/path.csv", 'r') as f:
    path = [line.rstrip('\n') for line in f]

print(path)