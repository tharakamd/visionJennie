# import the necessary packages
import numpy as np
import cv2
import math

def find_marker(image):
    # convert the image to grayscale, blur it, and detect edges
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 35, 125)
 
    # find the contours in the edged image and keep the largest one;
    # we'll assume that this is our piece of paper in the image
    (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    c = max(cnts, key = cv2.contourArea)
    # compute the bounding box of the of the paper region and return it
    return cv2.minAreaRect(c)

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
marker = find_marker(image)
focalLength = (marker[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH
print focalLength


# loop over the images
for imagePath in IMAGE_PATHS:
    # load the image, find the marker in the image, then compute the
    # distance to the marker from the camera
    image = cv2.imread(imagePath)
    marker = find_marker(image)
    height, width,_ = image.shape
    inches = distance_to_camera(height,width,CAMERA_HEIGTH,PITCH_ANGLE,FOVV,FOVH, focalLength, getPoints())
 
    # draw a bounding box around the image and display it
    box = np.int0(cv2.cv.BoxPoints(marker))
    cv2.drawContours(image, [box], -1, (0, 255, 0), 2)
    cv2.circle(image,(300,300), 63, (0,0,255), -1)
    cv2.putText(image, "%.2fft" % (inches / 12),
        (image.shape[1] - 200, image.shape[0] - 300), cv2.FONT_HERSHEY_SIMPLEX,
        2.0, (0, 255, 0), 3)
    cv2.imshow("image", image)
    if cv2.waitKey(0) & 0xFF == ord('q'):
            break
