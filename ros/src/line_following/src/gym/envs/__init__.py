from gym.envs.registration import register
from gym.envs.robotino.GazeboRobotinoEnv import GazeboRobotinoEnv

register(
    id='GazeboRobotinoEnv',
    entry_point='gym.envs.robotino:GazeboRobotinoEnv'
)