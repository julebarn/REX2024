
import math
from self_local import EstimatePosition
from RRT import RRT



landmarks = {
    1: (100, 100),
    2: (100, 400),
    3: (500, 100),
    4: (500, 400)
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
    (1, 100, 100),
    (2, 100, 400),
    (3, 500, 100),
    (4, 500, 400)
]

obstacles = {}
obstacleRadius = 20
def addObstacle(id, rx, ry):
    pos = EstimatePosition()

    # TODO
    x = pos[0] + rx
    y = pos[1] + ry
    
    obstacles[id] = (x, y)

def MakePath(local, target):
    lx, ly, lt = local
    tx, ty = getLandmark(target)
    # a path is a list of points to visit 

    O = []

    for (i , ox, oy) in landmarksObstacles:
        radius = landmarkRadius
        if i == target:
            radius = TargetRadius 
        O.append((ox, oy, radius))

    for (i, ox, oy) in obstacles.items():
        O.append((ox, oy, obstacleRadius))

    rrt = RRT((lx, ly), (tx, ty), 
               obstacles= O, 
               map_size=(600, 500))  
    path = rrt.find_path()

    return path
    

    


