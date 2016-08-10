import numpy as np
import cv2
import math

def distance_to_camera(imageHeigth,imageWidth,cameraHeigth, pitchAngle, fovv, fovh, focalLength, perWidth):
    # compute and return the distance from the maker to the camera
    verticalAngle = pitchAngle + (imageHeigth/2 - perWidth[1])*(fovv/imageHeigth)
    rotationAngle = (perWidth[0]- imageWidth/2)*(fovh/imageWidth)
    y = cameraHeigth*math.tan(verticalAngle)
    x = y*math.tan(rotationAngle)
    z = math.sqrt(cameraHeigth**2 + y**2 + x**2)
    return z

def getPoints():
    return [300,300]

# initialize the known distance from the camera to the object, which
# in this case is 24 inches
KNOWN_DISTANCE = 24.0
 
# initialize the known object width, which in this case, the piece of
# paper is 11 inches wide
KNOWN_WIDTH = 11.0

#initializing the camera heigth
CAMERA_HEIGTH = 48.0

#initializing pitch angle
PITCH_ANGLE = math.radians(90)

#initializing field of view in verticle direction
FOVV = math.radians(90)

#initializing field of view in horizontal direction
FOVH = math.radians(90)


# initialize the list of images that we'll be using
IMAGE_PATHS = ["images/2ft.png", "images/3ft.png", "images/4ft.png"]

# load the furst image that contains an object that is KNOWN TO BE 2 feet
# from our camera, then find the paper marker in the image, and initialize
# the focal length
image = cv2.imread(IMAGE_PATHS[0])
focalLength = 543;
print focalLength


# loop over the images
for imagePath in IMAGE_PATHS:
    # load the image, find the marker in the image, then compute the
    # distance to the marker from the camera
    image = cv2.imread(imagePath)
    height, width,_ = image.shape
    inches = distance_to_camera(height,width,CAMERA_HEIGTH,PITCH_ANGLE,FOVV,FOVH, focalLength, getPoints())
 
    cv2.circle(image,(300,300), 63, (0,0,255), -1)
    cv2.putText(image, "%.2fft" % (inches / 12),
        (image.shape[1] - 200, image.shape[0] - 300), cv2.FONT_HERSHEY_SIMPLEX,
        2.0, (0, 255, 0), 3)
    cv2.imshow("image", image)
    if cv2.waitKey(0) & 0xFF == ord('q'):
            break
