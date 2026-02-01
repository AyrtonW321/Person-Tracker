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
PREVIEW_SIZE = (1280, 960)

COLOR_RANGES = {
    # Target red: hex #CB132B (tight range)
    # Approx HSV(OpenCV): H~176, S~231, V~203
    "cb132b_red": [
        (np.array([173, 170,  60], dtype=np.uint8), 
         np.array([179, 255, 255], dtype=np.uint8)),
        # If you ever want slightly wider detection, you can add a 2nd range near 0,
        # but for tight CB132B, usually this one range is enough.
        # (np.array([  0, 170,  60], dtype=np.uint8), np.array([  2, 255, 255], dtype=np.uint8)),
    ],

    # Example placeholders for later (optional):
    # "blue": [
    #     (np.array([100, 150, 60], dtype=np.uint8), np.array([130, 255, 255], dtype=np.uint8)),
    # ],
}

ACTIVE_COLORS = ["cb132b_red"]

# Detection tuning
MIN_AREA = 2000
DEADBAND_PX = 15

# Servo usage
USE_SERVO = True  # flip True when ready

# Servo pins (BCM)
PAN_PIN = 18
TILT_PIN = 13

# Servo PWM + movement
SERVO_FREQ = 50
PAN_CENTER = 7.2
TILT_CENTER = 7.2

PAN_MIN, PAN_MAX = 5.0, 9.5
TILT_MIN, TILT_MAX = 5.0, 9.5

SERVO_STEP = 0.015
SERVO_UPDATE_S = 0.2

# Servo control tuning
SERVO_KP_PAN = 0.0008
SERVO_KP_TILT = 0.0008

SERVO_MAX_STEP = 0.06  # cap per update to prevent crazy jumps
# SERVO_UPDATE_S already in your config (0.03) is good


# Vision smoothing / cleanup
MASK_KERNEL = (5, 5)     # try (3,3) if you want tighter, (7,7) if noisy
OPEN_ITERS = 1
CLOSE_ITERS = 1

CENTER_SMOOTH_ALPHA = 0.25
# 0.15 = very smooth but slower
# 0.25 = balanced
# 0.40 = faster but more jitter

