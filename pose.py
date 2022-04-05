import threading
import numpy as np
from controllers.pose.pose_controller import PoseController
from model.robots.k3lso.k3lso import K3lso
from gui import Application


class Pose:

    def __init__(self):
        kelso = K3lso(None)
        self.controller = PoseController(kelso, 0)
        self.signal = []
        self.app = None

        thd = threading.Thread(target=self.runtk)  # gui thread
        thd.daemon = True  # background thread will exit if main thread exits
        thd.start()  # start tk loop

    def convert_pos_ros(self, command):
        # From radians to relative radians for Ros-commands and sign-change

        # Since k3lso calculates 0 from defined position
        offset_motor = np.array([
            -0.02132762,  0.84722027, -1.69444054,
            -0.02132762,  0.84722027,  1.69444054,
            -0.02132762, -0.84722027, -1.69444054,
            -0.02132762, -0.84722027,  1.69444054
        ])
        # Old position for k3lso with updated dimensions
        # -0.03964886725138972, 1.1035218357931036, -1.9554858419361683,
        # -0.03964886725138994, 1.1035218357931036, 1.9554858419361683,
        # -0.03964886725138972, -1.1035218357931036, -1.9554858419361683,
        # -0.03964886725138994, -1.1035218357931036, 1.9554858419361683

        # Better zero-position for k3lso
        offset_orig = np.array([
            0, 0.1, -0.1, 0.1, -0.1, 0.1,
            -0.1, 0, 0, 0, 0.15, -0.07
        ])

        transformed_command = (np.array(command) - offset_motor ) / (2 * 3.14159265)
        ids = [2, 3, 4, 6, 7, 8]
        for j in ids:
            transformed_command[j-1] = -transformed_command[j-1]

        transformed_command += offset_orig / (2 * 3.14159265)
        return transformed_command.tolist()

    def update_signal(self, position, orientation):
        self.controller.update_controller_params(position, orientation)
        self.signal = self.controller.get_action()

    def get_signal(self):
        return self.convert_pos_ros(self.signal)

    def runtk(self):  # runs in background thread
        self.app = Application()
        self.app.master.title('Gui Pose')
        self.app.mainloop()

    def check_gui(self):
        orientation = self.app.get_orientation()
        position = self.app.get_position()
        return position, orientation
