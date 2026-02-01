import numpy as np

'''Camera
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
DEADBAND_PX = 0 #changed

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
SERVO_KP_PAN = 0.35 #changed   # us per pixel
SERVO_KP_TILT = 0.35 #changed  # us per pixel

# Cap how much to change per update (microseconds)
SERVO_MAX_STEP_US = 16 #changed

# Flip direction if needed
PAN_INVERT = False
TILT_INVERT = True

# Vision smoothing / cleanup
MASK_KERNEL = (10, 10)
OPEN_ITERS = 1
CLOSE_ITERS = 1
CENTER_SMOOTH_ALPHA = 1
ERROR_SMOOTH_ALPHA = 1 #changed
'''

# ----------------------------
# Camera
# ----------------------------
PREVIEW_SIZE = (1280, 960)

# ----------------------------
# TRACKING MODE
# ----------------------------
# For now: human detection only
TRACK_MODE = "person"   # "person" or "color"

# ----------------------------
# Colour (keep for later)
# ----------------------------
COLOR_RANGES = {
    "cb132b_red": [
        (np.array([170, 120, 60], dtype=np.uint8),
         np.array([179, 255, 255], dtype=np.uint8)),
    ],
}
ACTIVE_COLORS = ["cb132b_red"]

# ----------------------------
# Detection tuning (general)
# ----------------------------
MIN_AREA = 1000
DEADBAND_PX = 10

# ----------------------------
# Person (HOG) tuning
# ----------------------------
# Big performance win: run HOG on a resized frame and scale boxes back.
PERSON_DETECT_WIDTH = 640      # try 480 if slow, set None to disable resize

PERSON_MIN_AREA = 2500         # reject tiny detections
PERSON_DEADBAND_PX = 10
PERSON_MIN_WEIGHT = 0.6        # raise if too many false positives (0.7–1.2)

# HOG speed/accuracy
PERSON_WIN_STRIDE = (8, 8)     # (4,4) more accurate but slower
PERSON_PADDING = (8, 8)
PERSON_SCALE = 1.05            # closer to 1.0 = slower but more accurate

# ----------------------------
# Servo usage (OFF for now)
# ----------------------------
USE_SERVO = False

# Servo pins (BCM) - keep for later
PAN_PIN = 18
TILT_PIN = 13

# pigpio servo settings (µs) - keep for later
PAN_US_MIN = 600
PAN_US_MAX = 2400
PAN_US_CENTER = 1500

TILT_US_MIN = 600
TILT_US_MAX = 2400
TILT_US_CENTER = 1500

SERVO_UPDATE_S = 0.03
SERVO_KP_PAN = 0.30
SERVO_KP_TILT = 0.30
SERVO_MAX_STEP_US = 10

PAN_INVERT = False
TILT_INVERT = True

# Vision smoothing (keep for later)
MASK_KERNEL = (10, 10)
OPEN_ITERS = 1
CLOSE_ITERS = 1
CENTER_SMOOTH_ALPHA = 0.35
ERROR_SMOOTH_ALPHA = 0.20

LOCK_TIME_S = 0.2
HOLD_TIME_S = 2.0

