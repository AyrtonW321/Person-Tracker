import numpy as np

# Camera
PREVIEW_SIZE = (1280, 960)

COLOR_RANGES = {
    "cb132b_red": [
        (np.array([170, 120, 60], dtype=np.uint8),
        np.array([179, 255, 255], dtype=np.uint8)),
    ],

}
ACTIVE_COLORS = ["cb132b_red"]

# Detection tuning
MIN_AREA = 1000
DEADBAND_PX = 20

# Servo usage
USE_SERVO = True

# Servo pins (BCM)
PAN_PIN = 18
TILT_PIN = 13

# ----------------------------
# pigpio servo settings (µs)
# ----------------------------
# Typical usable range is ~500–2500us, center ~1500us.
# You MUST tune these for your mount so you don't hit hard stops.
PAN_US_MIN = 600
PAN_US_MAX = 2400
PAN_US_CENTER = 1500

TILT_US_MIN = 600
TILT_US_MAX = 2400
TILT_US_CENTER = 1500

# How often to apply a servo update (seconds)
SERVO_UPDATE_S = 0.02

# Proportional tuning: converts pixel error -> microseconds change
# Bigger KP => more movement for the same error.
SERVO_KP_PAN = 0.30   # us per pixel
SERVO_KP_TILT = 0.30  # us per pixel

# Cap how much to change per update (microseconds)
SERVO_MAX_STEP_US = 8

# Flip direction if needed
PAN_INVERT = False
TILT_INVERT = True

# Vision smoothing / cleanup
MASK_KERNEL = (10, 10)
OPEN_ITERS = 1
CLOSE_ITERS = 1
CENTER_SMOOTH_ALPHA = 0.35
ERROR_SMOOTH_ALPHA = 0.10
