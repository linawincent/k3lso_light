import numpy as np

from robot_gym.model.equipment import camera
from util import pybullet_data
import imu
# from robot_gym.util import pybullet_data
import model.robots.k3lso.marks


class Robot:

    def __init__(self,
                 imu,
                 mark,
                 motor_control_mode,
                 pybullet_client,
                 z_offset=0.0
                 ):

        self.imu = imu
        self._pybullet_client = None
        self.motor_angles = []
        # self._simulation = simulation
        self._z_offset = z_offset
        self._mark = mark
        self._marks = self.GetMarks()
        self._constants = self.GetConstants()
        self._ctrl_constants = self.GetCtrlConstants()
        self._num_motors = self._marks.MARK_PARAMS[self._mark]['num_motors']
        self._num_legs = self._marks.MARK_PARAMS[self._mark]['num_legs']
        self._motors_name = self._marks.MARK_PARAMS[self._mark]['motor_names']
        self._motor_enabled_list = self.GetMotorConstants().MOTOR_ENABLED
        self._motor_offset = self.GetMotorConstants().MOTOR_OFFSET
        self._motor_direction = self.GetMotorConstants().MOTOR_DIRECTION
        self.joint_names = self._marks.MARK_PARAMS[self._mark]['motor_names']
        # load robot urdf
        # self._quadruped = self._load_urdf()
        # # build joints dict
        # self._BuildJointNameToIdDict()
        # self._BuildUrdfIds()
        # self._BuildMotorIdList()
        # set robot init pose
        # self.ResetPose()
        # fetch joints' states
        # self.ReceiveObservation()


        # Test
        self._MapContactForceToJointTorques = None
        self._ComputeMotorAnglesFromFootLocalPosition = None
        # build locomotion motor model
        """self._motor_model = self.GetMotorClass()(
            kp=self.GetMotorConstants().MOTOR_POSITION_GAINS,
            kd=self.GetMotorConstants().MOTOR_VELOCITY_GAINS,
            motor_control_mode=motor_control_mode,
            num_motors=self._num_motors
        )"""
        # robot equipment
        # self._load_equipment()

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

    def set_MapContactForceToJointTorques(self, func):
        self._MapContactForceToJointTorques = func

    def set_ComputeMotorAnglesFromFootLocalPosition(self, func):
        self._ComputeMotorAnglesFromFootLocalPosition = func

    def MapContactForceToJointTorques(self, leg_id, force):
        return self._MapContactForceToJointTorques(leg_id=leg_id, contact_force=force)

    def ComputeMotorAnglesFromFootLocalPosition(self, leg_id, foot_position):
        return self._ComputeMotorAnglesFromFootLocalPosition(
            leg_id=leg_id,
            foot_local_position=foot_position
        )

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

    def ReceiveObservation(self):
        self._joint_states = self._pybullet_client.getJointStates(self._quadruped, self._motor_id_list)

    def _load_urdf(self):
        x, y, z = self._constants.START_POS
        start_position = [x, y, z + self._z_offset]
        return self._pybullet_client.loadURDF(
            f"{pybullet_data.getDataPath()}/{self._marks.MARK_PARAMS[self._mark]['urdf_name']}", start_position)

    def ResetPose(self):
        for name in self._joint_name_to_id:
            joint_id = self._joint_name_to_id[name]
            self._pybullet_client.setJointMotorControl2(
                bodyIndex=self._quadruped,
                jointIndex=joint_id,
                controlMode=self._pybullet_client.VELOCITY_CONTROL,
                targetVelocity=0,
                force=0)
        for name, i in zip(self._motors_name, range(len(self._motors_name))):
            if self._constants.HIP_JOINTS_PATTERN in name:
                angle = self._constants.INIT_MOTOR_ANGLES[i] + self._constants.HIP_JOINT_OFFSET
            elif self._constants.UPPER_JOINTS_PATTERN in name:
                angle = self._constants.INIT_MOTOR_ANGLES[i] + self._constants.UPPER_LEG_JOINT_OFFSET
            elif self._constants.LOWER_JOINTS_PATTERN in name:
                angle = self._constants.INIT_MOTOR_ANGLES[i] + self._constants.LOWER_LEG_JOINT_OFFSET
            else:
                raise ValueError("The name %s is not recognized as a motor joint." %
                                 name)
            self._pybullet_client.resetJointState(
                self._quadruped, self._joint_name_to_id[name], angle, targetVelocity=0)

    def _GetMotorNames(self):
        return self._motors_name

    def _BuildMotorIdList(self):
        self._motor_id_list = [
            self._joint_name_to_id[motor_name]
            for motor_name in self._GetMotorNames()
        ]

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
        return self.imu.get_orientation()

    '''
        TransformAngularVelocityToLocalFrame only used in minotaur
    '''
    # def TransformAngularVelocityToLocalFrame(self, angular_velocity, orientation):
    #     """Transform the angular velocity from world frame to robot's frame.
    #     Args:
    #       angular_velocity: Angular velocity of the robot in world frame.
    #       orientation: Orientation of the robot represented as a quaternion.
    #     Returns:
    #       angular velocity of based on the given orientation.
    #     """
    #     # Treat angular velocity as a position vector, then transform based on the
    #     # orientation given by dividing (or multiplying with inverse).
    #     # Get inverse quaternion assuming the vector is at 0,0,0 origin.
    #     _, orientation_inversed = self._pybullet_client.invertTransform([0, 0, 0],
    #                                                                     orientation)
    #     # Transform the angular_velocity at neutral orientation using a neutral
    #     # translation and reverse of the given orientation.
    #     relative_velocity, _ = self._pybullet_client.multiplyTransforms(
    #         [0, 0, 0], orientation_inversed, angular_velocity,
    #         self._pybullet_client.getQuaternionFromEuler([0, 0, 0]))
    #     return np.asarray(relative_velocity)

    def GetBaseRollPitchYawRate(self):
        """Get the rate of orientation change of K3lso's base in euler angle.
        Returns:
          rate of (roll, pitch, yaw) change of the minitaur's base.
        """
        return self.imu.get_angular_velocity()

    def GetFootContacts(self):
        all_contacts = self._pybullet_client.getContactPoints(bodyA=self._quadruped)

        contacts = [False, False, False, False]
        for contact in all_contacts:
            # Ignore self contacts
            if contact[self._constants.BODY_B_FIELD_NUMBER] == self._quadruped:
                continue
            try:
                toe_link_index = self._foot_link_ids.index(
                    contact[self._constants.LINK_A_FIELD_NUMBER])
                contacts[toe_link_index] = True
            except ValueError:
                continue
        return contacts

    def GetMotorAngles(self):
        # TODO: from ROS node
        # motor_angles = [state[0] for state in self._joint_states]
        # motor_angles = np.multiply(
        #     np.asarray(motor_angles) - np.asarray(self._motor_offset),
        #     self._motor_direction)

        return self.motor_angles

    def GetTrueMotorAngles(self):
        # TODO: from ROS node, same as previous?
        """Gets the twelve motor angles at the current moment, mapped to [-pi, pi].
        Returns:
          Motor angles, mapped to [-pi, pi].
        """
        self.ReceiveObservation()

        return self.GetMotorAngles()

    def GetPDObservation(self):
        # TODO: From ROS
        self.ReceiveObservation()
        observation = []
        observation.extend(self.GetTrueMotorAngles())
        observation.extend(self.GetTrueMotorVelocities())
        q = observation[0:self._num_motors]
        qdot = observation[self._num_motors:2 * self._num_motors]
        return np.array(q), np.array(qdot)

    def GetTrueMotorVelocities(self):
        # TODO: From ROS
        """Get the velocity of all eight motors.
        Returns:
          Velocities of all eight motors.
        """
        motor_velocities = [state[1] for state in self._joint_states]

        motor_velocities = np.multiply(motor_velocities, self._motor_direction)
        return motor_velocities

    def GetTrueObservation(self):
        self.ReceiveObservation()
        observation = []
        observation.extend(self.GetTrueMotorAngles())
        observation.extend(self.GetTrueMotorVelocities())
        observation.extend(self.GetTrueMotorTorques())
        observation.extend(self.GetTrueBaseOrientation())
        observation.extend(self.GetTrueBaseRollPitchYawRate())
        return observation

    def _BuildJointNameToIdDict(self):
        num_joints = self._pybullet_client.getNumJoints(self._quadruped)
        self._joint_name_to_id = {}
        for i in range(num_joints):
            joint_info = self._pybullet_client.getJointInfo(self._quadruped, i)
            self._joint_name_to_id[joint_info[1].decode("UTF-8")] = joint_info[0]
            
    def _BuildUrdfIds(self):
        """Build the link Ids from its name in the URDF file.
        Raises:
          ValueError: Unknown category of the joint name.
        """
        num_joints = self._num_motors # self._pybullet_client.getNumJoints(self._quadruped)
        self._chassis_link_ids = [-1]
        self._leg_link_ids = []
        self._motor_link_ids = []
        self._knee_link_ids = []
        self._foot_link_ids = []

        for i in range(num_joints):
            joint_info = self._pybullet_client.getJointInfo(self._quadruped, i)
            joint_name = joint_info[1].decode("UTF-8")
            joint_id = self._joint_name_to_id[joint_name]
            if self._constants.CHASSIS_NAME_PATTERN.match(joint_name):
                self._chassis_link_ids.append(joint_id)
                print("chassi")
            elif self._constants.HIP_NAME_PATTERN.match(joint_name):
                self._motor_link_ids.append(joint_id)
                print("hip")
            elif self._constants.UPPER_NAME_PATTERN.match(joint_name):
                self._motor_link_ids.append(joint_id)
                print("upper")
            # We either treat the lower leg or the toe as the foot link, depending on
            # the urdf version used.
            elif self._constants.LOWER_NAME_PATTERN.match(joint_name):
                self._knee_link_ids.append(joint_id)
                print("lower")
            elif self._constants.TOE_NAME_PATTERN.match(joint_name):
                # assert self._urdf_filename == URDF_WITH_TOES
                self._foot_link_ids.append(joint_id)
                print("foot")
                print(self._constants.TOE_NAME_PATTERN)
            else:
                raise ValueError("Unknown category of joint %s" % joint_name)

        self._leg_link_ids.extend(self._knee_link_ids)
        self._leg_link_ids.extend(self._foot_link_ids)

        # assert len(self._foot_link_ids) == NUM_LEGS
        self._chassis_link_ids.sort()
        self._motor_link_ids.sort()
        self._knee_link_ids.sort()
        self._foot_link_ids.sort()
        self._leg_link_ids.sort()

        return


    def link_position_in_base_frame(self, link_id):
        """Computes the link's local position in the robot frame.
        Args:
          link_id: The link to calculate its relative position.
        Returns:
          The relative position of the link.
        """
        # Asssumes link_id has values between 0,1,2,3
        motor_angles = self.motor_angles[link_id : link_id + 3]

        local_link_position = self._ctrl_constants.mpc_link_default[link_id]

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
        
        print(foot_positions)
        return np.array(foot_positions)

    def Terminate(self):
        pass

    def update_motor_angles(self, angles):
        self.motor_angles = angles

