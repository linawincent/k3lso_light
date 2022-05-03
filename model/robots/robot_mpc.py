import numpy as np



class Robot:

    def __init__(self,
                 imu,
                 mark,
                 pybullet_client,
                 motor_control_mode = 1,
                 z_offset=0.0
                                  ):

        self.imu = imu
        self._pybullet_client = pybullet_client
        self.motor_angles = []
        self._mark = mark
        self._marks = self.GetMarks()
        self._constants = self.GetConstants()
        self._ctrl_constants = self.GetCtrlConstants()
        self._num_motors = self._marks.MARK_PARAMS[self._mark]['num_motors']
        self._num_legs = self._marks.MARK_PARAMS[self._mark]['num_legs']
        self._motors_name = self._marks.MARK_PARAMS[self._mark]['motor_names']
        self._motor_offset = self.GetMotorConstants().MOTOR_OFFSET
        self._motor_direction = self.GetMotorConstants().MOTOR_DIRECTION
        self.joint_names = self._marks.MARK_PARAMS[self._mark]['motor_names']
        self._foot_link_ids = [3, 7, 11, 15]
        self.motor_angles = np.zeros(12)
        self.motor_torques = np.zeros(12)


    @property
    def num_legs(self):
        return self._num_legs

    @property
    def num_motors(self):
        return self._num_motors

    @property
    def pybullet_client(self):
        return self._pybullet_client

    @property
    def equipment(self):
        return self._equip

    def set_up_discrete_action_space(self):
        pass

    def set_up_continuous_action_space(self):
        pass

    def GetBasePosition(self):
        """Get the position of K3slo's base.
        Returns:
          The position of K3lso's base.
        """
        return self.imu.get_position()

    def GetBaseRollPitchYaw(self):
        """Get the orientation of K3lso's base.
        Returns:
          The orientation of K3lso's base.
        """
        return self.imu.get_orientation()

    def GetMotorPositionGains(self):
        return self.GetMotorConstants().MOTOR_POSITION_GAINS

    def GetMotorVelocityGains(self):
        return self.GetMotorConstants().MOTOR_VELOCITY_GAINS

    def MapContactForceToJointTorques(self, leg_id, force):
        leg_id = leg_id * 3
        motor_torques = {
            leg_id: self.motor_torques[leg_id],
            leg_id + 1: self.motor_torques[leg_id + 1],
            leg_id + 2: self.motor_torques[leg_id + 2]
        }
        return motor_torques

    def ComputeMotorAnglesFromFootLocalPosition(self, leg_id, foot_position):
        leg_id = leg_id * 3
        motor_angles = self.motor_angles[leg_id : leg_id + 3]
        motor_index = [*range(leg_id, leg_id + 3)]
        return motor_index, motor_angles

    @property
    def GetJointStates(self):
        return self._joint_states

    @property
    def GetRobotId(self):
        return self._quadruped

    @property
    def GetFootLinkIds(self):
        return self._foot_link_ids

    @property
    def GetMotorModel(self):
        return self._motor_model

    def GetHipPositionsInBaseFrame(self):
        return self._constants.DEFAULT_HIP_POSITIONS

    def GetBaseVelocity(self):
        """Get the linear velocity of K3lso's base.
        Returns:
          The velocity of K3lso's base.
        """
        return self.imu.get_velocity()

    def GetTrueBaseOrientation(self):
        # TODO: Other true/predicitve orientation compared to before
        return self.imu.get_q()
    
    def GetBaseRollPitchYawRate(self):
        """Get the rate of orientation change of K3lso's base in euler angle.
        Returns:
          rate of (roll, pitch, yaw) change of the minitaur's base.
        """
        return self.imu.get_angular_velocity()

    def GetFootContacts(self):
        # TODO: add entry point for ROS to feed torque values
        contacts = [False, False, False, False]

        return contacts

    def link_position_in_base_frame(self, link_id):
        """Computes the link's local position in the robot frame.
        Args:
          link_id: The link to calculate its relative position.
        Returns:
          The relative position of the link.
        """
        # Asssumes link_id has values between 0,1,2,3
        link_id = self._foot_link_ids.index(link_id)
        
        local_link_position = self._ctrl_constants.mpc_link_default[link_id]


        link_id = 3 * link_id
        motor_angles = self.motor_angles[link_id : (link_id + 3)]

        local_foot_position = np.array([
            self._ctrl_constants.leg * (np.cos(motor_angles[1] + motor_angles[2]) - np.cos(motor_angles[1])),
            self._ctrl_constants.mpc_hip_lenght * np.cos(motor_angles[0]),
            self._ctrl_constants.leg * (np.sin(motor_angles[1]) - np.sin(motor_angles[1] + motor_angles[2]))
        ])

        return local_link_position + local_foot_position

    def GetFootLinkIDs(self):
        """Get list of IDs for all foot links."""
        return self._foot_link_ids

    def GetFootPositionsInBaseFrame(self):
        """Get the robot's foot position in the base frame."""
        # assert len(self._foot_link_ids) == self._num_legs
        foot_positions = []
        for foot_id in self.GetFootLinkIDs():
            foot_positions.append(
                self.link_position_in_base_frame(link_id=foot_id)
            )
        
        return np.array(foot_positions)

    def Terminate(self):
        pass

    def update_motor_angles(self, angles):
        self.motor_angles = angles

    def update_motor_torques(self, torques):
        self.motor_torques = torques
