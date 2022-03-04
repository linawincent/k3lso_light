import sys

from controllers.pose.pose_controller import PoseController
from model.robots.k3lso.k3lso import K3lso 

class Pose:

    def __init__(self):
        kelso = K3lso(None)
        self.controller = PoseController(kelso, 0)
        self.signal = []

    def format_values(self, xpos, ypos, zpos, roll, pitch, yaw):
        position = [xpos, ypos, zpos]
        orientation = [roll, pitch, yaw]
        return position, orientation

    def update_signal(self, values):
        self.signal = self.controller.get_action(
            self.format_values(values[1], values[2], values[3], values[4], values[5], values[6]))
        
    def get_signal(self):
        return self.signal




