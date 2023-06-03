try:
    from gym.envs.robotino.gazeborobotino import GazeboRobotinoTrainEnv
    from gym.envs.robotino.gazeborobotino import GazeboRobotinoTestEnv
except ImportError:
    Box2D = None
