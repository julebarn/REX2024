from robot import Robot 
from time import sleep


lspeed = 100
rspeed = 107

lturn = 60
rturn = 60

arlo = Robot()
arlo.reset_encoder_counts()
def t90(arlo):
    arlo.go_diff(lturn,rturn,1,0)
    sleep(0.783)
    arlo.stop()
    sleep(2)

def line(arlo):
    arlo.go_diff(lspeed,rspeed,1,1)
    sleep(3)
    arlo.stop()

def sq(arlo):
    line(arlo)
    t90(arlo)
    line(arlo)
    t90(arlo)
    line(arlo)
    t90(arlo)
    line(arlo)
    t90(arlo)

for i in range(4*5):
    t90(arlo)

