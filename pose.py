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
        hej = self.format_values(values[0], values[1], values[2], values[3], values[4], values[5])
        self.controller.update_controller_params(hej[0], hej[1])
        self.signal = self.controller.get_action()

    def get_signal(self):
        return self.signal




