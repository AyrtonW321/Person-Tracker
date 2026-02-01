# Import libraries
import numpy as np

# Camera Size
PREVIEW_SIZE = (1280, 960)

# Change the colour that you want to track
COLOR_RANGES = {
    "cb132b_red": [
        (
            np.array([173, 170, 60], dtype=np.uint8),  # Lower Bound
            np.array([179, 255, 255], dtype=np.uint8), # Upper Bound
        ),
    ],
}

ACTIVE_COLORS = ["cb132b_red"] # Changes the active colours

# Detection tuning
MIN_AREA = 1000 # Minimum area(px) of an object for detection
DEADBAND_PX = 0  # The error from the crosshair to the centre of the object

# Servo usage
USE_SERVO = False
# Tracking mode
TRACK_MODE = "colour"

# Servo pins
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
SERVO_KP_PAN = 0.35
SERVO_KP_TILT = 0.35

# Cap how much to change per update (microseconds)
SERVO_MAX_STEP_US = 16 #changed

# Flip directions if camera is mirrored or not
PAN_INVERT = False
TILT_INVERT = True

# Vision smoothing / cleanup
# Defines the size of the kernel for cleaning up the mask
# Larger kernel, more clean up -> Smaller kernel, less clean up
MASK_KERNEL = (10, 10) 
OPEN_ITERS = 1 # Removes noise (1-2), erode -> dialate
CLOSE_ITERS = 1 # Adds noise (1-2) dialate -> erode
CENTER_SMOOTH_ALPHA = 1 # Controls the smoothing of the center, how responsive the center jumps when the object moves
ERROR_SMOOTH_ALPHA = 1 # Controls the smoothing of the error signal

# Distance calculations
KNOWN_TARGET_WIDTH_CM = 6.5      # Set to real target width
CALIB_DISTANCE_CM = 50.0         # Calibration distance measurement
FOCAL_LENGTH_PX = None           # Will be computed when you press "c"

DIST_SMOOTH_ALPHA = 0.25         # 0.15-0.35 good range (higher = more responsive)