#!/usr/bin/env python3

import gym
import rospy
import rospkg
import os
from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import DDPG
from stable_baselines3.common.callbacks import StopTrainingOnRewardThreshold, EvalCallback
from stable_baselines3.ddpg.policies import MlpPolicy, CnnPolicy, MultiInputPolicy

def get_version_number(models_path):
    
    count = 0
    # Iterate directory
    for path in os.listdir(models_path):
        # check if current path is a file
        if os.path.isfile(os.path.join(models_path, path)):
            count += 1
    return count

def main():

    rospy.init_node("line_following_training")

    # get an instance of RosPack with the default search paths
    rospack = rospkg.RosPack()
    # get the file path for rospy_tutorials
    line_following_pkg = rospack.get_path('line_following')

    reward_th = rospy.get_param("~reward_threshold", -100)
    policy = rospy.get_param("~policy", 0)
    buff_size = rospy.get_param("~buff_size",10000)
    train_hz = rospy.get_param("~train_hz",3)
    timesteps = rospy.get_param("~timesteps",200000)

    policies = [MlpPolicy, CnnPolicy, MultiInputPolicy]

    env = gym.make('GazeboRobotinoTrainEnv-v0')
    print("Environment loaded")
    # check_env(env,warn=True,skip_render_check=True)
    stop_training = StopTrainingOnRewardThreshold(reward_threshold=reward_th,verbose=1)
    eval_callback = EvalCallback(env,callback_on_new_best=stop_training,verbose=1)
    model = DDPG(policies[policy],env,verbose=1, buffer_size=buff_size, train_freq=(train_hz,"episode"))
    model.learn(total_timesteps=timesteps,callback=eval_callback)
    print("Training completed")
    models_path = line_following_pkg + "/models/"
    version_num = str(get_version_number(models_path))
    print('File count: ', version_num)
    model_name = "line_following_model" + "_v" + version_num
    model.save(models_path + model_name)
    print('Model saved: ', models_path + model_name)
    rospy.spin()
    
if __name__=="__main__":
    try:
        main()
    except rospy.ROSInterruptException: pass