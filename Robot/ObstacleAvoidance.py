from robot import Robot 
from time import sleep

arlo = Robot()
lspeed = 100 * 0.6
rspeed = 107 * 0.6

lturn = 60
rturn = 60

meter = 1.42*2

print(arlo.read_sensor(0))

def line(arlo,dist):
    arlo.go_diff(lspeed,rspeed,1,1)
    sleep(dist*0.8)
    arlo.go_diff(lspeed/2,rspeed/2,1,1)
    sleep(dist*0.2)
    arlo.stop()
    sleep(1)

arlo.go_diff(lspeed,rspeed,1,1)

i=0
while i<1:
    if(arlo.read_sensor(0) <200):
        arlo.stop()
        i+1

print(arlo.read_sensor(0))
