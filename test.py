from model.robots.k3lso.k3lso import K3lso
from controllers.pose.pose_controller import PoseController
import numpy as np


def check_gui():
    position, orientation = np.zeros(3), np.zeros(3)
    position[0] = input('x: \n')
    position[1] = input('y:\n')
    position[2] = input('z:\n')
    orientation[0] = input('roll: \n')
    orientation[1] = input('pitch:\n')
    orientation[2] = input('yaw:\n')
    return position, orientation


def action():
    check = input('Input values y?:\n')
    if check == 'y':
        position, orientation = check_gui()
    else:
        position = [0., 0., 0.]
        orientation = [0., 0., 0.]
    controller.update_controller_params(position, orientation)
    return controller.get_action()


def convert_pos_ros(command):
    offset = np.array([
        -0.04962033801483967, 0.7540106309498033, -1.2809585946909632,
        -0.04962033801483945, 0.7540106309498033, 1.2809585946909632,
        -0.04962033801483967, -0.7540106309498033, -1.2809585946909632,
        -0.04962033801483945, -0.7540106309498033, 1.2809585946909632
        ])
    return np.array(command) - offset


if __name__ == '__main__':
    k3lso = K3lso(None)
    controller = PoseController(k3lso, 0)
    action = action()
    print('Action:')
    print(np.array(action))
    print('Radians:')
    print(convert_pos_ros(action))
    print('no. of rotations:')
    print(convert_pos_ros(action)/(2 * 3.1415))

