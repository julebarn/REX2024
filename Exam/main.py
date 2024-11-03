from movepath import * 
from robot import Robot
from spotting import Spot360
from world import AtTarget, MakePath
from self_local import EstimatePosition



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


#Spot360(arlo) 


while not target.isDone():
    if AtTarget(EstimatePosition(), target.current()):
        target.nextTarget()
    
    
    Spot360()
    path = MakePath(EstimatePosition(), target.current())
    print(f"{path=}")
    finished = MovePath(arlo, path)
    if not finished:
        #TODO if this code is reached 
        # the code just Kidnapped the robot
        print("Kidnapped by the anti-collision code 😅")
        break
        

