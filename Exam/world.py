from self_local import EstimatePosition
import math
from RRT import RRT



landmarks = {
    1: (0, 0),
    2: (0, 300),
    3: (400, 0),
    4: (400, 300)
}

def isLandmark(id):
    return id in landmarks

def getLandmark(id):
    return landmarks[id]


# visit_dist is in cm 
# (TODO we should probably standardize the units in the codebase)
def AtTarget(local, target, visit_dist= 40):
    lx, ly, _ = local
    tx, ty = getLandmark(target)

    dist = math.dist((lx, ly), (tx, ty))
    print(f"Distance to target({target}): {dist}")
    return dist < visit_dist


landmarkRadius = 50
TargetRadius = 20
landmarksObstacles = [
    # (id , x, y)
    (1, 0, 0),
    (2, 0, 300),
    (3, 400, 0),
    (4, 400, 300)
]

def MakePath(local, target):
    lx, ly, _ = local
    tx, ty = getLandmark(target)
    # a path is a list of points to visit 

    Obstacles = []

    for (i , ox, oy) in landmarksObstacles:
        radius = landmarkRadius
        if i == target:
            radius = TargetRadius 
        Obstacles.append((ox, oy, radius))

    # TODO add obstacle to the Obstacles list
    
    # TODO i am unsure if RRT implementation allows for the robot to be outside the map 
    # whcih is needed for the the coordinates of the landmarks to work
    rrt = RRT((lx, ly), (tx, ty), 
               obstacles= Obstacles, 
               map_size=(400, 400))  
    path = rrt.find_path()

    return path
    

    


