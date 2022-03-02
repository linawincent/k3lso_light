import sys

from controllers.pose.pose_controller import PoseController
from model.robots.k3lso.k3lso import K3lso 

def format_values(xpos, ypos, zpos, roll, pitch, yaw):
    position = [xpos, ypos, zpos]
    orientation = [roll, pitch, yaw]
    return position, orientation

if __name__ == "__main__":
    xpos = float(sys.argv[1])
    ypos = float(sys.argv[2])
    zpos = float(sys.argv[3])
    roll = float(sys.argv[4])
    pitch = float(sys.argv[5])
    yaw = float(sys.argv[6])

    kelso = K3lso(None)
    controller = PoseController(kelso, 0)
    controller.update_controller_params(format_values(xpos, ypos, zpos, roll, pitch, yaw))
    print(controller.get_action())




