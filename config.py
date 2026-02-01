'''
camera res
servo pins
angles/limits
tracking
distance calibration
which tracking to track for (humans, colour, object)
'''

# config.py
import numpy as np

# Camera
PREVIEW_SIZE = (640, 480)

# Red HSV thresholds (two ranges because red wraps hue)
LOWER_RED1 = np.array([0, 120, 70], dtype=np.uint8)
UPPER_RED1 = np.array([10, 255, 255], dtype=np.uint8)
LOWER_RED2 = np.array([170, 120, 70], dtype=np.uint8)
UPPER_RED2 = np.array([180, 255, 255], dtype=np.uint8)

# Detection tuning
MIN_AREA = 800
DEADBAND_PX = 10

# Servo usage
USE_SERVO = False  # flip True when ready

# Servo pins (BCM)
PAN_PIN = 18
TILT_PIN = None  # set to a BCM pin if you have tilt

# Servo PWM + movement
SERVO_FREQ = 50
PAN_CENTER = 7.2
TILT_CENTER = 7.2

PAN_MIN, PAN_MAX = 5.0, 9.5
TILT_MIN, TILT_MAX = 5.0, 9.5

SERVO_STEP = 0.03
