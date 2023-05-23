#!/usr/bin/env python3

import rospy
import math
from blob_segmentation.msg import Centroid
from geometry_msgs.msg import Twist

class ColorFollow:
    def __init__(self):
        # ROS pub/sub

        vel_topic = rospy.get_param("~vel_topic", "/cmd_vel")
        centroid_topic = rospy.get_param("centroid_topic", "centroid")
        self.image_width = rospy.get_param("~image_width", 0)
        self.image_height = rospy.get_param("~image_height", 0)
        self._laser_sub = rospy.Subscriber(centroid_topic, Centroid, self.centroidCallback, queue_size = 1)
        self.cmd_vel_pub = rospy.Publisher(vel_topic, Twist, queue_size = 1)
        
        self.prev_lineal = 0.0
        self.prev_angular = 0.0

        self.alpha_lineal=0.8
        self.alpha_w=0.8
        
    
    def centroidCallback(self, msg):
        #Cogemos la información del centroide del mayor área segmentada.
        x = msg.x
        y = msg.y
        area = msg.area 

        vel_angular = 0.0
        vel_lineal = 0.0

        if area<80:
            #Si el área máxima detectada es excesivamente pequeña, consideraremos que
            #no existe objeto al que seguir, por lo que giraremos el robot en busca de objetos
            vel_lineal = 0.0
            if self.prev_angular<0: 
                vel_angular = -0.5
            else:
                vel_angular=0.5
        elif area>300:
            #Si el área es excesivamente grande, asumiremos que estamos demasiado cerca del objeto,
            #por lo que detendremos el robot
            vel_lineal = 0.0
            vel_angular = 0.0
        else:
            #En el caso general, seguimos la estrategia definida en la documentación: 
            #utilizar un control proporcional para que la orientación del robot esté centrada con el
            #centro del objeto (segmentación), y para que la velocidad lineal sea proporcional
            #a la distancia con el objeto (área de la segmentación).
            #Se utilizará un filtrado paso bajo para suavizar las velocidades del robot
            vel_angular = float(((self.image_width/2.0) - x)/self.image_width*2*2)
            vel_angular = math.tanh(vel_angular)*0.5
            vel_angular = vel_angular*self.alpha_w + self.prev_angular*(1-self.alpha_w)

            vel_lineal = min(max(1.0/math.sqrt(area)*15.0 , 0.05),0.3) 
            vel_lineal = vel_lineal*self.alpha_lineal + self.prev_lineal*(1-self.alpha_lineal)

        #Establecemoos la velocidad
        cmd_vel_msg = Twist()
        cmd_vel_msg.linear.x  = vel_lineal
        cmd_vel_msg.angular.z = vel_angular
        self.cmd_vel_pub.publish(cmd_vel_msg)

        #actualizamos las velocidades de la iteración anterior, para realizar el filtrado paso bajo
        self.prev_lineal = vel_lineal
        self.prev_angular = vel_angular
        rospy.loginfo("Velocidad:%f\n", vel_lineal)

def main():
    rospy.init_node("color_follow")
    robot = ColorFollow()
    rospy.spin()
    
if __name__=="__main__":
    try:
        main()
    except rospy.ROSInterruptException: pass