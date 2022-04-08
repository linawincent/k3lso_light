import threading
import numpy as np
from controllers.pose.pose_controller import PoseController
from model.robots.k3lso.k3lso import K3lso
from gui import Application
import model.ros_convert

class Pose:

    def __init__(self):
        kelso = K3lso(None)
        self.controller = PoseController(kelso, 0)
        self.signal = []
        self.app = None

        thd = threading.Thread(target=self.runtk)  # gui thread
        thd.daemon = True  # background thread will exit if main thread exits
        thd.start()  # start tk loop

    def update_signal(self, position, orientation):
        self.controller.update_controller_params(position, orientation)
        self.signal = self.controller.get_action()

    def get_signal(self):
        return model.ros_convert.convert_to_ros(self.signal)

    def runtk(self):  # runs in background thread
        self.app = Application()
        self.app.master.title('Gui Pose')
        self.app.mainloop()

    def check_gui(self):
        orientation = self.app.get_orientation()
        position = self.app.get_position()
        return position, orientation
