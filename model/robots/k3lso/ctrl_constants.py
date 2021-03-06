import numpy as np


# -------------------------------------------------
# MPC Controller
# -------------------------------------------------
MPC_BODY_MASS = 190 / 9.8
# MPC_BODY_INERTIA = (0.020299, 0, 0, 0, 0.102942, 0, 0, 0, 0.116746)
#MPC_BODY_INERTIA = (0.07335, 0, 0, 0, 0.25068, 0, 0, 0, 0.25447) #//working

MPC_BODY_INERTIA = (0.07335, 0, 0, 0, 0.25068, 0, 0, 0, 0.25447)
MPC_BODY_HEIGHT = 0.35
MPC_VELOCITY_MULTIPLIER = 1.0

STANCE_DURATION_SECONDS = [0.19] * 4  # For faster trotting (v > 1.5 ms reduce this to 0.13s).
MAX_TIME_SECONDS = 30.

# Standing
# DUTY_FACTOR = [1.] * 4
# INIT_PHASE_FULL_CYCLE = [0., 0., 0., 0.]
#
# INIT_LEG_STATE = (
#     gait_generator_lib.LegState.STANCE,
#     gait_generator_lib.LegState.STANCE,
#     gait_generator_lib.LegState.STANCE,
#     gait_generator_lib.LegState.STANCE,
# )

# Trotting
DUTY_FACTOR = [0.6] * 4
INIT_PHASE_FULL_CYCLE = [0.9, 0, 0, 0.9]

# INIT_LEG_STATE = (
#     gait_generator_lib.LegState.SWING,
#     gait_generator_lib.LegState.STANCE,
#     gait_generator_lib.LegState.STANCE,
#     gait_generator_lib.LegState.SWING,
# )

VX_OFFSET = -0.042
VY_OFFSET = 0.005
WZ_OFFSET = -0.

# -------------------------------------------------
# Pose Controller
# -------------------------------------------------

"""l = 0.246
w = 0.055
hip = 0.105
leg = 0.20652
foot = 0.245
y_dist = 0.285
x_dist = l
height = 0.25"""

""" Updated constants"""
l = 0.6
w = 0.256
hip = 0.0049
leg = 0.34
foot = 0.34
y_dist = 0.285
x_dist = l
height = 0.45

# frame vectors
hip_front_right_v = np.array([l / 2, -w / 2, 0])
hip_front_left_v = np.array([l / 2, w / 2, 0])
hip_rear_right_v = np.array([-l / 2, -w / 2, 0])
hip_rear_left_v = np.array([-l / 2, w / 2, 0])
foot_front_right_v = np.array([x_dist / 2, -y_dist / 2, -height])
foot_front_left_v = np.array([x_dist / 2, y_dist / 2, -height])
foot_rear_right_v = np.array([-x_dist / 2, -y_dist / 2, -height])
foot_rear_left_v = np.array([-x_dist / 2, y_dist / 2, -height])


# -------------------------------------------------
# MPC controller
# -------------------------------------------------

# coordinates
mpc_l = 0.6
mpc_w = 0.13
mpc_hip_lenght = 0.13
mpc_hip_FR = np.array([mpc_l/2, -mpc_w/2, 0])
mpc_hip_FL = np.array([mpc_l/2, mpc_w/2, 0])
mpc_hip_RR = np.array([-mpc_l/2, -mpc_w/2, 0])
mpc_hip_RL = np.array([-mpc_l/2, -mpc_w/2, 0])
mpc_link_default = [mpc_hip_FR, mpc_hip_FL, mpc_hip_RR, mpc_hip_RL]