'''
camera res
servo pins
angles/limits
tracking
distance calibration
which tracking to track for (humans, colour, object)
'''

import numpy as np

# Camera
PREVIEW_SIZE = (1280, 960)

COLOR_RANGES = {
    "cb132b_red": [
        (np.array([173, 170,  60], dtype=np.uint8),
         np.array([179, 255, 255], dtype=np.uint8)),
    ],
}

ACTIVE_COLORS = ["cb132b_red"]

# Detection tuning
MIN_AREA = 2000
DEADBAND_PX = 25

# Servo usage
USE_SERVO = True

# Servo pins (BCM)
PAN_PIN = 18
TILT_PIN = 13

# Servo PWM + movement
SERVO_FREQ = 50
PAN_CENTER = 7.2
TILT_CENTER = 7.2

PAN_MIN, PAN_MAX = 5.0, 9.5
TILT_MIN, TILT_MAX = 5.0, 9.5

# Servo timing: how often to apply a servo update
SERVO_UPDATE_S = 0.75

# Servo control tuning (proportional)
SERVO_KP_PAN = 0.0006
SERVO_KP_TILT = 0.0006
SERVO_MAX_STEP = 0.02

# If your servos move the wrong way, flip these booleans
PAN_INVERT = False
TILT_INVERT = True

# Vision smoothing / cleanup
MASK_KERNEL = (5, 5)
OPEN_ITERS = 1
CLOSE_ITERS = 1
CENTER_SMOOTH_ALPHA = 0.12

ERROR_SMOOTH_ALPHA = 0.12
LOCK_TIME_S = 0.5
HOLD_TIME_S = 1.0