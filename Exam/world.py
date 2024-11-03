
import math
from self_local import EstimatePosition
from RRT import RRT



landmarks = {
    1: (1, 1),
    2: (1, 4),
    3: (5, 1),
    4: (5, 4)
}

def isLandmark(id):
    return id in landmarks

def getLandmark(id):
    return landmarks[id]


# visit_dist is in cm 
# (TODO we should probably standardize the units in the codebase)
def AtTarget(local, target, visit_dist= 0.40):
    lx, ly, _ = local
    tx, ty = getLandmark(target)

    dist = math.dist((lx, ly), (tx, ty))
    print(f"Distance to target({target}): {dist}")
    return dist < visit_dist


landmarkRadius =0.40
TargetRadius = 0.20
landmarksObstacles = [
    # (id , x, y)
    (1, 1, 1),
    (2, 1, 4),
    (3, 5, 1),
    (4, 5, 4)
]

obstacles = {}
obstacleRadius = 0.20
def addObstacle(id, rx, ry):
    pos = EstimatePosition()
    
    x, y, t = pos

    x = x + rx * math.cos(t) - ry * math.sin(t)
    y = y + rx * math.sin(t) + ry * math.cos(t)

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
    
    print("RRT")
    rrt = RRT((lx, ly), (tx+0.2, ty), 
               obstacles= O, 
               map_size=(6, 5),
               step_size=0.5,
               max_iter=500)  
    path = rrt.find_path()
    rrt.plot_initial()
    rrt.plot_final(path)

    return path
    

    


