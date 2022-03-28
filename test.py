from model.robots.k3lso.k3lso import K3lso
# from controllers.pose.pose_controller import PoseController
# import pose
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


"""def get_action(position, orientation):
    controller.update_controller_params(position, orientation)
    return controller.get_action()"""


def get_action(velocity):
    controller.update_controller_params(velocity)
    return controller.get_action()


def convert_pos_ros(command):
    # From radians to relative radians for Ros-commands and sign-change
    # Since k3lso calculates 0 from defined position
    offset_motor = np.array([
        -0.03964886725138972, 1.1035218357931036, -1.9554858419361683,
        -0.03964886725138994, 1.1035218357931036, 1.9554858419361683,
        -0.03964886725138972, -1.1035218357931036, -1.9554858419361683,
        -0.03964886725138994, -1.1035218357931036, 1.9554858419361683
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

    transformed_command = (np.array(command) - offset_motor) / (2 * 3.14159265) + offset_orig
    ids = [1, 2, 5, 6, 8]
    for j in ids:
        transformed_command[j] = -transformed_command[j]

    return transformed_command


def print_output(pybullet_action, ros_action):
    print('ros2 service call /k3lso_moteus/motors_test k3lso_msgs/srv/MotorsTest '
          '"{ids: [1,2,3,4,5,6,7,8,9,10,11,12], position:', np.around(ros_action, 5).tolist(), '}"')


if __name__ == '__main__':
    k3lso = K3lso(1, None, 0)
    controller = MPCController(k3lso, 0)
    # pose = pose.Pose()
    mpc = mpc.MPC()

    # wanted_position, wanted_orientation = position_check_gui()
    """steps = int(input('Number of steps:\n'))
    step_position, step_orientation = np.zeros(3), np.zeros(3)

    for i in range(steps + 1):
        action = get_action(step_position, step_orientation)
        print_output(action, pose.convert_pos_ros(pose, action))
        step_position += wanted_position / steps
"""

    wanted_velocity = velocity_check_gui()
    action = get_action(wanted_velocity)
    print(action)

