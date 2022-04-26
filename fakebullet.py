'''
    Object with purpose of faking the pybullet client object that
    needs to be passed into the com_velocity_estimator
'''

class Fakebullet():

    def __init__(self):
        pass

    def invertTransform(self, vec3, base_orientation):
        return

    def multiplyTransforms(self, vec3, inverse_rotation, com_velocity_world_frame,
            vec4):
        return