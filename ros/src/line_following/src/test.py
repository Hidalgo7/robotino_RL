#!/usr/bin/env python3

import gym
import rospy
import rospkg
import os
from stable_baselines3 import DDPG
from stable_baselines3.common.evaluation import evaluate_policy

import time


def get_version_number(models_path):
    
    count = 0
    # Iterate directory
    for path in os.listdir(models_path):
        # check if current path is a file
        if os.path.isfile(os.path.join(models_path, path)):
            count += 1
    return count

def main():

    rospy.init_node("line_following_test")

    # get an instance of RosPack with the default search paths
    rospack = rospkg.RosPack()
    # get the file path for rospy_tutorials


    model_name = rospy.get_param("~model", None)

    if model_name == "":
        rospy.signal_shutdown("")
        print
        print("ERROR: Se debe indicar la carpeta de models desde la que se quiere cargar el modelo")
    else:
        env = gym.make('GazeboRobotinoTestEnv-v0')
        line_following_pkg = rospack.get_path('line_following')

        models_path = line_following_pkg + "/models/" + model_name + "/"

    # Load the trained agent
    # NOTE: if you have loading issue, you can pass `print_system_info=True`
    # to compare the system on which the model was trained vs the current one
    # model = DQN.load("dqn_lunar", env=env, print_system_info=True)
        model = DDPG.load(models_path + "line_following_model.zip", env=env)
        print("Model ", model_name, " loaded")

    # Evaluate the agent
    # NOTE: If you use wrappers with your environment that modify rewards,
    #       this will be reflected here. To evaluate with original rewards,
    #       wrap environment in a "Monitor" wrapper before other wrappers.
    #mean_reward, std_reward = evaluate_policy(model, model.get_env(), n_eval_episodes=10)

    # Enjoy trained agent
        vec_env = model.get_env()
        obs = vec_env.reset()

        times_list = []
        linea_centrada_list = []

        for i in range(10):
            done = False
            start_time = time.time()
            steps = 0
            linea_centrada = 0
            while not done:
                steps += 1
                action, _states = model.predict(obs, deterministic=True)
                obs, reward, done, _ = vec_env.step(action)

                if reward == -0.05:
                    linea_centrada += 1

            finish_time = time.time()
            
            times_list.append(finish_time-start_time)
            linea_centrada_list.append((linea_centrada/steps) * 100)

        file = open(models_path + "resultados_test.txt", 'w')
        file.write("Tiempo medio para finalizar el circuito: " + str(sum(times_list)/10) + "\n")
        file.write("Porcentaje del tiempo con la linea en el centro de la imagen: " + str(sum(linea_centrada_list)/10) + "%")
        file.close()
        fin = "#" * 30
        print(fin)

        rospy.spin()
    
if __name__=="__main__":
    try:
        main()
    except rospy.ROSInterruptException: pass