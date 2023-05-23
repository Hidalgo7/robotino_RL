#!/usr/bin/env python3

import gym
import rospy
from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import DDPG
from stable_baselines3.common.callbacks import StopTrainingOnRewardThreshold, EvalCallback
from stable_baselines3.ddpg.policies import MlpPolicy

# class LineFollow:
#     def __init__(self):
#         # ROS pub/sub

#         vel_topic = rospy.get_param("~vel_topic", "/cmd_vel")
#         image_topic = rospy.get_param("centroid_topic", "centroid")
#         self.image_width = rospy.get_param("~image_width", 0)
#         self.image_height = rospy.get_param("~image_height", 0)
#         self._image_sub = rospy.Subscriber(image_topic, Image, self.centroidCallback, queue_size = 1)
#         self.cmd_vel_pub = rospy.Publisher(vel_topic, Twist, queue_size = 1)
#         self.ddpg = DDPG()
        
#         self.prev_lineal = 0.0
#         self.prev_angular = 0.0

#         self.alpha_lineal=0.8
#         self.alpha_w=0.8

    
        
    
#     def centroidCallback(self, msg):
#         #Cogemos la información del centroide del mayor área segmentada.
#         x = msg.x
#         y = msg.y
#         area = msg.area 

#         vel_angular = 0.0
#         vel_lineal = 0.0

#         if area<80:
#             #Si el área máxima detectada es excesivamente pequeña, consideraremos que
#             #no existe objeto al que seguir, por lo que giraremos el robot en busca de objetos
#             vel_lineal = 0.0
#             if self.prev_angular<0: 
#                 vel_angular = -0.5
#             else:
#                 vel_angular=0.5
#         elif area>300:
#             #Si el área es excesivamente grande, asumiremos que estamos demasiado cerca del objeto,
#             #por lo que detendremos el robot
#             vel_lineal = 0.0
#             vel_angular = 0.0
#         else:
#             #En el caso general, seguimos la estrategia definida en la documentación: 
#             #utilizar un control proporcional para que la orientación del robot esté centrada con el
#             #centro del objeto (segmentación), y para que la velocidad lineal sea proporcional
#             #a la distancia con el objeto (área de la segmentación).
#             #Se utilizará un filtrado paso bajo para suavizar las velocidades del robot
#             vel_angular = float(((self.image_width/2.0) - x)/self.image_width*2*2)
#             vel_angular = math.tanh(vel_angular)*0.5
#             vel_angular = vel_angular*self.alpha_w + self.prev_angular*(1-self.alpha_w)

#             vel_lineal = min(max(1.0/math.sqrt(area)*15.0 , 0.05),0.3) 
#             vel_lineal = vel_lineal*self.alpha_lineal + self.prev_lineal*(1-self.alpha_lineal)

#         #Establecemoos la velocidad
#         cmd_vel_msg = Twist()
#         cmd_vel_msg.linear.x  = vel_lineal
#         cmd_vel_msg.angular.z = vel_angular
#         self.cmd_vel_pub.publish(cmd_vel_msg)

#         #actualizamos las velocidades de la iteración anterior, para realizar el filtrado paso bajo
#         self.prev_lineal = vel_lineal
#         self.prev_angular = vel_angular
#         rospy.loginfo("Velocidad:%f\n", vel_lineal)

def main():
    # gym.envs.register(
    #     id='GazeboRobotinoEnv-v0',
    #     entry_point='gym.envs.robotino:GazeboRobotinoEnv'
    # )

    rospy.init_node("line_follow")
    env = gym.make('GazeboRobotinoEnv-v0')
    print("Environment loaded")
    # check_env(env,warn=True,skip_render_check=True)
    stop_training = StopTrainingOnRewardThreshold(reward_threshold=-20,verbose=1)
    eval_callback = EvalCallback(env,callback_on_new_best=stop_training,verbose=1)
    model = DDPG(MlpPolicy,env,verbose=1, buffer_size=10000, train_freq=(3,"episode"))
    model.learn(total_timesteps=100000,callback=eval_callback)
    print("Training completed")
    rospy.spin()
    
if __name__=="__main__":
    try:
        main()
    except rospy.ROSInterruptException: pass