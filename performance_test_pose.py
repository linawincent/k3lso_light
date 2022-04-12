from pose import Pose
import time



pose = Pose()
time.sleep(0.01)
data = pose.check_gui()
pose.update_signal(data[0], data[1])
print(pose.get_signal())