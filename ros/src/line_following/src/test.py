#!/usr/bin/env python3

import gym
import rospy
import rospkg
import os
from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import DDPG
from stable_baselines3.common.evaluation import evaluate_policy


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
    line_following_pkg = rospack.get_path('line_following')

    reward_th = rospy.get_param("~reward_threshold", -200)
    policy = rospy.get_param("~policy", 0)
    buff_size = rospy.get_param("~buff_size",10000)
    train_hz = rospy.get_param("~train_hz",3)
    timesteps = rospy.get_param("~timesteps",100000)


    env = gym.make('GazeboRobotinoEnv-v0')

    models_path = line_following_pkg + "/models/"
    version_num = str(get_version_number(models_path)-1)
    print('File count: ', version_num)
    model_name = "line_following_model" + "_v" + version_num

    # Load the trained agent
    # NOTE: if you have loading issue, you can pass `print_system_info=True`
    # to compare the system on which the model was trained vs the current one
    # model = DQN.load("dqn_lunar", env=env, print_system_info=True)
    model = DDPG.load(models_path + model_name, env=env)
    print("Model loaded")

    # Evaluate the agent
    # NOTE: If you use wrappers with your environment that modify rewards,
    #       this will be reflected here. To evaluate with original rewards,
    #       wrap environment in a "Monitor" wrapper before other wrappers.
    mean_reward, std_reward = evaluate_policy(model, model.get_env(), n_eval_episodes=10)

    # Enjoy trained agent
    vec_env = model.get_env()
    obs = vec_env.reset()
    for i in range(1000):
        action, _states = model.predict(obs, deterministic=True)
        obs, rewards, dones, info = vec_env.step(action)

    rospy.spin()
    
if __name__=="__main__":
    try:
        main()
    except rospy.ROSInterruptException: pass