from movepath import * 
from robot import Robot
from spotting import Spot



class TargetLandmark:
    def __init__(self):
        self.targetOrder = [1,2,3,4,1]
        self.currentTargetIndex = 0
    
    def isDone(self):
        return self.currentTargetIndex == len(self.targetOrder)

    def current(self):
        return self.targetOrder[self.currentTargetIndex]
    
    def nextTarget(self):
        self.currentTargetIndex += 1
        print("Next target is: ", self.targetOrder[self.currentTargetIndex])
        return self.targetOrder[self.currentTargetIndex]
        


target = TargetLandmark()
arlo = Robot()

#TODO use locilization here 
Spot(arlo)


while not target.isDone():
    if atTarget(local, target.current()):
        target.nextTarget()
    
    #TODO use locilization here 
    Spot(arlo)

    path = makePath(arlo, target.current())

    finished = MovePath(arlo, path)
    if not finished:
        #TODO use locilization here 
        Spot(arlo)
        break
        


