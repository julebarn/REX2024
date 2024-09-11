
try:
    import picamera2
    print("Camera.py: Using picamera2 module")
except ImportError:
    print("Camera.py: picamera2 module not available")
    exit(-1)

while True:
    name = input("Enter the image name (q to quit): ")
    if name == "q":
        break

    picamera2.capture("./img/" + name + ".jpg")
    
    