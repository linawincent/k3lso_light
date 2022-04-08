import numpy as np
import model.ros_convert

class Kinematics:

    def __init__(self,
                 robot
                 ):

        self._pybullet_client = robot.pybullet_client
        self._robot = robot

    def MapContactForceToJointTorques(self, leg_id, all_motor_torques):
        # TODO: Torques from ROS?
        """Maps the foot contact force to the leg joint torques."""
        motor_torques = {}
        motors_per_leg = self._robot.GetMotorConstants().NUM_MOTORS // self._robot.GetConstants().NUM_LEG
        com_dof = 6
        for joint_id in range(leg_id * motors_per_leg,
                              (leg_id + 1) * motors_per_leg):
            motor_torques[joint_id] = all_motor_torques[
                                          com_dof + joint_id
                                      ] * self._robot.GetMotorConstants().MOTOR_DIRECTION[joint_id]

        return motor_torques

    def ComputeMotorAnglesFromFootLocalPosition(self, leg_id, angles):
        # TODO: motor angles from ROS, name change
        """Use IK to compute the motor angles, given the foot link's local position.
        Args:
          leg_id: The leg index.
          foot_local_position: The foot link's position in the base frame.
        Returns:
          A tuple. The position indices and the angles for all joints along the
          leg. The position indices is consistent with the joint orders as returned
          by GetMotorAngles API.
        """
        joint_angles = model.ros_convert.convert_from_ros(angles)
        motors_per_leg = self._robot.num_motors // self._robot.GetConstants().NUM_LEG
        joint_position_idxs = [
            i for i in range(leg_id * motors_per_leg, leg_id * motors_per_leg +
                             motors_per_leg)
        ]

        return joint_position_idxs, joint_angles.tolist()
