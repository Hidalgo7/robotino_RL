#!/usr/bin/env python3

import rospy
import curses
import time
import sys
import io
import json

from gazebo_msgs.msg import ModelState
from gazebo_msgs.srv import SetModelState
from gazebo_msgs.srv import GetModelState
from sensor_msgs.msg import Image
from std_srvs.srv import Empty

from cv_bridge import CvBridge

segment_blob_path = '/home/hidalgo/TFG/ros/src/blob_segmentation/scripts'
sys.path.append(segment_blob_path)

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

class Robot():
    def __init__(self):
        self.unpause = rospy.ServiceProxy('/gazebo/unpause_physics', Empty)
        self.pause = rospy.ServiceProxy('/gazebo/pause_physics', Empty)
        self.reset_proxy = rospy.ServiceProxy('/gazebo/reset_simulation', Empty)
        self.set_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
        self.get_state = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)

        self.filtered_image_topic = "/filtered_image"

        self.image_width = 128
        self.image_height = 96

        self.actual_circuit = -1
        self.num_circuits = 0
        self.circuits = []

        circuits_path = "/home/hidalgo/.local/lib/python3.8/site-packages/gym/envs/robotino/circuits.json"
        #circuits_path = "/usr/local/lib/python3.8/dist-packages/gym/envs/robotino/circuits.json"
        f = open(circuits_path)
        data = json.load(f)

        for circuit in data['Circuits']:
            self.num_circuits += 1
            new_circuit = Circuit(circuit['start_position'], circuit['finish_position'])
            self.circuits.append(new_circuit)

    def array_max_index(self, array):
        index_max = None
        max_val = float('-inf')

        for i, subarray in enumerate(array):
            max_subarray = max(subarray)
            if max_subarray > max_val:
                max_val = max_subarray
                index_max = i

        return index_max

    def mover(self, direccion):
        try:
            robotino_coordinates = self.get_state('robotino','')
        except rospy.ServiceException as e:
            print("/gazebo/get_model state service call failed")

        x_pos = robotino_coordinates.pose.position.x
        y_pos = robotino_coordinates.pose.position.y

        if direccion == 'w':
            y_pos += 0.01
        elif direccion == 'a':
            x_pos -= 0.01
        elif direccion == 's':
            y_pos -= 0.01
        elif direccion == 'd':
            x_pos += 0.01

        state_msg = ModelState()
        state_msg.model_name = 'robotino'
        state_msg.pose.position.x = x_pos
        state_msg.pose.position.y = y_pos
        state_msg.pose.position.z = robotino_coordinates.pose.position.z
        state_msg.pose.orientation.x = robotino_coordinates.pose.orientation.x
        state_msg.pose.orientation.y = robotino_coordinates.pose.orientation.y
        state_msg.pose.orientation.z = robotino_coordinates.pose.orientation.z
        state_msg.pose.orientation.w = robotino_coordinates.pose.orientation.w

        try:
            self.set_state(state_msg)

        except rospy.ServiceException as e:
            print("/gazebo/set_model_state service call failed")

        #print("X: {}\n Y:{}".format(x_pos,y_pos))

    def rotar(self, direccion):
        try:
            robotino_coordinates = self.get_state('robotino','')
        except rospy.ServiceException as e:
            print("/gazebo/get_model state service call failed")

        z_axis = robotino_coordinates.pose.orientation.z

        if direccion == "+":
            z_axis += 0.01
        elif direccion == "-":
            z_axis -= 0.01
        
        state_msg = ModelState()
        state_msg.model_name = 'robotino'
        state_msg.pose.position.x = robotino_coordinates.pose.position.x
        state_msg.pose.position.y = robotino_coordinates.pose.position.y
        state_msg.pose.position.z = robotino_coordinates.pose.position.z
        state_msg.pose.orientation.x = robotino_coordinates.pose.orientation.x
        state_msg.pose.orientation.y = robotino_coordinates.pose.orientation.y
        state_msg.pose.orientation.z = z_axis
        state_msg.pose.orientation.w = robotino_coordinates.pose.orientation.w

        try:
            self.set_state(state_msg)

        except rospy.ServiceException as e:
            print("/gazebo/set_model_state service call failed")

        #print("X: {}\n Y:{}".format(x_pos,y_pos))


    def recompensa(self):

        data = None
        while data is None:
            try:
                data = rospy.wait_for_message(self.filtered_image_topic, Image, timeout=5)
            except:
                pass

        state = CvBridge().imgmsg_to_cv2(data)

        try:
            robotino_coordinates = self.get_state('robotino','')
        except rospy.ServiceException as e:
            print("/gazebo/get_model state service call failed")

        robotino_coordinates = self.get_state('robotino','')
        x_pos = robotino_coordinates.pose.position.x
        y_pos = robotino_coordinates.pose.position.y

        if (abs(x_pos - self.circuits[self.actual_circuit].finish_x) < 0.1 and abs(y_pos -  self.circuits[self.actual_circuit].finish_y) < 0.1):
            self.switch_circuit()
            print("Objective reached")
        else:
            fila = state[(int)(0.95*self.image_height),:,:]
            #print("Fila: ", type(fila))
            indice = self.array_max_index(fila)
            #indice = np.argmax(fila != [0,0,0])
            #print("Indice: ", indice)
            diff = abs(self.image_width/2-indice) 
            #print("Diff: ", diff)
            print("Treshold: ", self.image_width*0.05)
            if diff < self.image_width*0.05:
                reward = 0
            else:
                reward = -diff 
            print("Reward: ", reward)
            
    
    def get_pose(self):
        try:
            robotino_coordinates = self.get_state('robotino','')
        except rospy.ServiceException as e:
            print("/gazebo/get_model state service call failed")

        print(robotino_coordinates.pose.position)
        print(robotino_coordinates.pose.orientation)

    def switch_circuit(self):
        if self.actual_circuit < self.num_circuits-1:
            self.actual_circuit += 1
        else:
            self.actual_circuit = 0

        start_circuit = self.circuits[self.actual_circuit]
        
        state_msg = ModelState()
        state_msg.model_name = 'robotino'
        state_msg.pose.position.x = start_circuit.start_posx
        state_msg.pose.position.y = start_circuit.start_posy
        state_msg.pose.position.z = start_circuit.start_posz
        state_msg.pose.orientation.x = start_circuit.start_orx
        state_msg.pose.orientation.y = start_circuit.start_ory
        state_msg.pose.orientation.z = start_circuit.start_orz
        state_msg.pose.orientation.w = start_circuit.start_orw

        rospy.wait_for_service('/gazebo/set_model_state')
        try:
            self.set_state(state_msg)

        except rospy.ServiceException as e:
            print("/gazebo/set_model_state service call failed")



if __name__ == "__main__":

    time.sleep(5)

    rospy.init_node("mover_robot")
    print("-----------------------------------------")
    print("Simple keyboard teleop node in python")
    print("Use WASD keys to command position values")
    print("Press ENTER to quit")
    print("-----------------------------------------")
    # get the curses screen window
    screen = curses.initscr()
    
    # turn off input echoing
    curses.noecho()
    # respond to keys immediately (don't wait for enter)
    curses.cbreak()

    direcciones = ['w','a','s','d']
    robot = Robot()

    #env = gym.make('GazeboRobotinoTestEnv-v0')
    

    try:
        while True:
            char = chr(screen.getch())

            if ord(char) == curses.KEY_ENTER:
                break
            
            if char in direcciones:
                robot.mover(char)
                robot.recompensa()
                #print("Robot movido")
            elif char == 'q':
                robot.rotar('+')
            elif char == 'e':
                robot.rotar('-')
            elif char == 'p':
                robot.get_pose()
            elif char == 'n':
                robot.switch_circuit()
            

        

    except Exception as e:
        print(str(e))
