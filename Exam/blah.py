import math

def angleBetweenPoints(a,b):
    return(math.degrees(math.atan((a[0]-b[0])/(a[1]-b[1]))))

a = (0,0)
b = (0.27558484319520465, 0.41719658939290777)
print(angleBetweenPoints(a,b))