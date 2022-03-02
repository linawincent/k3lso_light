from controllers.pose.pose_controller import PoseController
from model.robots.k3lso.k3lso import K3lso 

def set_values(controller):
    position = [0, 0, 0]
    orientation = [0, 0, 0]
    return position, orientation

if __name__ == "__main__":
    kelso = K3lso(None)
    controller = PoseController(kelso, 0)
    controller.update_controller_params(set_values(controller))
    print(controller.get_action())

    # while(True):
        
    #     controller.get_action()
    #     set_values(controller)

    #     print("test")




