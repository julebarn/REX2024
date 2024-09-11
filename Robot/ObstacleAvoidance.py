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

def tr(arlo):
    arlo.stop()
    arlo.go_diff(lturn,rturn,1,0)
    sleep(0.3)


def tl(arlo):
    arlo.stop()
    arlo.go_diff(lturn,rturn,0,1)
    sleep(0.3)

def t90(arlo):
    arlo.go_diff(lturn,rturn,1,0)
    sleep(0.79)
    arlo.stop()
    sleep(2)


arlo.go_diff(lspeed,rspeed,1,1)

i=0
state = 0
while i<1:
    # if(state == 0):
    #     if(arlo.read_sensor(0)<200):
    #         if(arlo.read_sensor(3) > 1000):
    #             t90r(arlo)
    #             state = 1
    #         elif (arlo.read_sensor(2) > 1000):
    #             t90l(arlo)
    #             state = 3
    #         elif (arlo.read_sensor(1) >1000):
    #             t90r(arlo)
    #             t90r(arlo)

    if(arlo.read_sensor(0)<300):
        tr(arlo)
        arlo.go_diff(lspeed,rspeed,1,1)
    
    if(arlo.read_sensor(2)<300):
        tr(arlo)
        arlo.go_diff(lspeed,rspeed,1,1)
    
    if(arlo.read_sensor(3)<300):
        tl(arlo)
        arlo.go_diff(lspeed,rspeed,1,1)

    if arlo.read_sensor(0) < 300 and arlo.read_sensor(2)<300 and arlo.read_sensor(3)<300 :
        t90(arlo)
        t90(arlo)
        arlo.go_diff(lspeed,rspeed,1,1) 


    i+1
print(arlo.read_sensor(0))

arlo.stop()