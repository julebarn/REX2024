from robot import Robot
from time import sleep

arlo = Robot()

# 10-300
distances = [10,50,100,150,200,250,300]

measurments = [0,0,0,0,0,0,0]

print("Place Arlo 10cm away from object")

i = 0
while i < len(distances):
    print("Place Arlo " + distances[i] + "cm away from object")
    if input("Done? [y/n ]") == 'y':
        measurments[i] = arlo.read_front_ping_sensor()


print(measurments)