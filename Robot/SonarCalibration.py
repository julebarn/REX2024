from robot import Robot
from time import sleep
import numpy as np

arlo = Robot()

# 10-300
distances = [100,500,1000,1500,2000,2500,3000]

measurments = [0,0,0,0,0,0,0]
normalized = np.array()

i = 0
while i < len(distances):
    print("Place Arlo " + str(distances[i]) + "mm away from object")
    if input("Done? [y/n ]") == 'y':
        measurments[i] = arlo.read_front_ping_sensor()
    i+=1


print(measurments)

for i in range (len(distances)):
    normalized[i] = distances[i]-measurments[i]

print(np.std(normalized))