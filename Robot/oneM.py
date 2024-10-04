
def goLine(dist):
    print("Going", dist, "meters")
    arlo.go_diff(speed * (1+bias),speed * (1-bias), 1, 1)
    time.sleep(calibration["speed"]*dist)
    arlo.stop()


goLine(1)
