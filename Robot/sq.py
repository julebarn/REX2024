from robot import Robot 
from time import sleep


lspeed = 100 * 0.6
rspeed = 107 * 0.6

lturn = 60
rturn = 60

meter = 1.42*2
arlo = Robot()
arlo.reset_encoder_counts()
def t90(arlo):
    arlo.go_diff(lturn,rturn,1,0)
    sleep(0.79)
    arlo.stop()
    sleep(2)

def line(arlo,dist):
    arlo.go_diff(lspeed,rspeed,1,1)
    sleep(dist*0.8)
    arlo.go_diff(lspeed/2,rspeed/2,1,1)
    sleep(dist*0.2)
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
#t90(arlo)
