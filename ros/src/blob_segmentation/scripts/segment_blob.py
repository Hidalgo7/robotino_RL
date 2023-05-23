#!/usr/bin/env python3
import rospy
import numpy as np
import traceback
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


class blobDetection:
    def __init__(self):
        image_topic = rospy.get_param("~image_topic", "/camera/image_raw")
        filtered_image_topic = rospy.get_param("~filtered_image_topic", "/filtered_image")
        
        self.bridge = CvBridge()
        self.pub = rospy.Publisher(filtered_image_topic, Image, queue_size=1)
        self.sub = rospy.Subscriber(image_topic, Image, self.callback, queue_size=1)
        self.lineUpper = np.array([70,255,255])
        self.lineLower = np.array([0,50,50])
        
    def callback(self, msg):
        try:
            cv_img = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            resized = cv2.resize(cv_img.copy(),(64,48),interpolation=cv2.INTER_AREA)
            img_filtered = self.colorFilter(resized)
            cv2.imshow("Resized filtered",img_filtered)
            msg = self.bridge.cv2_to_imgmsg(img_filtered,)
            self.pub.publish(msg)
            cv2.waitKey(10)

        except CvBridgeError as exc:
            print(traceback.format.exc())

    def colorFilter(self,src):
        src_copy = src.copy()
        hsv = cv2.cvtColor(src_copy,cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv,self.lineLower,self.lineUpper)

        filtered_img = cv2.bitwise_and(src_copy,src_copy,mask=mask)

        return filtered_img

def detectLine(image):
    cv_img = CvBridge().imgmsg_to_cv2(image)
    cv_copy = cv_img.copy()
    hsv = cv2.cvtColor(cv_copy,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv,np.array([0,50,50]),np.array([70,255,255]))

    return np.sum(mask) > 0


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

