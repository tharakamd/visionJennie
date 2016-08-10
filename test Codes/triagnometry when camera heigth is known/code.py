import numpy as np
import cv2
import math

#initializing the camera heigth
CAMERA_HEIGTH = 48.0

#initializing pitch angle
PITCH_ANGLE = math.radians(90)

#initializing field of view in verticle direction
FOVV = math.radians(90)

#initializing field of view in horizontal direction
FOVH = math.radians(90)

#focalLength of the camera
FOCAL_LENGTH = 543;

#main function with the logic implemented
def distance_to_camera(imageHeigth,imageWidth,cameraHeigth, pitchAngle, fovv, fovh, focalLength, perWidth):
    verticalAngle = pitchAngle + (imageHeigth/2 - perWidth[1])*(fovv/imageHeigth)
    rotationAngle = (perWidth[0]- imageWidth/2)*(fovh/imageWidth)
    y = cameraHeigth*math.tan(verticalAngle)
    x = y*math.tan(rotationAngle)
    z = math.sqrt(cameraHeigth**2 + y**2 + x**2)
    return z

#we are calculating distance to this point from the camera
def getPoints():
    return [300,300]

# initialize the list of images that we'll be using
IMAGE_PATHS = ["images/2ft.png", "images/3ft.png", "images/4ft.png"]

# loop over the images
for imagePath in IMAGE_PATHS:
    image = cv2.imread(imagePath)
    height, width,_ = image.shape
    inches = distance_to_camera(height,width,CAMERA_HEIGTH,PITCH_ANGLE,FOVV,FOVH, FOCAL_LENGTH, getPoints())
 
	#displaying results
    cv2.circle(image,(300,300), 63, (0,0,255), -1)
    cv2.putText(image, "%.2fft" % (inches / 12),
        (image.shape[1] - 200, image.shape[0] - 300), cv2.FONT_HERSHEY_SIMPLEX,
        2.0, (0, 255, 0), 3)
    cv2.imshow("image", image)
    if cv2.waitKey(0) & 0xFF == ord('q'):
            break
