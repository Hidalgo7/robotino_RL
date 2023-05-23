# robotino_RL

## Dependencies ##
### Python Packages ###
* Gym
```console
pip install gym
```
The files in the folder /robotino_RL/gym must be copied to the folder of the library ../python3.8/site-packages/gym.

Add the following lines to the file .../python3.8/site-packages/gym/envs/\_\_init.py__:
```python
# Robotino
# ----------------------------------------
register(
    id="GazeboRobotinoEnv-v0",
    entry_point="gym.envs.robotino:GazeboRobotinoEnv",
)
```

* Stable Baselines3
```console
pip install stable_baselines3
```
* OpenCV
```console
pip install opencv-python
```
### Ros Noetic ###
Instalation guide: http://wiki.ros.org/noetic/Installation
* Initialize ros workspace
```console
cd robotino_RL/ros/src
catkin_init_workspace
cd robotino_RL/ros
catkin_make
```
Add the  following line to ~\.bashrc
```console
source ~/robotino_RL/ros/devel/setup.bash
```

## Running ##
* Training model:
```console
roslaunch line_following training.launch
```
