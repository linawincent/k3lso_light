import time
import numpy as np


def q_to_euler(q):
    """ Returns the roll, pitch, yaw from the IMU quaternions """
    orientation = np.zeros(3)
    orientation[0] = np.arctan2(2 * (q[3] * q[0] + q[1] * q[2]), (1 - 2 * (q[0]**2 * q[1]**2)))
    orientation[1] = np.arcsin(2 * (q[3] * q[1] - q[0] * q[2]))
    orientation[2] = np.arctan2(2 * (q[3] * q[2] + q[0] * q[1]), (1 - 2 * (q[1]**2 * q[2]**2)))
    return orientation


class IMU:

    def __init__(self, start_pos):
        # TODO: quaternions from ROS
        self.q = np.array([0., 0., 0., 1.])
        self.angular_vel = np.array([0., 0., 0.])
        self.lin_acc = np.array([0., 0., 0.])

        self.position = start_pos
        self.orientation = np.array([0., 0., 0.])
        self.velocity = np.array([0., 0., 0.])

        self.t0 = time.perf_counter()

    def get_position(self):
        return self.position

    def get_orientation(self):
        return q_to_euler(self.q)

    def get_velocity(self):
        return self.velocity

    def get_angular_velocity(self):
        return self.angular_vel

    def get_lin_acc(self):
        return self.lin_acc

    def get_q(self):
        return self.q

    def update(self, q, lin_acc, ang_vel):
        g = 10.1  # gravitational offset for the acceleration in z-direction
        t1 = time.perf_counter()
        dt = t1 - self.t0
        self.t0 = t1

        """ Update values from IMU"""
        self.q = q
        self.angular_vel = ang_vel
        self.lin_acc = lin_acc.copy()

        """ Rotation matrix for q"""
        rot_matrix = np.array([
            (1 - 2 * (q[1] ** 2 + q[2] ** 2)), 2 * (q[0] * q[1] + q[3] * q[2]), 2 * (q[3] * q[1] + q[0] * q[2]),
            2 * (q[0] * q[1] + q[3] * q[2]), (1 - 2 * (q[0]**2 + q[2]**2)), 2 * (q[1] * q[2] + q[3] * q[0]),
            2 * (q[0] * q[2] + q[3] * q[1]), 2 * (q[3] * q[0] + q[1] * q[2]), (1 - 2 * (q[0]**2 + q[1]**2))
        ])
        rot_matrix = rot_matrix.reshape((3, 3))

        """ Remove gravitational acceleration for position calculation"""
        if np.abs(lin_acc[2] - g) < 0.3:
            lin_acc[2] = g

        lin_acc[2] = lin_acc[2] - g

        """ Calculate position and velocity in world frame"""
        self.orientation = q_to_euler(q)
        self.velocity += np.matmul(rot_matrix, lin_acc) * dt
        self.position += self.velocity * dt  # + 0.5 * np.matmul(rot_matrix, self.lin_acc) * dt * dt

if __name__ == '__main__':
    imu = IMU(np.array([0.0, 0.0, 0.0]))
    imu.update([0.0, 0.0, 0.0, 0.0],[0.1, 0.1, 10.2],[0.1, 0.1, 0.1])
    print(imu.lin_acc)