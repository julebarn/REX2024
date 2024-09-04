from robot import Robot 
from time import sleep


lspeed = 100
rspeed = 107

lturn = 60
rturn = 60

meter = 1.42
arlo = Robot()
arlo.reset_encoder_counts()
def t90(arlo):
    arlo.go_diff(lturn,rturn,1,0)
    sleep(0.7808)
    arlo.stop()
    sleep(2)

def line(arlo,dist):
    arlo.go_diff(lspeed,rspeed,1,1)
    sleep(dist)
    arlo.stop()
    sleep(1)

def sq(arlo,dist):
    line(arlo,dist)
    t90(arlo)
    line(arlo,dist)
    t90(arlo)
    line(arlo,dist)
    t90(arlo)
    line(arlo,dist)
    t90(arlo)
for i in range(5):
    sq(arlo,meter)
#sq(arlo,meter)
#line(arlo,meter*4)
