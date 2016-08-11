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

focalLength = 543;

def distance_to_camera(imageHeigth,imageWidth,cameraHeigth, pitchAngle, fovv, fovh, focalLength, perWidth):
    print perWidth
    verticalAngle = pitchAngle + (imageHeigth/2 - perWidth[1])*(fovv/imageHeigth)
    rotationAngle = (perWidth[0]- imageWidth/2)*(fovh/imageWidth)
    y = cameraHeigth*math.tan(verticalAngle)
    x = y*math.tan(rotationAngle)
    z = math.sqrt(cameraHeigth**2 + y**2 + x**2)
    return x,y,z

def getPoints():
    return [100,300]

cap = cv2.VideoCapture(0)
cv2.namedWindow('image')
while(True):
    ret, image = cap.read()
    height, width,_ = image.shape
    x,y,z = distance_to_camera(height,width,CAMERA_HEIGTH,PITCH_ANGLE,FOVV,FOVH, focalLength, getPoints())
    point = getPoints()
    cv2.circle(image,(point[0],point[1]), 20, (0,0,255), -1)
    cv2.imshow("image", image)
    print "x= %.2f y= %.2ft z= %.2ft" %(x/12,y/12,z/12)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

