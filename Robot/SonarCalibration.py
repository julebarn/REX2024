from robot import Robot
from time import sleep
import numpy as np

arlo = Robot()

distances = [100,500,1000,1500,2000,2500,3000]

measurments = [0,0,0,0,0,0,0]
normalized = [0,0,0,0,0,0,0]

i = 0
while i < len(distances):
    print("Place Arlo " + str(distances[i]) + "mm away from object")
    if input("Done? [y/n ]") == 'y':
        measurments[i] = arlo.read_front_ping_sensor()
    i+=1


print(measurments)

for i in range (len(distances)):
    normalized[i] = distances[i]-measurments[i]

npnorm = np.array(normalized)
print(np.std(npnorm))