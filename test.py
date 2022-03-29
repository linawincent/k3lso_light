"""from model.robots.k3lso.k3lso import K3lso
from controllers.pose.pose_controller import PoseController
import pose"""
from model.robots.k3lso.k3lso_mpc import K3lso
from controllers.mpc.mpc_controller import MPCController
import mpc
import numpy as np


def position_check_gui():
    position, orientation = np.zeros(3), np.zeros(3)
    position[2] = input('z:\n')
    return position, orientation


def velocity_check_gui():
    velocity = np.zeros(3)
    velocity[0] = input('vx:\n')
    return velocity


def get_action_pos(position, orientation):
    controller.update_controller_params(position, orientation)
    return controller.get_action()


def get_action_vel(velocity):
    controller.update_controller_params(velocity)
    return controller.get_action()


"""def convert_pos_ros(command):
    # From radians to relative radians for Ros-commands and sign-change
    # Since k3lso calculates 0 from defined position
    offset_motor = np.array([
        0.07683732,  0.8524038, - 1.7048076,   0.07683732,  0.8524038,   1.7048076,
        0.07683732, - 0.8524038, - 1.7048076,   0.07683732, - 0.8524038,  1.7048076
        ])
    # Better zero-position for k3lso
    offset_orig = np.array([
        0,   0.1, -0.1, 0, -0.1, 0.1,
        -0.05, 0, 0, 0, 0.09, -0.05
    ])

    # Better zero-position for k3lso
    offset_orig = np.array([
        0.017, - 1.030, 1.480, 0.001, - 1.040, 1.430,
        0.007, - 1.090, 1.460, 0.050, - 1.190, 1.440
    ])

    transformed_command = (np.array(command) - offset_motor) / (2 * 3.14159265) # + offset_orig
    ids = [1, 2, 5, 6, 8]
    for j in ids:
        transformed_command[j] = -transformed_command[j]

    return transformed_command"""


def print_output(pybullet_action, ros_action):
    print('ros2 service call /k3lso_moteus/motors_test k3lso_msgs/srv/MotorsTest '
          '"{ids: [1,2,3,4,5,6,7,8,9,10,11,12], position:', np.around(ros_action, 5).tolist(), '}"')


if __name__ == '__main__':
    k3lso = K3lso('1', None)
    controller = MPCController(k3lso, None)
    mpc = mpc.MPC()

    """k3lso = K3lso(None)
    controller = PoseController(k3lso, 0)
    pose = pose.Pose()
    action = get_action_pos(np.zeros(3), np.zeros(3))
    print(action)
    print(pose.convert_pos_ros(action))"""


    # wanted_velocity = velocity_check_gui()
    action = get_action_vel(np.zeros(3))
    print(action)

