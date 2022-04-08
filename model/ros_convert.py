import numpy as np

offset_motor = np.array([
    -0.02132762, 0.84722027, -1.69444054,
    -0.02132762, 0.84722027, 1.69444054,
    -0.02132762, -0.84722027, -1.69444054,
    -0.02132762, -0.84722027, 1.69444054
])

# Better zero-position for k3lso
offset_orig = np.array([
    0, 0.1, -0.1, 0.1, -0.1, 0.1,
    -0.1, 0, 0, 0, 0.15, -0.07
])

pi2 = (2 * 3.14159265)
ids = [2, 3, 4, 6, 7, 8]


def invert(command):
    for j in ids:
        command[j - 1] = -command[j - 1]
    return command


def convert_to_ros(command):
    """ From Python-angles to ROS-angles """
    transformed_command = invert((np.array(command) - offset_motor) / pi2) + offset_orig / pi2
    return transformed_command.tolist()


def convert_from_ros(command):
    """ From ROS-angles to Python-angles """
    transformed_command = pi2 * invert(np.array(command) - offset_orig / pi2) + offset_motor
    return transformed_command.tolist()
