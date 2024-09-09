from robot import Robot
from time import sleep

bias = -0.043750000000000004

speed = 100
rturn_speed = speed * 0.45
lturn_speed = speed * 0.42

rturn_time = 4.65
lturn_time = 4
line_time = 2.5

def _8(arlo):
    arlo.go_diff(speed * (1+bias),rturn_speed * (1-bias), 1, 1)
    sleep(rturn_time)
    arlo.go_diff(speed * (1+bias),speed * (1-bias), 1, 1)
    sleep(line_time)
    arlo.go_diff(lturn_speed * (1+bias),speed * (1-bias), 1, 1)
    sleep(lturn_time)
    arlo.go_diff(speed * (1+bias),speed * (1-bias), 1, 1)
    sleep(line_time)
    arlo.stop()


if __name__ == "__main__":
    arlo = Robot()
    for i in range(8):
        _8(arlo)


