#!/usr/bin/env python3
import rospy
import numpy as np
import traceback
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from geometry_msgs.msg import Point
from cv_bridge import CvBridge, CvBridgeError

from blob_segmentation.msg import Centroid


class blobDetection:
    def __init__(self):

        image_topic = rospy.get_param("~image_topic", "/usb_cam/image_raw")
        centroid_topic = rospy.get_param("centroid_topic", "/usb_cam/image_raw")
        self.bridge = CvBridge()
        self.pub = rospy.Publisher(centroid_topic, Centroid, queue_size=1)
        self.sub = rospy.Subscriber(image_topic, Image, self.callback, queue_size=1)
        self.orig_img = None
        self.params = None
        print("Done control window")
        self.window_initialized = False
        
    def callback(self, msg):
        if not self.window_initialized:
            createControlWindow()
            self.window_initialized = True
        try:
            cv_img = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            self.handleTrackbarChanges()
            
            cresx, cresy, area, img = findCentroid(cv_img.copy(), self.params)
            msg = Centroid(cresx, cresy, area)
            self.pub.publish(msg)
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
            drawCross( img, cresx, cresy, (0,0,255), 5)
            cv2.imshow("Blob segmentation", img)
            cv2.waitKey(1)

        except CvBridgeError as exc:
            print(traceback.format.exc())
            
    def getTrackbarParams(self):
        return [cv2.getTrackbarPos('LowB', 'Blob segmentation'),
                cv2.getTrackbarPos('LowG', 'Blob segmentation'),
                cv2.getTrackbarPos('LowR', 'Blob segmentation'),
                cv2.getTrackbarPos('HighB', 'Blob segmentation'),
                cv2.getTrackbarPos('HighG', 'Blob segmentation'),
                cv2.getTrackbarPos('HighR', 'Blob segmentation')]
            
    def handleTrackbarChanges(self):
        self.params = self.getTrackbarParams()
        

def applyErodeAndDilate(im):
    kernel = np.ones((2,2), np.uint8)
    
    eroded = cv2.erode(im,  kernel, iterations = 1)
    dilated = cv2.dilate(eroded, kernel, iterations = 1)
    return dilated


def drawCross(img, x, y, color, d):
    cv2.line(img, (x+d, y-d), (x-d, y+d), color, 2)
    cv2.line(img, (x-d, y-d), (x+d, y+d), color, 2)


def nothing(x):
    pass


def findCentroid(src, params):
    lowRGB = np.array(params[0:3])
    highRGB = np.array(params[3:])

    img_segmented = cv2.inRange(src, lowRGB, highRGB)
    # # Apply erode and dilate
    img_segmented = applyErodeAndDilate(img_segmented)

    # Find contours
    # Depending upon cv2 version!!
    contours, hierarchy = cv2.findContours(img_segmented, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # im, contours, _ = cv2.findContours(img_segmented, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    resx = -1
    resy = -1
    numcontours = len(contours)
    if numcontours < 1:
      return resx, resy, src    
  
    color = (255,255,255)
    cv2.drawContours(src, contours, -1, color, 3)
    #Approximate contours to polygons + get bounding rects and circles
    contours_poly = []
    center = []
    radius = []
    biggestContour = -1
    maxsize = 0
    boundRect = []
    x = [-1 for i in range(numcontours)]
    y = [-1 for i in range(numcontours)]
    w = [-1 for i in range(numcontours)]
    h = [-1 for i in range(numcontours)]
    for i in range(0, numcontours):
        contours_poly.append(cv2.approxPolyDP(contours[i], 3, True ))
        x[i], y[i], w[i], h[i] = cv2.boundingRect(contours_poly[i])
        c, r = cv2.minEnclosingCircle(contours_poly[i])
        center.append(c)
        radius.append(r)
    i = 0
    maxindex = -1
    maxsize = 0
    color2 = (255, 0, 0)
    for contour in contours:
        if contour.size > 10:
            if contour.size > maxsize:
                maxsize = contour.size
                maxindex = i
                biggestContour = contour
            cv2.rectangle(img_segmented, (x[i], y[i]), (x[i]+w[i], y[i]+h[i]),  color2, 2, 8, 0 )
        i = i+1
  
    #Centroid estimate
    if maxsize >= 10:
        M = cv2.moments( biggestContour, False )
        resx = int(M['m10']/M['m00'])
        resy = int(M['m01']/M['m00'])
    
    # print("%d contours found. Biggest size: %d centroid(%d,%d)"%(len(contours), maxsize, resx, resy))
    return resx,resy, maxsize, img_segmented #src


def createControlWindow():
    print("creating control window")
    cv2.namedWindow('Blob segmentation')
    
    cv2.createTrackbar("LowR", 'Blob segmentation', 0, 255, nothing)
    cv2.createTrackbar("HighR", 'Blob segmentation', 255, 255, nothing)
    
    cv2.createTrackbar("LowG", 'Blob segmentation', 0, 255, nothing)
    cv2.createTrackbar("HighG", 'Blob segmentation', 255, 255, nothing)
    
    cv2.createTrackbar("LowB", 'Blob segmentation', 0, 255, nothing)
    cv2.createTrackbar("HighB", 'Blob segmentation', 255, 255, nothing)

def main():

    rospy.init_node("segment_blob")

    blobd = blobDetection()
    

    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()

        
if __name__ == "__main__":
    main()

