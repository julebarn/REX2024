
from robot import Robot
from time import sleep


arlo = Robot()

while True:
    print(arlo.read_front_ping_sensor())
    sleep(0.5)