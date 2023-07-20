import rospy
import rospkg
import json
import numpy as np
import sys
import os
from datetime import date

from gym import spaces
from gym.envs.robotino import gazebo_env
from geometry_msgs.msg import Twist
from gazebo_msgs.msg import ModelState
from gazebo_msgs.srv import SetModelState
from gazebo_msgs.srv import GetModelState
from sensor_msgs.msg import Image
from std_srvs.srv import Empty
from cv_bridge import CvBridge

#segment_blob_path = '/home/hidalgo/TFG/ros/src/blob_segmentation/scripts'
segment_blob_path = '/home/bee/ikerkuntza/tfg/2022-2023/IkerHidalgo/robotino_RL/ros/src/blob_segmentation/scripts'
sys.path.append(segment_blob_path)
import segment_blob

line_weight_list = [0.95, 1.0, 0.9, 0.7]
time_weight_list = [0.05, 0.0, 0.1, 0.3]
i = 0


# PARAMETERS
max_linear_speed = 0.4
min_linear_speed = 0.1
max_angular_speed = 0.5
image_width = 128
image_height = 96
line_weight = line_weight_list[i]
time_weight = time_weight_list[i]
error_meta = 0.2
error_imagen = 0.05
fila_linea = 0.95

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

class GazeboRobotinoTrainEnv(gazebo_env.GazeboEnv):

    def __init__(self):

        # ROS topic names
        self.cmd_vel_topic = "/cmd_vel"
        self.filtered_image_topic = "/filtered_image"

        # Rospy service proxies
        self.unpause = rospy.ServiceProxy('/gazebo/unpause_physics', Empty)
        self.pause = rospy.ServiceProxy('/gazebo/pause_physics', Empty)
        self.reset_proxy = rospy.ServiceProxy('/gazebo/reset_simulation', Empty)
        self.set_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
        self.get_state = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)

        # Define observation_space
        self.image_width = 128
        self.image_height = 96

        self.observation_space = spaces.Box(low=0, high=255,
                                            shape=(self.image_height,self.image_width,3), dtype=np.uint8)

        # Define action space
        self.max_linear_speed = max_linear_speed
        self.min_linear_speed = min_linear_speed
        self.max_angular_speed = max_angular_speed

        self.action_space = spaces.Box(low=np.array([self.min_linear_speed, -self.max_angular_speed]),
                                        high=np.array([self.max_linear_speed, self.max_angular_speed]),
                                        dtype=np.float32)
        
        # Speed Publisher
        self.vel_pub = rospy.Publisher(self.cmd_vel_topic, Twist, queue_size=5)

        # Filtered image subscriber
        self.blob_sub = rospy.Subscriber(self.filtered_image_topic, Image, queue_size=1)

        # Import circuits from circuits.json
        self.num_circuits = 0
        self.circuits = []

        #circuits_path = "/home/hidalgo/.local/lib/python3.8/site-packages/gym/envs/robotino/circuits.json"
        circuits_path = "/usr/local/lib/python3.8/dist-packages/gym/envs/robotino/circuits.json"
        f = open(circuits_path)
        data = json.load(f)

        for circuit in data['Circuits']:
            self.num_circuits += 1
            new_circuit = Circuit(circuit['start_position'], circuit['finish_position'])
            self.circuits.append(new_circuit)

        # Steps per episode counter
        self.steps = 0

        # self.rotation_buffer = []
        # self.rotation_buffer_length = 10

        self.step_reward = -1 # Constante asociada a la reward por cada step
        
        self.episode_reward = 0
        self.num_episodes = 1

        # Line and time rewards weight
        self.line_weight = line_weight
        self.time_weight = time_weight

        # Fichero para guardar las recompensas de los episodios
        rospack = rospkg.RosPack()

        model_path = rospack.get_path("line_following") + "/models/" + str(date.today()) + "-v0"
                
        while os.path.exists(model_path):
            model_path = model_path[:-1] + str(int(model_path[-1])+1)
                
        os.makedirs(model_path)

        self.reward_file_path = model_path + "/rewards.txt"
        self.info_file_path = model_path + "/info.txt"

        # Save training info
        f = open(self.info_file_path, 'w')
        image_info = "Image width: " + str(self.image_width) + "\t" + "Image height: " + str(self.image_height) + "\n"
        vel_info = "Linear max: " + str(self.max_linear_speed) + "\t" + "Linear min: " + str(self.min_linear_speed) + "\t" + "Angular: " + str(self.max_angular_speed) + "\n"
        weight_info = "Line weight: " + str(self.line_weight) + "\t" + "Time weight: " + str(self.time_weight) + "\n"
        error_info = "Error meta: " + str(error_meta) + "\t" + "Error imagen: " + str(error_imagen) + "\n"
        line_info = "Fila linea: " + str(fila_linea) + "\n"
        info = image_info + vel_info + weight_info + error_info + line_info
        f.write(info)
        f.close()
        

        self.reset()

    def array_max_index(self, array):
        index_max = None
        max_val = float('-inf')

        for i, subarray in enumerate(array):
            max_subarray = max(subarray)
            if max_subarray > max_val:
                max_val = max_subarray
                index_max = i

        return index_max
    
    def calculate_reward(self,state):
        # Se obtiene la posicion (x,y) del robot
        robotino_coordinates = self.get_state('robotino','')
        x_pos = robotino_coordinates.pose.position.x
        y_pos = robotino_coordinates.pose.position.y

        if (abs(x_pos - self.start_circuit.finish_x) < error_meta and abs(y_pos -  self.start_circuit.finish_y) < error_meta):
            # Si la posicion del robot es igual a la meta del circuito (con un error posible de 0.1 en cada eje)
            # se finaliza el episodio con una recompensa neutra.
            done = True
            reward = 0
            self.steps = 0
            print("Objective reached")
        else:
            if not segment_blob.detectLine(state):
                # Si no se detecta la linea en camara se finaliza el episodio con una recompensa negativa variable
                # en funcion de los pasos realizados, penalizando menos al robot si ha conseguido llegar mas lejos 
                # en el circuito (mas pasos).
                done = True
                reward = min(-1000 + self.steps,-500)
                self.steps = 0
                print("Line lost")
            else:
                # Si no se da ninguno de los casos anteriores el episodio continua. La recompensa se calcula en 
                # funcion de la desviacion de la linea al centro de la camara y el numero de oscilaciones en las 
                # ultimas 10 acciones. Se normalizan ambas en el rango [0,1] y se le aplica un peso proporcional
                # a cada recompensa individual para calcular la recompensa total.
                done = False
                self.steps += 1
                fila = state[(int)(fila_linea*self.image_height),:,:]
                indice = self.array_max_index(fila)
                diff = abs(self.image_width/2-indice)

                if diff < self.image_width*error_imagen: # Se permite un error del 5% de la anchura de la imagen 
                    desv_linea = 0
                else:
                    desv_linea = (-diff + self.image_width/2) / ((self.image_width/2) - self.image_width*error_imagen) -1

                # print("Width: ", self.image_width)
                # print("Fila: ", type(fila))
                # print("Indice: ", indice)
                # print("Diff: ", diff)
                # print("Desviacion linea: ", desv_linea)

                # Evaluar los cambios de direccion
                # i = 0
                # j = 1

                # cambios_direccion = 0
                
                # while j < len(self.rotation_buffer): # Mientras el segundo indice sea menor que la longitud del buffer
                #     vel_ang_1 = self.rotation_buffer[i]
                #     vel_ang_2 = self.rotation_buffer[j]

                #     if vel_ang_1 * vel_ang_2 < 0: 
                #         # Si las dos velocidades angulares tienen diferente signo, hay un cambio de direccion
                #         cambios_direccion += 1
                #     i += 1
                #     j += 1
                
                # if cambios_direccion > 1:
                #     # Si hay mas de un cambio de direccion se penaliza (con normalizacion)
                #     cambios_direccion -= 1
                #     oscilaciones = -cambios_direccion / (len(self.rotation_buffer)-2)
                # else:
                #     # En caso contrario (un cambio o ninguno), no se penaliza
                #     oscilaciones = 0

                reward = desv_linea * self.line_weight + self.step_reward * self.time_weight # Proporcion 95/5

                #print("Recompensa: {}".format(reward))

        return reward,done

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
                data = rospy.wait_for_message(self.filtered_image_topic, Image, timeout=5)
            except:
                pass

        rospy.wait_for_service('/gazebo/pause_physics')
        try:
            self.pause()
        except:
            print('/gazebo/pause_physics service call failed')

        # if len(self.rotation_buffer) == self.rotation_buffer_length:
        #     self.rotation_buffer.pop(0)
        #     self.rotation_buffer.append(action[1])
        # else:
        #     self.rotation_buffer.append(action[1])

        state = CvBridge().imgmsg_to_cv2(data)

        reward, done = self.calculate_reward(state)
        
        self.episode_reward += reward

        if done:
            # Save Reward
            f = open(self.reward_file_path, 'a')
            f.write("{} {}\n".format(self.num_episodes,self.episode_reward))
            f.close()
            print("Episode Reward: ", self.episode_reward)
            self.episode_reward = 0
            self.num_episodes += 1
              

        return state, reward, done, {}



    def reset(self): 
        # Moves the robot to the start of a random circuit and makes and observation

        # Select random circuit
        self.start_circuit = self.circuits[np.random.randint(0,len(self.circuits))]

        # Set robot pose to the starting point of selected circuit
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
                data = rospy.wait_for_message(self.filtered_image_topic, Image, timeout=5)
            except:
                pass

        rospy.wait_for_service('/gazebo/pause_physics')
        try:
            self.pause()
        except:
            print('/gazebo/pause_physics service call failed')
        
        state = CvBridge().imgmsg_to_cv2(data)

        return state

class GazeboRobotinoTestEnv(gazebo_env.GazeboEnv):
    def __init__(self):
        # ROS topic names
        self.cmd_vel_topic = "/cmd_vel"
        self.filtered_image_topic = "/filtered_image"

        # Rospy service proxies
        self.unpause = rospy.ServiceProxy('/gazebo/unpause_physics', Empty)
        self.pause = rospy.ServiceProxy('/gazebo/pause_physics', Empty)
        self.reset_proxy = rospy.ServiceProxy('/gazebo/reset_simulation', Empty)
        self.set_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
        self.get_state = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)

        # Define observation space
        self.image_width = image_width
        self.image_height = image_height

        self.observation_space = spaces.Box(low=0, high=255,
                                            shape=(self.image_height,self.image_width,3), dtype=np.uint8)
        
        # Define action space
        self.max_linear_speed = max_linear_speed
        self.min_linear_speed = min_linear_speed
        self.max_angular_speed = max_angular_speed

        self.action_space = spaces.Box(low=np.array([self.min_linear_speed, -self.max_angular_speed]),
                                        high=np.array([self.max_linear_speed, self.max_angular_speed]),
                                        dtype=np.float32)
        
        # Speed Publisher
        self.vel_pub = rospy.Publisher(self.cmd_vel_topic, Twist, queue_size=5)

        # Filtered image subscriber
        self.blob_sub = rospy.Subscriber(self.filtered_image_topic, Image, queue_size=1)

        # Steps per episode counter
        self.steps = 0

        self.step_reward = -1 # Constante asociada a la reward por cada step

        # Line and time rewards weight
        self.line_weight = line_weight
        self.time_weight = time_weight

        # Finishing coordinates
        self.finish_x = 3.5845
        self.finish_y = 3.1228

    def array_max_index(self, array):
        index_max = None
        max_val = float('-inf')

        for i, subarray in enumerate(array):
            max_subarray = max(subarray)
            if max_subarray > max_val:
                max_val = max_subarray
                index_max = i

        return index_max
    
    def calculate_reward(self,state):
        # Se obtiene la posicion (x,y) del robot
        robotino_coordinates = self.get_state('robotino','')
        x_pos = robotino_coordinates.pose.position.x
        y_pos = robotino_coordinates.pose.position.y

        if (abs(x_pos - self.finish_x) < error_meta and abs(y_pos -  self.finish_y) < error_meta):
            # Si la posicion del robot es igual a la meta del circuito (con un error posible de 0.1 en cada eje)
            # se finaliza el episodio con una recompensa neutra.
            done = True
            reward = 0
            self.steps = 0
            print("Objective reached")
        else:
            if not segment_blob.detectLine(state):
                # Si no se detecta la linea en camara se finaliza el episodio con una recompensa negativa variable
                # en funcion de los pasos realizados, penalizando menos al robot si ha conseguido llegar mas lejos 
                # en el circuito (mas pasos).
                done = True
                reward = min(-1000 + self.steps,-500)
                self.steps = 0
                print("Line lost")
            else:
                # Si no se da ninguno de los casos anteriores el episodio continua. La recompensa se calcula en 
                # funcion de la desviacion de la linea al centro de la camara y el numero de oscilaciones en las 
                # ultimas 10 acciones. Se normalizan ambas en el rango [0,1] y se le aplica un peso proporcional
                # a cada recompensa individual para calcular la recompensa total.
                done = False
                self.steps += 1
                fila = state[(int)(fila_linea*self.image_height),:,:]
                indice = self.array_max_index(fila)
                diff = abs(self.image_width/2-indice)

                if diff < self.image_width*error_imagen: # Se permite un error del 5% de la anchura de la imagen 
                    desv_linea = 0
                else:
                    desv_linea = (-diff + self.image_width/2) / ((self.image_width/2) - self.image_width*error_imagen) -1

                #print("Width: ", self.image_width)
                #print("Fila: ", type(fila))
                #print("Indice: ", indice)
                #print("Diff: ", diff)
                #print("Desviacion linea: ", desv_linea)

                # Evaluar los cambios de direccion
                # i = 0
                # j = 1

                # cambios_direccion = 0
                
                # while j < len(self.rotation_buffer): # Mientras el segundo indice sea menor que la longitud del buffer
                #     vel_ang_1 = self.rotation_buffer[i]
                #     vel_ang_2 = self.rotation_buffer[j]

                #     if vel_ang_1 * vel_ang_2 < 0: 
                #         # Si las dos velocidades angulares tienen diferente signo, hay un cambio de direccion
                #         cambios_direccion += 1
                #     i += 1
                #     j += 1
                
                # if cambios_direccion > 1:
                #     # Si hay mas de un cambio de direccion se penaliza (con normalizacion)
                #     cambios_direccion -= 1
                #     oscilaciones = -cambios_direccion / (len(self.rotation_buffer)-2)
                # else:
                #     # En caso contrario (un cambio o ninguno), no se penaliza
                #     oscilaciones = 0

                reward = desv_linea * self.line_weight + self.step_reward * self.time_weight # Proporcion 95/5

                #print("Recompensa: {}".format(reward))

        return reward,done

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
                data = rospy.wait_for_message(self.filtered_image_topic, Image, timeout=5)
            except:
                pass

        rospy.wait_for_service('/gazebo/pause_physics')
        try:
            self.pause()
        except:
            print('/gazebo/pause_physics service call failed')

        # if len(self.rotation_buffer) == self.rotation_buffer_length:
        #     self.rotation_buffer.pop(0)
        #     self.rotation_buffer.append(action[1])
        # else:
        #     self.rotation_buffer.append(action[1])

        state = CvBridge().imgmsg_to_cv2(data)

        reward,done = self.calculate_reward(state)   

        return state, reward, done, {}
    
    def reset(self):
        # Moves the robot to the start the circuit and makes and observation
        state_msg = ModelState()
        state_msg.model_name = 'robotino'
        state_msg.pose.position.x = 4.525
        state_msg.pose.position.y = 2.989
        state_msg.pose.position.z = 0.14602241423442358
        state_msg.pose.orientation.x = 0
        state_msg.pose.orientation.y = 0
        state_msg.pose.orientation.z = -0.0706
        state_msg.pose.orientation.w = 0.9975

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
                data = rospy.wait_for_message(self.filtered_image_topic, Image, timeout=5)
            except:
                pass

        rospy.wait_for_service('/gazebo/pause_physics')
        try:
            self.pause()
        except:
            print('/gazebo/pause_physics service call failed')
        
        state = CvBridge().imgmsg_to_cv2(data)

        return state
