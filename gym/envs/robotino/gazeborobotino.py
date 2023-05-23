import rospy
import json
import numpy as np
import sys

from gym import utils, spaces
from gym.envs.robotino import gazebo_env
from geometry_msgs.msg import Twist
from gazebo_msgs.msg import ModelState
from gazebo_msgs.srv import SetModelState
from gazebo_msgs.srv import GetModelState
from sensor_msgs.msg import Image
from std_srvs.srv import Empty
from cv_bridge import CvBridge

from gym.utils import seeding
sys.path.append('/home/hidalgo/TFG/ros/src/blob_segmentation/scripts')
import segment_blob


class Circuit:
    def __init__(self,start,finish):
        self.start_posx = start[0]
        self.start_posy = start[1]
        self.start_posz = start[2]
        self.start_orx = start[3]
        self.start_ory = start[4]
        self.start_orz = start[5]
        self.start_orw = start[6]

        self.finish_x = finish[0]
        self.finish_y = finish[1]

class GazeboRobotinoEnv(gazebo_env.GazeboEnv):

    def __init__(self):

        # Import circuits from circuits.json
        self.num_circuits = 0
        self.circuits = []

        f = open('/home/hidalgo/.local/lib/python3.8/site-packages/gym/envs/robotino/circuits.json')
        data = json.load(f)

        for circuit in data['Circuits']:
            self.num_circuits += 1
            new_circuit = Circuit(circuit['start_position'], circuit['finish_position'])
            self.circuits.append(new_circuit)

        # Rospy service proxies

        self.unpause = rospy.ServiceProxy('/gazebo/unpause_physics', Empty)
        self.pause = rospy.ServiceProxy('/gazebo/pause_physics', Empty)
        self.reset_proxy = rospy.ServiceProxy('/gazebo/reset_simulation', Empty)
        self.set_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
        self.get_state = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)

        self.image_width = 64
        self.image_height = 48

        self.observation_space = spaces.Box(low=0, high=255,
                                            shape=(self.image_height,self.image_width,3), dtype=np.uint8)

        # Define action space
        self.max_linear_speed = 2.0
        self.max_angular_speed = 0.3

        self.action_space = spaces.Box(low=np.array([0.2, -self.max_angular_speed]),
                                        high=np.array([self.max_linear_speed, self.max_angular_speed]),
                                        dtype=np.float32)
        
        # Speed Publisher

        self.vel_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=5)
        self.blob_sub = rospy.Subscriber("/filtered_image", Image, queue_size=1)

        # Actual circuit, to know if the robot has reached the final coordinates

        self.reset()

    def step(self, action):
        rospy.wait_for_service('/gazebo/unpause_physics')
        try:
            self.unpause()
        except rospy.ServiceException as e:
            print("/gazebo/unpause_physics service call failed")

        vel_cmd = Twist()
        vel_cmd.linear.x = action[0]
        vel_cmd.angular.z = action[1]

        self.vel_pub.publish(vel_cmd)

        data = None
        while data is None:
            try:
                data = rospy.wait_for_message('/filtered_image', Image, timeout=5)
            except:
                pass

        rospy.wait_for_service('/gazebo/pause_physics')
        try:
            self.pause()
        except:
            print('/gazebo/pause_physics service call failed')
        
        state = CvBridge().imgmsg_to_cv2(data)

        robotino_coordinates = self.get_state('robotino','')
        x_pos = robotino_coordinates.pose.position.x
        y_pos = robotino_coordinates.pose.position.y

        if (abs(x_pos - self.start_circuit.finish_x) < 0.1 and abs(y_pos -  self.start_circuit.finish_y) < 0.1):
            done = True
            reward = 0
            print("Objective reached")
        else:
            if not segment_blob.detectLine(data):
                done = True
                reward = -5
                print("Line lost")
            else:
                done = False
                fila = state[(int)(0.8*self.image_height),:,:]
                indice = np.argmax(fila != [0,0,0])
                diff = abs(self.image_width/2-indice)
                if diff < self.image_width*0.1:
                    reward = 1
                else:
                    reward = -1

                reward -= 1.01
        
        return state, reward, done, {}



    def reset(self): 
        # Moves the robot to the start of a random circuit and makes and observation
        self.start_circuit = self.circuits[np.random.randint(0,len(self.circuits))]

        # from euler to quaternion
        state_msg = ModelState()
        state_msg.model_name = 'robotino'
        state_msg.pose.position.x = self.start_circuit.start_posx
        state_msg.pose.position.y = self.start_circuit.start_posy
        state_msg.pose.position.z = self.start_circuit.start_posz
        state_msg.pose.orientation.x = self.start_circuit.start_orx
        state_msg.pose.orientation.y = self.start_circuit.start_ory
        state_msg.pose.orientation.z = self.start_circuit.start_orz
        state_msg.pose.orientation.w = self.start_circuit.start_orw

        rospy.wait_for_service('/gazebo/set_model_state')
        try:
            self.set_state(state_msg)

        except rospy.ServiceException as e:
            print("/gazebo/set_model_state service call failed")

        # Unpause simulation to make observation

        rospy.wait_for_service('/gazebo/unpause_physics')
        try:
            self.unpause()
        except rospy.ServiceException as e:
            print('/gazebo/unpause_physics service call failed')
        
        # Reads an image
        data = None
        while data is None:
            try:
                data = rospy.wait_for_message('/filtered_image', Image, timeout=5)
            except:
                pass

        rospy.wait_for_service('/gazebo/pause_physics')
        try:
            self.pause()
        except:
            print('/gazebo/pause_physics service call failed')
        
        state = CvBridge().imgmsg_to_cv2(data)

        return state