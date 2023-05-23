try:
    from gym.envs.robotino.gazeborobotino import GazeboRobotinoEnv
except ImportError:
    Box2D = None
