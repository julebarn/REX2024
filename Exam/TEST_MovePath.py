from movepath import * 
from robot import Robot

# path =[
#     [0, 0],
#     [0.27558484319520465, 0.41719658939290777],
# 	[0.7364580606932789, 0.611093153036962],
# 	[0.7549048590666272, 1.1107527527944099],
#  	[0.957324827579686, 1.567946537033842],
#  	[0.668544966572807, 1.9761207545891006],
# 	[0.17724971919484672, 2.0690130573048195],
# 	[0, 1.8]
#     ]


path = [
     [0,0],
     [1,1],
     [1,2],
     [0,3]
 ]

arlo = Robot()

#MovePath(arlo,path)

#goDist(arlo,0.5)

#rotateDeg(arlo,45,60)
rotateDeg(arlo,-45,60)
