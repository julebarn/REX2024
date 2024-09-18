

import os
import cv2


# Specify the folder path
folder_path = './'

# List all files ending with .jpg
jpg_files = [f for f in os.listdir(folder_path) if f.endswith('.jpg')]

# Print the list of jpg files
print(jpg_files)

for jpg_file in jpg_files:
    print(f"Processing file: {jpg_file}")
    # Load your image (replace 'your_image.jpg' with your image file)
    image = cv2.imread(jpg_file)


    # Convert to grayscale if needed
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
    ret,thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # sort contours by area
    contours = sorted(contours, key=cv2.contourArea)
    if len(contours) == 3:
        contours = [contours[1]]

    # Iterate through contours
    for contour in contours:
        # Get bounding box
        x, y, w, h = cv2.boundingRect(contour)
    
        # Calculate size of the bounding box
        size = (w, h)
    
        # Print or use size as needed
        print(f"Bounding box size: {size}")

        # Draw the bounding box on the image (optional)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the image with bounding boxes (optional)
    cv2.imshow('Image with Bounding Boxes', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()