import numpy as np


class IMU:

    def __init__(self):
        # TODO: quaternions from ROS
        self.qx = 0
        self.qy = 0
        self.qz = 0
        self.qw = 0
        self.pos = np.array([0., 0., 0.])

    def get_position(self):
        return [self.x, self.y, self.z]

    def get_orientation(self):
        return [self]

    def add_pos(self, lin_acc, ang_vel, time):
        t = np.power(time, 2) / 2
        g = 10.1  # gravitational offset for the acceleration in z-direction
        self.pos += np.multiply(lin_acc, t)
        self.x += lin_acc[0] / 2 * time**2
        self.y += lin_acc[1] / 2 * time ** 2
        self.z += ((lin_acc[2] - g) / 2 * time ** 2)

