import time
try:
    from picamera2 import Picamera2, Preview
    print("Camera.py: Using picamera2 module")
except ImportError:
    print("Camera.py: picamera2 module not available")
    exit(-1)

cam = Picamera2()
camera_config = cam.create_preview_configuration()
cam.configure(camera_config)
cam.start_preview(Preview.QTGL)
cam.start()
time.sleep(2)

while True:
    name = input("Enter the image name (q to quit): ")
    if name == "q":
        break

    cam.capture_file("./img/" + name + ".jpg")
    
    
