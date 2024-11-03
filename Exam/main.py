from movepath import MovePath, goDist
from robot import Robot
from spotting import Spot360
from world import AtTarget, MakePath
from self_local import EstimatePosition
from self_local import move


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
    print("Current target is: ", target.current())
    if AtTarget(EstimatePosition(), target.current()):
        target.nextTarget()
    
    
    Spot360(arlo)
    path = MakePath(EstimatePosition(), target.current())
    print(f"{path=}")
    finished = MovePath(arlo, path)
    if not finished:
        print("Kidnapped by the anti-collision code 😅")
        if not AtTarget(EstimatePosition(), target.current()):
            goDist(arlo, 0.2, back=True)
           
                            
        

