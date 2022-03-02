import numpy as np

from robot_gym.model.equipment import camera
from robot_gym.util import pybullet_data


class Robot:

    def __init__(self, motor_control_mode):
        self.motor_control_mode = motor_control_mode
